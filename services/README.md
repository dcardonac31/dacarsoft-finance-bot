# 🔧 Services Module

This folder contains external service integrations and configuration management.

## 📁 Files

### `config.py`
**Configuration Management**
- Loads environment variables from `.env`
- Uses Pydantic Settings for validation
- Provides centralized access to configuration

```python
from services.config import settings

print(settings.BOT_TOKEN)
print(settings.SPREADSHEET_ID)
```

### `llm_service.py`
**Natural Language Processing**
- OpenAI GPT integration
- Parses Spanish financial messages
- Converts text to structured Transaction objects

```python
from services.llm_service import LLMService

llm = LLMService()
transaction = await llm.parse_message("Gasté 50 mil en comida")
```

### `sheets_service.py`
**Google Sheets Integration**
- Authenticates with service account
- Creates and manages sheets
- Saves and retrieves transactions

```python
from services.sheets_service import SheetsService

sheets = SheetsService()
sheets.authenticate()
sheets.connect_spreadsheet()
sheets.save_transaction(transaction)
```

## 🔑 Required Files

### `credentials.json`
**⚠️ IMPORTANT: This file is NOT included in the repository for security reasons.**

You need to create this file yourself by following these steps:

#### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one

#### Step 2: Enable APIs
1. Navigate to "APIs & Services" > "Library"
2. Enable:
   - Google Sheets API
   - Google Drive API

#### Step 3: Create Service Account
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the details:
   - Name: `dacarsoft-finance-bot`
   - Role: `Editor`
4. Click "Done"

#### Step 4: Generate Key
1. Click on the service account you just created
2. Go to the "Keys" tab
3. Click "Add Key" > "Create new key"
4. Select "JSON" format
5. Click "Create"

#### Step 5: Save the File
1. A JSON file will be downloaded
2. Rename it to `credentials.json`
3. Place it in this `services/` folder
4. The final path should be: `services/credentials.json`

### File Structure
The `credentials.json` file will look like this:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "xxxxx",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "xxxxx",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "xxxxx"
}
```

## 🔒 Security

### .gitignore
The `credentials.json` file is included in `.gitignore` to prevent accidental commits:

```gitignore
# Google Sheets credentials
services/credentials.json
services/token.json
```

### Best Practices
1. ✅ **Never commit** `credentials.json` to Git
2. ✅ **Never share** the service account key publicly
3. ✅ **Rotate keys** periodically for security
4. ✅ **Use different keys** for development and production
5. ✅ **Restrict permissions** to only what's needed

## 📊 Google Sheets Setup

After creating the credentials:

### Step 1: Create Spreadsheet
1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it (e.g., "Finanzas DacarSoft")

### Step 2: Get Spreadsheet ID
Copy the ID from the URL:
```
https://docs.google.com/spreadsheets/d/[THIS_IS_THE_ID]/edit
```

### Step 3: Share with Service Account
1. Open your `credentials.json` file
2. Find the `client_email` field
3. Copy that email address
4. Share your spreadsheet with that email (Editor permissions)

### Step 4: Configure Environment
Add the spreadsheet ID to your `.env` file:
```
SPREADSHEET_ID="your_spreadsheet_id_here"
```

## 🧪 Testing Services

### Test Google Sheets Connection
```bash
python test_sheets.py
```

This will:
- ✅ Authenticate with Google
- ✅ Connect to your spreadsheet
- ✅ Create necessary sheets (Gastos, Ingresos, Presupuestos)
- ✅ Insert test transactions

### Test LLM Parsing
```bash
python test_llm.py
```

This will:
- ✅ Test various Spanish messages
- ✅ Show parsed results
- ✅ Validate Transaction objects

## 🔧 Configuration

### Environment Variables

All services use environment variables from `.env`:

```env
# Telegram
BOT_TOKEN="your_telegram_token"
BOT_NAME="Dacarsoft Asistente Financiero Bot"
BOT_USERNAME="DacarsoftFinanceBot"

# Google Sheets
SHEETS_CREDENTIALS_FILE="services/credentials.json"
SPREADSHEET_ID="your_spreadsheet_id"

# OpenAI
OPENAI_API_KEY="your_openai_key"

# Application
TIMEZONE="America/Bogota"
DEBUG=True
```

### Accessing Configuration

```python
from services.config import settings

# Access any setting
bot_token = settings.BOT_TOKEN
spreadsheet_id = settings.SPREADSHEET_ID
debug_mode = settings.DEBUG

# Get credentials path
creds_path = settings.credentials_path
```

## 📚 Service Usage Examples

### Complete Example

```python
import asyncio
from services.llm_service import LLMService
from services.sheets_service import SheetsService

async def process_message(message: str):
    # Parse message
    llm = LLMService()
    transaction = await llm.parse_message(message)
    
    if transaction:
        # Save to sheets
        sheets = SheetsService()
        sheets.authenticate()
        sheets.connect_spreadsheet()
        success = sheets.save_transaction(transaction)
        
        if success:
            print(f"✅ Saved: {transaction}")
        else:
            print("❌ Failed to save")
    else:
        print("❌ Failed to parse")

# Run
asyncio.run(process_message("Gasté 50 mil en comida"))
```

## 🆘 Troubleshooting

### Error: "credentials.json not found"
**Solution**: Create the file following the steps above.

### Error: "Permission denied" (Google Sheets)
**Solution**: Share the spreadsheet with the service account email.

### Error: "Invalid API key" (OpenAI)
**Solution**: Verify your `OPENAI_API_KEY` in `.env`

### Error: "Quota exceeded" (Google)
**Solution**: Check your quotas in Google Cloud Console.

## 📖 API Documentation

### LLMService

```python
class LLMService:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with optional API key."""
        
    async def parse_message(self, message: str) -> Optional[Transaction]:
        """
        Parse a Spanish financial message.
        
        Args:
            message: Natural language message
            
        Returns:
            Transaction object or None if parsing fails
        """
        
    def get_example_messages(self) -> list[str]:
        """Get list of example messages for testing."""
```

### SheetsService

```python
class SheetsService:
    def __init__(self, credentials_file: Optional[str] = None, 
                 spreadsheet_id: Optional[str] = None):
        """Initialize with optional credentials and spreadsheet ID."""
        
    def authenticate(self) -> bool:
        """Authenticate with Google Sheets API."""
        
    def connect_spreadsheet(self) -> bool:
        """Connect to the configured spreadsheet."""
        
    def initialize_sheets(self) -> bool:
        """Create required sheets if they don't exist."""
        
    def save_transaction(self, transaction: Transaction) -> bool:
        """Save a transaction to the appropriate sheet."""
        
    def get_transactions(self, 
                        transaction_type: Optional[TransactionType] = None
                        ) -> List[List]:
        """Retrieve transactions from sheets."""
```

## 🎓 Learning Resources

- [Google Sheets API Python Quickstart](https://developers.google.com/sheets/api/quickstart/python)
- [OpenAI Python Library](https://github.com/openai/openai-python)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)

## 📝 Notes

- The bot automatically creates three sheets: "Gastos", "Ingresos", "Presupuestos"
- Each sheet gets headers automatically
- Transactions are appended in real-time
- All timestamps use the configured timezone
- LLM parsing uses GPT-4o-mini for cost efficiency

---

Need help? Check the main [README.md](../README.md) or visit [DacarSoft on YouTube](https://youtube.com/@DacarSoft)! 📺

