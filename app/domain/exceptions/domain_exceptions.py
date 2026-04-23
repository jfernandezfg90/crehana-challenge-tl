"""
Excepciones personalizadas del dominio.
Define los errores de lógica de negocio que pueden ocurrir en el sistema.
"""


class TaskListNotFoundException(Exception):
    def __init__(self, task_list_id: str):
        self.task_list_id = task_list_id
        super().__init__(f"Lista de tareas '{task_list_id}' no encontrada")


class TaskNotFoundException(Exception):
    def __init__(self, task_id: str):
        self.task_id = task_id
        super().__init__(f"Tarea '{task_id}' no encontrada")


class UserNotFoundException(Exception):
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Usuario '{identifier}' no encontrado")


class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Ya existe un usuario con el email '{email}'")


class InvalidCredentialsException(Exception):
    def __init__(self):
        super().__init__("Email o contrasena incorrectos")


class UnauthorizedAccessException(Exception):
    def __init__(self, resource: str = "resource"):
        self.resource = resource
        super().__init__(f"Acceso no autorizado a {resource}")


class InvalidTaskStatusTransitionException(Exception):
    def __init__(self, current: str, target: str):
        self.current = current
        self.target = target
        super().__init__(f"Transicion de estado invalida de '{current}' a '{target}'")
