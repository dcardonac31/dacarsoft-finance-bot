"""
LLM Service for natural language parsing.

Uses OpenAI's GPT models to parse Spanish financial messages into structured data.
"""

import json
import logging
from typing import Optional, Dict, Any
from openai import OpenAI
from datetime import datetime

from domain.transaction import Transaction, TransactionType
from domain.capital import CapitalMovement, CapitalType, CapitalStatus
from services.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for parsing natural language financial messages using LLM.
    
    Converts messages like "Gasté 50 mil en comida" into structured Transaction objects.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LLM service.
        
        Args:
            api_key: OpenAI API key (defaults to settings.OPENAI_API_KEY)
        """
        self.client = OpenAI(api_key=api_key or settings.OPENAI_API_KEY)
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the LLM."""
        return """Eres un asistente financiero que ayuda a parsear mensajes en español sobre finanzas personales.

Tu tarea es convertir mensajes de texto en un objeto JSON estructurado.

HAY DOS TIPOS DE MENSAJES:

1. TRANSACCIONES OPERATIVAS (gastos, ingresos, presupuestos):
{
    "tipo": "gasto" | "ingreso" | "presupuesto",
    "monto": <número>,
    "categoria": <string>,
    "descripcion": <string>
}

2. MOVIMIENTOS DE CAPITAL (ahorros, inversiones):
{
    "tipo": "ahorro" | "inversion",
    "monto": <número>,
    "institucion": <string>,
    "descripcion": <string>
}

REGLAS IMPORTANTES:
1. "tipo" debe ser exactamente: "gasto", "ingreso", "presupuesto", "ahorro" o "inversion"
2. "monto" debe ser un número. Si ves "mil" o "k", conviértelo (ej: "50 mil" = 50000)
3. Para transacciones operativas usa "categoria" (comida, transporte, salario)
4. Para movimientos de capital usa "institucion" (banco, cdt, acciones, davivienda)
5. "descripcion" usa el mensaje original
6. Si el mensaje es ambiguo, responde con {"error": "mensaje de error"}

CLASIFICACIÓN:
- Palabras clave para AHORRO: "ahorré", "guardé", "ahorrar", "guardar dinero", "ahorro"
- Palabras clave para INVERSION: "invertí", "inversión", "CDT", "acciones", "bolsa", "plazo fijo"
- Palabras clave para GASTO: "gasté", "compré", "pagué", "me costó"
- Palabras clave para INGRESO: "recibí", "me pagaron", "salario", "ganancia", "ingreso"
- Palabras clave para PRESUPUESTO: "presupuesto", "planear", "asignar"

EJEMPLOS TRANSACCIONES:
- "Gasté 50 mil en comida" → {"tipo": "gasto", "monto": 50000, "categoria": "comida", "descripcion": "Gasté 50 mil en comida"}
- "Recibí 100 mil de salario" → {"tipo": "ingreso", "monto": 100000, "categoria": "salario", "descripcion": "Recibí 100 mil de salario"}
- "Presupuesto de 300 mil para transporte" → {"tipo": "presupuesto", "monto": 300000, "categoria": "transporte", "descripcion": "Presupuesto de 300 mil para transporte"}

EJEMPLOS CAPITAL:
- "Ahorré 100 mil en el banco" → {"tipo": "ahorro", "monto": 100000, "institucion": "banco", "descripcion": "Ahorré 100 mil en el banco"}
- "Invertí 500 mil en CDT" → {"tipo": "inversion", "monto": 500000, "institucion": "cdt", "descripcion": "Invertí 500 mil en CDT"}
- "Guardé 200k en Davivienda" → {"tipo": "ahorro", "monto": 200000, "institucion": "davivienda", "descripcion": "Guardé 200k en Davivienda"}
- "Inversión de 1 millón en acciones" → {"tipo": "inversion", "monto": 1000000, "institucion": "acciones", "descripcion": "Inversión de 1 millón en acciones"}

Responde SOLO con el JSON, sin texto adicional."""
    
    async def parse_message(self, message: str):
        """
        Parse a natural language message into a Transaction or CapitalMovement object.
        
        Args:
            message: Natural language message in Spanish
            
        Returns:
            Transaction or CapitalMovement object if parsing successful, None otherwise
            tuple: (object, "transaction" | "capital") or (None, None)
            
        Example:
            >>> service = LLMService()
            >>> obj, tipo = await service.parse_message("Gasté 50 mil en comida")
            >>> print(tipo)  # "transaction"
            >>> print(obj.monto)  # 50000
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using the faster, cheaper model
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.1,  # Low temperature for consistent parsing
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            logger.info(f"LLM Response: {content}")
            
            # Parse the JSON response
            parsed_data = json.loads(content)
            
            # Check for errors
            if "error" in parsed_data:
                logger.warning(f"LLM returned error: {parsed_data['error']}")
                return None, None
            
            tipo = parsed_data.get("tipo", "").lower()
            
            # Determine if it's a capital movement or transaction
            if tipo in ["ahorro", "inversion"]:
                # Create CapitalMovement object
                capital_data = {
                    "tipo": tipo,
                    "monto": parsed_data.get("monto"),
                    "institucion": parsed_data.get("institucion", "general"),
                    "descripcion": parsed_data.get("descripcion"),
                    "fecha": datetime.now(),
                    "estado": "activo",
                    "retorno": 0.0
                }
                capital = CapitalMovement(**capital_data)
                logger.info(f"Successfully parsed capital movement: {capital}")
                return capital, "capital"
            else:
                # Create Transaction object
                if "fecha" not in parsed_data:
                    parsed_data["fecha"] = datetime.now().isoformat()
                
                transaction = Transaction(**parsed_data)
                logger.info(f"Successfully parsed transaction: {transaction}")
                return transaction, "transaction"
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            return None, None
        except Exception as e:
            logger.error(f"Error parsing message with LLM: {e}")
            return None, None
    
    def get_example_messages(self) -> list[str]:
        """
        Get a list of example messages for testing.
        
        Returns:
            List of example Spanish financial messages
        """
        return [
            # Transacciones operativas
            "Gasté 50 mil en comida",
            "Recibí 100 mil de salario",
            "Presupuesto de 300 mil para transporte",
            "Pagué 15000 en Uber",
            "Ingreso de 250k por freelance",
            "Compré ropa por 80 mil",
            "Gast $45000 en supermercado",
            "Presupuesto mensual de 1 millón para arriendo",
            # Movimientos de capital
            "Ahorré 100 mil en el banco",
            "Invertí 500 mil en CDT",
            "Guardé 200k en Davivienda",
            "Inversión de 1 millón en acciones",
            "Ahorré 50 mil para emergencias"
        ]

