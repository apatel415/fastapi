from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import posts, users, auth, votes

# this line was used to create all the tables specified in the models file when code is run
# since we are using alembic to generate the tables, we don't need this anymore
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"] # list of web domains that can access our api; "*" means everyone can access
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
# can do async def if you want an async operation
def root():
    return {"message": "welcome to my api!!"}


        






    