from app import urls
from app.controllers import app
from fastapi.staticfiles import StaticFiles
import uvicorn

#print(app.routes)

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    # コンソールで [$ uvicorn run:app --reload]でも可
    uvicorn.run(app=app)