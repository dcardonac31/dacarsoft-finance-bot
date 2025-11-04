"""
Domain models and entities for the financial bot.

This module contains the core business entities used throughout the application.
"""

from .transaction import Transaction, TransactionType
from .capital import CapitalMovement, CapitalType, CapitalStatus

__all__ = [
    "Transaction",
    "TransactionType",
    "CapitalMovement",
    "CapitalType",
    "CapitalStatus"
]

