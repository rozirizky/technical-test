from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from fastapi import HTTPException


async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "detail": str(exc)
        }
    )
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP error {exc.status_code}: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail
        }
    )