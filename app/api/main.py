from fastapi import FastAPI
from api.router.amin_router import router as admin_router
from api.router.users_router import router as users_router
from api.auth.admin_auth import router as admin_auth_router
from api.router.product_router import router as product_router
from api.router.order_router import router as order_router

app = FastAPI(title="Admin",
              docs_url="/api/admin/docs")

app.include_router(admin_router)
# app.include_router(users_router)
app.include_router(admin_auth_router)
app.include_router(product_router)
# app.include_router(order_router)

app.mount("/api/users", users_router)
