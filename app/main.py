from fastapi import FastAPI
from routers import predict,auth,user
import uvicorn
from databases.database import engine
from databases import models, crud
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["http://myproject.local:3000"]
app.middleware(
    app.add_middleware( 
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
)

app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(user.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/storage", StaticFiles(directory="app/storage"),name="storage")
if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, log_level="info", reload=True)   