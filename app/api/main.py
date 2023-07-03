from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.router.amin_router import router as admin_router
from api.router.users_router import router as users_router
from api.auth.admin_auth import router as admin_auth_router
from api.router.product_router import router as product_router
from api.router.order_router import router as order_router
from api.creat_superuser import router as super_user_router

app = FastAPI(title="Admin",
              docs_url="/api/admin/docs")

app.include_router(admin_router)
app.include_router(admin_auth_router)
app.include_router(product_router)
app.include_router(order_router)

app.mount("/api/users", users_router)
app.mount("/api/super-user", super_user_router)
app.mount('/media', StaticFiles(directory="static/image"), name="media")
