# Nos ayudamos de starlette que ya viene en fastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

class ErrorHandler(BaseHTTPMiddleware):
    ## Crear un método constructor
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        
    # Método que se ejecutará cuando haya un error en la app
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
    