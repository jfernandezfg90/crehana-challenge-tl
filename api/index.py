"""
Punto de entrada para el despliegue en Vercel.
Importa la instancia de la aplicación FastAPI para que el runtime de Vercel pueda ejecutarla como una función serverless.
"""

from app.main import app  # noqa: F401 — Vercel uses this ASGI app object
