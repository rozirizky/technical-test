from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.exception import global_exception_handler, http_exception_handler
from fastapi import HTTPException
import httpx
import os

app = FastAPI(title="API Gateway - Peminjaman Kendaraan")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USER_SVC    = os.getenv("USER_SERVICE_URL",        "http://user-service:8000")
VEHICLE_SVC = os.getenv("VEHICLE_SERVICE_URL",     "http://vehicle-service:8000")
BOOKING_SVC = os.getenv("BOOKING_SERVICE_URL",     "http://booking-service:8000")
OPS_SVC     = os.getenv("OPERATIONAL_SERVICE_URL", "http://operational-service:8000")

SERVICES: dict[str, str] = {
    "/users":               USER_SVC,
    "/role":                USER_SVC,
    "/location":            USER_SVC,
    "/api":                 USER_SVC,
    "/bookings":            BOOKING_SVC,
    "/fuel-logs":           OPS_SVC,
    "/service-schedules":   OPS_SVC,
    "/service-histories":   OPS_SVC,
    "/usage-logs":          OPS_SVC,
    "/vehicles":            VEHICLE_SVC,
    "/drivers":             VEHICLE_SVC,
}


def _resolve(path: str) -> str | None:
    prefix = "/" + path.split("/")[0]
    return SERVICES.get(prefix)


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    include_in_schema=False,
)
async def gateway(path: str, request: Request):
    base_url = _resolve(path)

    if not base_url:
        raise HTTPException(
            status_code=404,
            detail=f"No service registered for /{path.split('/')[0]}"
        )

    target_url = f"{base_url}/{path}"
    if request.query_params:
        target_url += f"?{request.query_params}"

    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ("host", "content-length")
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=await request.body(),
            )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            media_type=resp.headers.get("content-type", "application/json"),
        )
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {base_url}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail=f"Service timeout: {base_url}")


@app.get("/", tags=["gateway"])
async def root():
    return {"message": "API Gateway aktif", "services": list(SERVICES.keys())}


@app.get("/health", tags=["gateway"])
async def health():
    results = {}
    async with httpx.AsyncClient(timeout=5.0) as client:
        seen = set()
        for prefix, base_url in SERVICES.items():
            if base_url in seen:
                continue
            seen.add(base_url)
            try:
                resp = await client.get(f"{base_url}/")
                results[base_url] = {"status": "up", "code": resp.status_code}
            except Exception as e:
                results[base_url] = {"status": "down", "error": str(e)}
    return results


app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
