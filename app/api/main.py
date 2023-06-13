from fastapi import FastAPI
from api.router.amin_U import router as create_admin

app = FastAPI(title="Admin",
              docs_url="/api/admin")

app.include_router(create_admin)


