"""
Test script for LLM service.

Run this to test the natural language parsing without starting the full bot.
"""

import asyncio
import logging
from services.llm_service import LLMService

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def test_messages():
    """Test various message formats with the LLM service."""
    
    # Initialize service
    llm_service = LLMService()
    
    # Test messages
    test_cases = [
        "Gasté 50 mil en comida",
        "Recibí 100 mil de salario",
        "Presupuesto de 300 mil para transporte",
        "Pagué 15000 en Uber",
        "Ingreso de 250k por freelance",
        "Compré ropa por 80 mil",
        "Gasté $45000 en supermercado",
        "Presupuesto mensual de 1 millón para arriendo",
        "Recibí pago de 500 mil por proyecto",
        "Gasté 120 mil en gasolina"
    ]
    
    print("\n" + "="*70)
    print("🧪 TESTING LLM SERVICE - Natural Language Parsing")
    print("="*70 + "\n")
    
    for i, message in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {message}")
        print("-" * 70)
        
        try:
            transaction = await llm_service.parse_message(message)
            
            if transaction:
                print(f"✅ Successfully parsed!")
                print(f"   Tipo: {transaction.tipo.value}")
                print(f"   Monto: ${transaction.monto:,.2f}")
                print(f"   Categoría: {transaction.categoria}")
                print(f"   Descripción: {transaction.descripcion}")
                print(f"   Fecha: {transaction.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"❌ Failed to parse message")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "="*70)
    print("✅ Testing completed!")
    print("="*70 + "\n")


def main():
    """Main entry point."""
    try:
        asyncio.run(test_messages())
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        logger.error(f"Testing failed: {e}", exc_info=True)


if __name__ == "__main__":
    main()

