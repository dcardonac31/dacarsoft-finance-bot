"""
Test script for Google Sheets service.

Run this to test Google Sheets integration without starting the full bot.
"""

import logging
from datetime import datetime
from services.sheets_service import SheetsService
from domain.transaction import Transaction, TransactionType

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def test_sheets_integration():
    """Test Google Sheets service."""
    
    print("\n" + "="*70)
    print("🧪 TESTING GOOGLE SHEETS INTEGRATION")
    print("="*70 + "\n")
    
    # Initialize service
    sheets_service = SheetsService()
    
    # Test authentication
    print("📝 Step 1: Authenticating with Google Sheets...")
    if not sheets_service.authenticate():
        print("❌ Authentication failed!")
        print("   Please check:")
        print("   - services/credentials.json exists")
        print("   - Credentials file is valid")
        return
    print("✅ Authentication successful!\n")
    
    # Test spreadsheet connection
    print("📝 Step 2: Connecting to spreadsheet...")
    if not sheets_service.connect_spreadsheet():
        print("❌ Connection failed!")
        print("   Please check:")
        print("   - SPREADSHEET_ID in .env is correct")
        print("   - Spreadsheet is shared with service account")
        return
    print(f"✅ Connected to: {sheets_service.spreadsheet.title}\n")
    
    # Test sheet initialization
    print("📝 Step 3: Initializing sheets...")
    if not sheets_service.initialize_sheets():
        print("❌ Initialization failed!")
        return
    print("✅ Sheets initialized successfully!\n")
    
    # Test saving transactions
    print("📝 Step 4: Testing transaction saves...")
    
    test_transactions = [
        Transaction(
            tipo=TransactionType.GASTO,
            monto=50000,
            categoria="comida",
            descripcion="Test: Gasté 50 mil en comida",
            fecha=datetime.now()
        ),
        Transaction(
            tipo=TransactionType.INGRESO,
            monto=100000,
            categoria="salario",
            descripcion="Test: Recibí 100 mil de salario",
            fecha=datetime.now()
        ),
        Transaction(
            tipo=TransactionType.PRESUPUESTO,
            monto=300000,
            categoria="transporte",
            descripcion="Test: Presupuesto de 300 mil para transporte",
            fecha=datetime.now()
        )
    ]
    
    for i, transaction in enumerate(test_transactions, 1):
        print(f"\n   Testing {i}/3: {transaction.tipo.value}...")
        if sheets_service.save_transaction(transaction):
            print(f"   ✅ Saved: {transaction.categoria} - ${transaction.monto:,.2f}")
        else:
            print(f"   ❌ Failed to save transaction")
    
    print("\n📝 Step 5: Retrieving transactions...")
    all_transactions = sheets_service.get_transactions()
    print(f"✅ Found {len(all_transactions)} total transactions\n")
    
    print("="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
    print("\n📊 Check your Google Spreadsheet to see the test data!")
    print("   Note: You may want to delete the test rows manually.\n")


def main():
    """Main entry point."""
    try:
        test_sheets_integration()
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        logger.error(f"Testing failed: {e}", exc_info=True)


if __name__ == "__main__":
    main()

