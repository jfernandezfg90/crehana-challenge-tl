"""
Objetos de valor para el estado de las tareas.
Define el ciclo de vida de una tarea (PENDING, IN_PROGRESS, DONE).
"""

from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
