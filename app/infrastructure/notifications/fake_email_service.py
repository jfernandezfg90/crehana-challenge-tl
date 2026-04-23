"""
Servicio de notificación simulado (Mock).
Implementa NotificationService registrando envíos en los logs.
"""

import logging

from app.application.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class FakeEmailService(NotificationService):
    def send_assignment_notification(self, user_email: str, task_title: str) -> None:
        logger.info(
            "[EMAIL SIMULADO] Email enviado a '%s' para la tarea '%s'",
            user_email,
            task_title,
        )
