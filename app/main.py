from fastapi import FastAPI
from app.config import Config
from app.email_file import router
from aiopg.sa import create_engine
import uvicorn


config = Config()
app = FastAPI(title='email_microservices')
app.include_router(router)


# @app.on_event("startup")
# async def startup():
#     app.state.db = await create_engine(connection)


# @app.on_event("shutdown")
# async def shutdown():
#     app.state.db.close()


if __name__ == '__main__':
    uvicorn.run(app, host=config.host_url, port=config.host_port)