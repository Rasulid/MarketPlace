import uvicorn
from api.core.config import DB_NAME, DB_PORT, DB_USER, DB_PASS, DB_HOST
import psycopg2

# connection = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
if __name__ == '__main__':
    uvicorn.run("api.main:app", port=8000, reload=True)
