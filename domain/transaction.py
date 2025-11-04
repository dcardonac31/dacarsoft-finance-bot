"""
Transaction domain model.

Represents a financial transaction (expense, income, or budget).
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TransactionType(str, Enum):
    """Types of financial transactions."""
    GASTO = "gasto"  # Expense
    INGRESO = "ingreso"  # Income
    PRESUPUESTO = "presupuesto"  # Budget
    AHORRO = "ahorro"  # Savings
    INVERSION = "inversion"  # Investment


class Transaction(BaseModel):
    """
    Represents a financial transaction.
    
    Attributes:
        tipo: Type of transaction (gasto, ingreso, presupuesto)
        monto: Amount in the transaction
        categoria: Category of the transaction (e.g., comida, transporte, salario)
        descripcion: Description or notes about the transaction
        fecha: Date and time of the transaction (ISO format)
    """
    tipo: TransactionType = Field(..., description="Type of transaction")
    monto: float = Field(..., gt=0, description="Amount (must be positive)")
    categoria: str = Field(..., min_length=1, description="Transaction category")
    descripcion: Optional[str] = Field(None, description="Optional description")
    fecha: datetime = Field(default_factory=datetime.now, description="Transaction date")
    
    @field_validator('categoria')
    @classmethod
    def normalize_categoria(cls, v: str) -> str:
        """Normalize category to lowercase and trim whitespace."""
        return v.lower().strip()
    
    @field_validator('monto')
    @classmethod
    def validate_monto(cls, v: float) -> float:
        """Ensure amount is positive and has at most 2 decimal places."""
        if v <= 0:
            raise ValueError("Amount must be positive")
        return round(v, 2)
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary format."""
        return {
            "tipo": self.tipo.value,
            "monto": self.monto,
            "categoria": self.categoria,
            "descripcion": self.descripcion or "",
            "fecha": self.fecha.isoformat()
        }
    
    def is_income(self) -> bool:
        """
        Check if transaction is an income.
        
        Returns:
            True if income, False if expense
        """
        return self.tipo == TransactionType.INGRESO
    
    def to_sheets_row(self) -> list:
        """
        Convert transaction to a row format for Google Sheets.
        
        New structure with unified Transacciones sheet:
        - Fecha, Monto, Categoría, Descripción, Es Ingreso
        
        Returns:
            List of values ready to be inserted into Google Sheets
        """
        return [
            self.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            self.monto,
            self.categoria,
            self.descripcion or "",
            self.is_income()  # Boolean: TRUE for income, FALSE for expense
        ]
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        use_enum_values = True

