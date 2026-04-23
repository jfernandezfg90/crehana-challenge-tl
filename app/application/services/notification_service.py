"""
Interfaz del Servicio de Notificaciones.
Contrato para el envío de avisos desacoplado del proveedor.
"""

from abc import ABC, abstractmethod


class NotificationService(ABC):
    @abstractmethod
    def send_assignment_notification(self, user_email: str, task_title: str) -> None:
        pass
