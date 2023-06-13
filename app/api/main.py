from fastapi import FastAPI

app = FastAPI(title="Admin",
              docs_url="/api/admin")


@app.get("/")
async def root():
    return {"market": "place"}


