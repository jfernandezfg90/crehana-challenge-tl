"""
Objetos de valor para la prioridad de las tareas.
Define los niveles de urgencia permitidos en el sistema.
"""

from enum import Enum


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
