from fastapi import FastAPI
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from container import Container
from serve import routers
from serve.infra.database.errors import DBException
from serve.logger import logger
from serve.routers import router


async def db_exception_handler(request: Request, exc: DBException):
    return JSONResponse({"detail": exc.error.message}, status_code=400)


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Internal Error {exc}")
    return JSONResponse({"detail": f"Internal error {exc}"}, status_code=500)


async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.error(f"ValidationError {exc}")
    return JSONResponse(
        {
            "detail": "Validation error : a data is missing or in wrong format.",
            "validation_error_message": str(exc),
        },
        status_code=400,
    )


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[routers])

    init_db(container)
    server = FastAPI()
    server.container = container
    server.include_router(router)
    server.add_exception_handler(DBException, db_exception_handler)
    server.add_exception_handler(ValidationError, validation_exception_handler)
    server.add_exception_handler(Exception, generic_exception_handler)

    return server


def init_db(container):
    db = container.db()
    db.create_database()


app = create_app()


@app.get("/")
def default():
    return {"status": "OK"}
