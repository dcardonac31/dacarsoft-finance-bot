"""
Google Sheets integration service.

Handles authentication and data persistence to Google Sheets.
"""

import logging
from typing import Optional, List
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError

from domain.transaction import Transaction, TransactionType
from domain.capital import CapitalMovement
from services.config import settings

logger = logging.getLogger(__name__)


class SheetsService:
    """
    Service for interacting with Google Sheets.
    
    Manages authentication and data persistence for financial transactions.
    """
    
    # Google Sheets API scopes
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # Sheet names - Structure with capital movements
    # Gastos e Ingresos → "Transacciones" sheet (operational)
    # Ahorros e Inversiones → "Ahorros e Inversiones" sheet (capital)
    # Presupuestos → "Presupuestos" sheet (budgets)
    TRANSACCIONES_SHEET = "Transacciones"
    CAPITAL_SHEET = "Ahorros e Inversiones"
    PRESUPUESTOS_SHEET = "Presupuestos"
    
    # Header row for Transacciones sheet (gastos e ingresos unificados)
    TRANSACCIONES_HEADER = ["Fecha", "Monto", "Categoría", "Descripción", "Es Ingreso"]
    
    # Header row for Ahorros e Inversiones sheet (capital movements)
    CAPITAL_HEADER = ["Fecha", "Tipo", "Monto", "Institución", "Estado", "Fecha Retiro", "Retorno", "Descripción"]
    
    # Header row for Presupuestos sheet
    PRESUPUESTOS_HEADER = ["Fecha", "Monto", "Categoría", "Descripción"]
    
    def __init__(self, credentials_file: Optional[str] = None, spreadsheet_id: Optional[str] = None):
        """
        Initialize the Sheets service.
        
        Args:
            credentials_file: Path to Google service account credentials JSON file
            spreadsheet_id: Google Sheets spreadsheet ID
        """
        self.credentials_file = credentials_file or settings.SHEETS_CREDENTIALS_FILE
        self.spreadsheet_id = spreadsheet_id or settings.SPREADSHEET_ID
        self.client = None
        self.spreadsheet = None
    
    def authenticate(self) -> bool:
        """
        Authenticate with Google Sheets API.
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            if not Path(self.credentials_file).exists():
                logger.error(f"Credentials file not found: {self.credentials_file}")
                return False
            
            creds = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=self.SCOPES
            )
            
            self.client = gspread.authorize(creds)
            logger.info("Successfully authenticated with Google Sheets")
            return True
            
        except GoogleAuthError as e:
            logger.error(f"Google authentication error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error during authentication: {e}")
            return False
    
    def connect_spreadsheet(self) -> bool:
        """
        Connect to the configured spreadsheet.
        
        Returns:
            True if connection successful, False otherwise
        """
        if not self.client:
            logger.error("Not authenticated. Call authenticate() first.")
            return False
        
        if not self.spreadsheet_id:
            logger.error("No spreadsheet ID configured")
            return False
        
        try:
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            logger.info(f"Connected to spreadsheet: {self.spreadsheet.title}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to spreadsheet: {e}")
            return False
    
    def initialize_sheets(self) -> bool:
        """
        Initialize the spreadsheet with required sheets and headers.
        
        Creates three sheets:
        1. "Transacciones" - Unified sheet for gastos e ingresos (operational flow)
        2. "Ahorros e Inversiones" - Capital movements (savings & investments)
        3. "Presupuestos" - Budgets
        
        Returns:
            True if initialization successful, False otherwise
        """
        if not self.spreadsheet:
            logger.error("Not connected to spreadsheet. Call connect_spreadsheet() first.")
            return False
        
        try:
            existing_sheets = [ws.title for ws in self.spreadsheet.worksheets()]
            
            # Create or verify "Transacciones" sheet (unified gastos + ingresos)
            if self.TRANSACCIONES_SHEET not in existing_sheets:
                worksheet = self.spreadsheet.add_worksheet(
                    title=self.TRANSACCIONES_SHEET,
                    rows=1000,  # More rows since it's unified
                    cols=5
                )
                worksheet.append_row(self.TRANSACCIONES_HEADER)
                logger.info(f"Created sheet: {self.TRANSACCIONES_SHEET}")
            else:
                worksheet = self.spreadsheet.worksheet(self.TRANSACCIONES_SHEET)
                first_row = worksheet.row_values(1)
                if not first_row or first_row != self.TRANSACCIONES_HEADER:
                    worksheet.insert_row(self.TRANSACCIONES_HEADER, 1)
                    logger.info(f"Added header to sheet: {self.TRANSACCIONES_SHEET}")
            
            # Create or verify "Ahorros e Inversiones" sheet (capital movements)
            if self.CAPITAL_SHEET not in existing_sheets:
                worksheet = self.spreadsheet.add_worksheet(
                    title=self.CAPITAL_SHEET,
                    rows=500,
                    cols=8
                )
                worksheet.append_row(self.CAPITAL_HEADER)
                logger.info(f"Created sheet: {self.CAPITAL_SHEET}")
            else:
                worksheet = self.spreadsheet.worksheet(self.CAPITAL_SHEET)
                first_row = worksheet.row_values(1)
                if not first_row or first_row != self.CAPITAL_HEADER:
                    worksheet.insert_row(self.CAPITAL_HEADER, 1)
                    logger.info(f"Added header to sheet: {self.CAPITAL_SHEET}")
            
            # Create or verify "Presupuestos" sheet
            if self.PRESUPUESTOS_SHEET not in existing_sheets:
                worksheet = self.spreadsheet.add_worksheet(
                    title=self.PRESUPUESTOS_SHEET,
                    rows=100,
                    cols=4
                )
                worksheet.append_row(self.PRESUPUESTOS_HEADER)
                logger.info(f"Created sheet: {self.PRESUPUESTOS_SHEET}")
            else:
                worksheet = self.spreadsheet.worksheet(self.PRESUPUESTOS_SHEET)
                first_row = worksheet.row_values(1)
                if not first_row or first_row != self.PRESUPUESTOS_HEADER:
                    worksheet.insert_row(self.PRESUPUESTOS_HEADER, 1)
                    logger.info(f"Added header to sheet: {self.PRESUPUESTOS_SHEET}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error initializing sheets: {e}")
            return False
    
    def save_transaction(self, transaction: Transaction) -> bool:
        """
        Save a transaction to the appropriate sheet.
        
        - Gastos e Ingresos → "Transacciones" sheet (operational flow)
        - Presupuestos → "Presupuestos" sheet
        - Ahorros e Inversiones → Use save_capital_movement() instead
        
        Args:
            transaction: Transaction object to save
            
        Returns:
            True if save successful, False otherwise
        """
        if not self.spreadsheet:
            logger.error("Not connected to spreadsheet")
            return False
        
        try:
            # Determine target sheet based on transaction type
            if transaction.tipo == TransactionType.PRESUPUESTO:
                sheet_name = self.PRESUPUESTOS_SHEET
                # For presupuestos, exclude the "Es Ingreso" column
                row_data = [
                    transaction.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                    transaction.monto,
                    transaction.categoria,
                    transaction.descripcion or ""
                ]
            elif transaction.tipo in [TransactionType.AHORRO, TransactionType.INVERSION]:
                # Capital movements should use save_capital_movement() instead
                logger.warning(f"Transaction tipo {transaction.tipo} should use save_capital_movement()")
                return False
            else:
                # Gastos and Ingresos go to unified "Transacciones" sheet
                sheet_name = self.TRANSACCIONES_SHEET
                row_data = transaction.to_sheets_row()
            
            worksheet = self.spreadsheet.worksheet(sheet_name)
            worksheet.append_row(row_data)
            logger.info(f"Saved transaction to {sheet_name}: {transaction}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving transaction: {e}")
            return False
    
    def save_capital_movement(self, capital: CapitalMovement) -> bool:
        """
        Save a capital movement (ahorro/inversion) to the "Ahorros e Inversiones" sheet.
        
        Args:
            capital: CapitalMovement object to save
            
        Returns:
            True if save successful, False otherwise
        """
        if not self.spreadsheet:
            logger.error("Not connected to spreadsheet")
            return False
        
        try:
            worksheet = self.spreadsheet.worksheet(self.CAPITAL_SHEET)
            row_data = capital.to_sheets_row()
            worksheet.append_row(row_data)
            logger.info(f"Saved capital movement to {self.CAPITAL_SHEET}: {capital}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving capital movement: {e}")
            return False
    
    def get_capital_movements(self, only_active: bool = False) -> List[List]:
        """
        Retrieve capital movements from Google Sheets.
        
        Args:
            only_active: If True, return only active (non-withdrawn) movements
            
        Returns:
            List of capital movement rows
        """
        if not self.spreadsheet:
            logger.error("Not connected to spreadsheet")
            return []
        
        try:
            worksheet = self.spreadsheet.worksheet(self.CAPITAL_SHEET)
            records = worksheet.get_all_values()[1:]  # Skip header
            
            if only_active:
                # Filter by Estado column (index 4): only "activo"
                records = [r for r in records if len(r) > 4 and r[4] == "activo"]
            
            return records
            
        except Exception as e:
            logger.error(f"Error retrieving capital movements: {e}")
            return []
    
    def get_transactions(self, transaction_type: Optional[TransactionType] = None) -> List[List]:
        """
        Retrieve transactions from Google Sheets.
        
        Args:
            transaction_type: Type of transactions to retrieve (None for all)
            
        Returns:
            List of transaction rows
        """
        if not self.spreadsheet:
            logger.error("Not connected to spreadsheet")
            return []
        
        try:
            all_records = []
            
            if transaction_type == TransactionType.PRESUPUESTO:
                # Get only presupuestos
                worksheet = self.spreadsheet.worksheet(self.PRESUPUESTOS_SHEET)
                records = worksheet.get_all_values()[1:]  # Skip header
                return records
            elif transaction_type in [TransactionType.GASTO, TransactionType.INGRESO]:
                # Get from Transacciones sheet and filter by "Es Ingreso" column
                worksheet = self.spreadsheet.worksheet(self.TRANSACCIONES_SHEET)
                records = worksheet.get_all_values()[1:]  # Skip header
                
                # Filter by type: last column (index 4) is "Es Ingreso"
                is_ingreso_filter = transaction_type == TransactionType.INGRESO
                filtered = [r for r in records if len(r) > 4 and r[4] == str(is_ingreso_filter)]
                return filtered
            else:
                # Get all transactions from both sheets
                # Transacciones
                worksheet = self.spreadsheet.worksheet(self.TRANSACCIONES_SHEET)
                all_records.extend(worksheet.get_all_values()[1:])
                
                # Presupuestos
                worksheet = self.spreadsheet.worksheet(self.PRESUPUESTOS_SHEET)
                all_records.extend(worksheet.get_all_values()[1:])
                
                return all_records
                
        except Exception as e:
            logger.error(f"Error retrieving transactions: {e}")
            return []

