# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al **Dacarsoft Finance Bot**! Este documento te guiará sobre cómo contribuir al proyecto.

## 📋 Código de Conducta

- Sé respetuoso con todos los contribuidores
- Acepta críticas constructivas
- Enfócate en lo que es mejor para la comunidad
- Muestra empatía hacia otros miembros de la comunidad

## 🎯 Cómo Contribuir

### Reportar Bugs

Si encuentras un bug:

1. Verifica que no esté ya reportado en [Issues](https://github.com/dacarsoft/dacarsoft-finance-bot/issues)
2. Abre un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs actual
   - Screenshots si es aplicable
   - Información del entorno (OS, Python version, etc.)

### Proponer Nuevas Funcionalidades

Para proponer nuevas features:

1. Abre un issue con la etiqueta "enhancement"
2. Describe claramente:
   - El problema que resuelve
   - La solución propuesta
   - Alternativas consideradas
   - Impacto en usuarios existentes

### Pull Requests

#### Proceso

1. **Fork el repositorio**
   ```bash
   # Haz fork desde GitHub, luego:
   git clone https://github.com/TU_USUARIO/dacarsoft-finance-bot.git
   cd dacarsoft-finance-bot
   ```

2. **Crea una rama**
   ```bash
   git checkout -b feature/mi-nueva-feature
   # o
   git checkout -b fix/mi-bug-fix
   ```

3. **Instala dependencias de desarrollo**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install black flake8 mypy pytest  # Herramientas de desarrollo
   ```

4. **Haz tus cambios**
   - Sigue las convenciones de código
   - Escribe/actualiza tests
   - Actualiza documentación

5. **Ejecuta tests y linters**
   ```bash
   # Formatear código
   black .
   
   # Verificar estilo
   flake8 .
   
   # Type checking
   mypy .
   
   # Ejecutar tests (cuando estén disponibles)
   pytest
   ```

6. **Commit tus cambios**
   ```bash
   git add .
   git commit -m "feat: descripción clara del cambio"
   ```
   
   Usa conventional commits:
   - `feat:` nueva funcionalidad
   - `fix:` corrección de bug
   - `docs:` cambios en documentación
   - `style:` formateo, sin cambio de código
   - `refactor:` refactorización de código
   - `test:` agregar o modificar tests
   - `chore:` mantenimiento

7. **Push a tu fork**
   ```bash
   git push origin feature/mi-nueva-feature
   ```

8. **Abre un Pull Request**
   - Ve a GitHub y abre un PR
   - Describe claramente los cambios
   - Referencia issues relacionados
   - Espera review

## 🏗️ Estructura del Proyecto

```
dacarsoft-finance-bot/
├── bot/                    # Lógica del bot de Telegram
│   ├── handlers.py         # Manejadores de comandos y mensajes
│   └── bot_instance.py     # Instancia del bot
├── services/               # Servicios externos
│   ├── config.py           # Configuración
│   ├── llm_service.py      # OpenAI integration
│   └── sheets_service.py   # Google Sheets
├── domain/                 # Modelos de dominio
│   └── transaction.py      # Modelo de transacción
├── main.py                 # Entry point
└── tests/                  # Tests (por agregar)
```

## 📝 Convenciones de Código

### Python

1. **PEP 8**: Seguir el estilo de Python
   ```python
   # Bien
   def calculate_total(amount: float, tax: float) -> float:
       return amount * (1 + tax)
   
   # Mal
   def calculateTotal(Amount,Tax):
       return Amount*(1+Tax)
   ```

2. **Type Hints**: Usar anotaciones de tipo
   ```python
   # Bien
   def process_transaction(transaction: Transaction) -> bool:
       pass
   
   # Mal
   def process_transaction(transaction):
       pass
   ```

3. **Docstrings**: Documentar funciones y clases
   ```python
   def parse_message(message: str) -> Optional[Transaction]:
       """
       Parse a natural language message into a Transaction.
       
       Args:
           message: Spanish language financial message
           
       Returns:
           Transaction object if successful, None otherwise
           
       Example:
           >>> parse_message("Gasté 50 mil en comida")
           Transaction(tipo="gasto", monto=50000, ...)
       """
       pass
   ```

4. **Nombres descriptivos**
   ```python
   # Bien
   def save_transaction_to_sheets(transaction: Transaction) -> bool:
       pass
   
   # Mal
   def save(t):
       pass
   ```

5. **Async/Await**: Usar async donde sea apropiado
   ```python
   # Bien
   async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
       transaction = await llm_service.parse_message(message)
   
   # Mal (bloquea el event loop)
   def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
       transaction = llm_service.parse_message_sync(message)
   ```

### Mensajes en Español

Los mensajes del bot deben ser en español, pero el código y comentarios en inglés:

```python
# Good
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    welcome_message = "👋 ¡Hola! Soy Dacarsoft Asistente Financiero Bot."
    await update.message.reply_text(welcome_message)

# Bad
async def comando_inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja el comando /start."""
    mensaje_bienvenida = "👋 Hello! I'm Dacarsoft Finance Bot."
    await update.message.reply_text(mensaje_bienvenida)
```

## 🧪 Testing (To Do)

Actualmente el proyecto no tiene tests automatizados, pero son bienvenidos. Áreas para agregar tests:

1. **Unit tests**:
   - `domain/transaction.py`: Validación de modelos
   - `services/llm_service.py`: Parsing de mensajes
   - `services/sheets_service.py`: Operaciones de sheets (con mocks)

2. **Integration tests**:
   - Bot handlers
   - End-to-end message processing

3. **Herramientas sugeridas**:
   - `pytest` para testing
   - `pytest-asyncio` para tests async
   - `pytest-mock` para mocking

Ejemplo de test:

```python
import pytest
from domain.transaction import Transaction, TransactionType

def test_transaction_creation():
    """Test basic transaction creation."""
    transaction = Transaction(
        tipo=TransactionType.GASTO,
        monto=50000,
        categoria="comida",
        descripcion="Test"
    )
    assert transaction.tipo == TransactionType.GASTO
    assert transaction.monto == 50000.0

def test_transaction_validation():
    """Test transaction validation."""
    with pytest.raises(ValueError):
        Transaction(
            tipo=TransactionType.GASTO,
            monto=-100,  # Invalid: negative amount
            categoria="comida"
        )
```

## 📚 Áreas para Contribuir

### Prioridad Alta

- [ ] Agregar tests automatizados
- [ ] Implementar comando `/stats` con estadísticas reales
- [ ] Agregar soporte para múltiples usuarios/cuentas
- [ ] Mejorar manejo de errores y logging

### Prioridad Media

- [ ] Agregar visualizaciones (gráficos) en el bot
- [ ] Implementar categorías personalizables
- [ ] Agregar soporte para diferentes monedas
- [ ] Crear dashboard web (adicional al bot)

### Prioridad Baja

- [ ] Soporte para imágenes de recibos (OCR)
- [ ] Integración con bancos (open banking)
- [ ] Recordatorios automáticos
- [ ] Export a Excel/PDF

## 🎨 UI/UX

Si trabajas en mensajes del bot:

1. **Emojis**: Úsalos pero con moderación
   ```python
   # Bien
   "✅ Transacción guardada"
   
   # Mal (muy recargado)
   "✅💰📊🎉 Transacción 💵 guardada 🎊✨"
   ```

2. **Claridad**: Mensajes claros y concisos
   ```python
   # Bien
   "❌ No pude entender tu mensaje. Intenta con: 'Gasté 50 mil en comida'"
   
   # Mal
   "Error: parsing failed due to invalid input format"
   ```

3. **Ayuda contextual**: Siempre ofrecer ayuda
   ```python
   "❌ Error al guardar. Usa /help para ver ejemplos."
   ```

## 🐛 Debugging

Para debugging local:

1. Activa el modo DEBUG en `.env`:
   ```
   DEBUG=True
   ```

2. Verifica logs:
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.debug("Debug info")
   logger.info("Info message")
   logger.error("Error occurred", exc_info=True)
   ```

3. Usa los scripts de testing:
   ```bash
   python test_llm.py
   python test_sheets.py
   ```

## 📖 Documentación

Si agregas una nueva funcionalidad, actualiza:

1. **README.md**: Funcionalidad principal
2. **DEPLOYMENT.md**: Si afecta el deployment
3. **setup_guide.md**: Si afecta la configuración
4. **Docstrings**: En el código
5. **Type hints**: Para mejor IDE support

## 🚀 Release Process

Los maintainers manejan los releases:

1. Actualizar versión en `main.py`
2. Actualizar CHANGELOG
3. Crear tag de git
4. Publicar release en GitHub

## 💬 Comunicación

- **Issues**: Para bugs y features
- **Pull Requests**: Para cambios de código
- **Discussions**: Para preguntas generales
- **YouTube**: Para tutoriales → [DacarSoft](https://youtube.com/@DacarSoft)

## 🙏 Reconocimientos

Todos los contribuidores serán reconocidos en:
- README.md (sección de Contributors)
- Notas de release
- Videos del canal (cuando aplique)

## 📄 Licencia

Al contribuir, aceptas que tu código esté bajo la Licencia MIT del proyecto.

---

¡Gracias por contribuir al proyecto! 🎉

Si tienes dudas, no dudes en preguntar en los issues o buscar más información en el canal de YouTube [DacarSoft](https://youtube.com/@DacarSoft).

