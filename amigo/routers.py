from .user import router as user_router
from .appointments import router as appointments_router
from .billing import router as billing_router


def include_routers(app):
    app.include_router(user_router)
    app.include_router(appointments_router)
    app.include_router(billing_router)
