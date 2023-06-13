from fastapi import FastAPI
from api.router.amin_router import router as admin_router
from api.router.users_router import router as users_router

app = FastAPI(title="Admin",
              docs_url="/api/admin")

app.include_router(admin_router)
app.include_router(users_router)


