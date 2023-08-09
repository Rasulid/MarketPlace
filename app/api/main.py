from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.router.amin_router import router as admin_router
from api.router.users_router import router as users_router
from api.auth.admin_auth import router as admin_auth_router
from api.router.product_router import router as product_router
from api.router.order_router import router as order_router
from api.creat_superuser import router as super_user_router
from api.router.category_router import router as category_router
from api.router.colour_router import router as colour_router
from api.router.promocode_router import router as promocode_router
from fastapi.middleware.cors import CORSMiddleware
from api.router.admin.api import app as admin
from api.router.site.api import app as site

app = FastAPI()

app.include_router(admin_router)
app.include_router(admin_auth_router)
app.include_router(product_router)
app.include_router(promocode_router)
app.include_router(order_router)
app.include_router(category_router)
app.include_router(colour_router)
app.include_router(users_router)


app.mount("/super-user", super_user_router)
app.mount('/static/image', StaticFiles(directory="static/image"), name="media")
app.mount('/admin', admin)
app.mount('/site', site)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://market-place-site.vercel.app/,*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all headers
)
