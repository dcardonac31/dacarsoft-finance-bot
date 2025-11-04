"""
Capital movement domain model.

Represents savings and investments (capital movements).
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class CapitalType(str, Enum):
    """Types of capital movements."""
    AHORRO = "ahorro"  # Savings
    INVERSION = "inversion"  # Investment


class CapitalStatus(str, Enum):
    """Status of capital movement."""
    ACTIVO = "activo"  # Active/Current
    RETIRADO = "retirado"  # Withdrawn


class CapitalMovement(BaseModel):
    """
    Represents a capital movement (savings or investment).
    
    This is separate from operational transactions (expenses/income)
    to track where your money is stored/invested.
    
    Attributes:
        tipo: Type of capital movement (ahorro, inversion)
        monto: Initial amount deposited
        institucion: Where the money is (bank, CDT, stocks, etc.)
        estado: Current status (activo, retirado)
        fecha: Date when money was deposited
        fecha_retiro: Date when money was withdrawn (optional)
        retorno: Total returns/interest earned (optional)
        descripcion: Additional notes
    """
    tipo: CapitalType = Field(..., description="Type of capital movement")
    monto: float = Field(..., gt=0, description="Initial amount deposited (must be positive)")
    institucion: str = Field(..., min_length=1, description="Where the money is stored/invested")
    estado: CapitalStatus = Field(default=CapitalStatus.ACTIVO, description="Current status")
    fecha: datetime = Field(default_factory=datetime.now, description="Deposit date")
    fecha_retiro: Optional[datetime] = Field(None, description="Withdrawal date")
    retorno: float = Field(default=0.0, ge=0, description="Total returns/interest earned")
    descripcion: Optional[str] = Field(None, description="Additional notes")
    
    @field_validator('institucion')
    @classmethod
    def normalize_institucion(cls, v: str) -> str:
        """Normalize institution to lowercase and trim whitespace."""
        return v.lower().strip()
    
    @field_validator('monto', 'retorno')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        """Ensure amount has at most 2 decimal places."""
        return round(v, 2)
    
    def get_current_value(self) -> float:
        """
        Calculate current value (principal + returns).
        
        Returns:
            Total current value
        """
        return self.monto + self.retorno
    
    def is_active(self) -> bool:
        """
        Check if this capital movement is currently active.
        
        Returns:
            True if active, False if withdrawn
        """
        return self.estado == CapitalStatus.ACTIVO
    
    def withdraw(self, fecha_retiro: Optional[datetime] = None) -> None:
        """
        Mark this capital movement as withdrawn.
        
        Args:
            fecha_retiro: Withdrawal date (defaults to now)
        """
        self.estado = CapitalStatus.RETIRADO
        self.fecha_retiro = fecha_retiro or datetime.now()
    
    def add_return(self, amount: float) -> None:
        """
        Add returns/interest to this capital movement.
        
        Args:
            amount: Return amount to add
        """
        if amount > 0:
            self.retorno += round(amount, 2)
    
    def to_dict(self) -> dict:
        """Convert capital movement to dictionary format."""
        return {
            "tipo": self.tipo.value,
            "monto": self.monto,
            "institucion": self.institucion,
            "estado": self.estado.value,
            "fecha": self.fecha.isoformat(),
            "fecha_retiro": self.fecha_retiro.isoformat() if self.fecha_retiro else None,
            "retorno": self.retorno,
            "descripcion": self.descripcion or ""
        }
    
    def to_sheets_row(self) -> list:
        """
        Convert capital movement to a row format for Google Sheets.
        
        Format: Fecha, Tipo, Monto, Institución, Estado, Fecha Retiro, Retorno, Descripción
        
        Returns:
            List of values ready to be inserted into Google Sheets
        """
        return [
            self.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            self.tipo.value,
            self.monto,
            self.institucion,
            self.estado.value,
            self.fecha_retiro.strftime("%Y-%m-%d %H:%M:%S") if self.fecha_retiro else "",
            self.retorno,
            self.descripcion or ""
        ]
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        use_enum_values = True

