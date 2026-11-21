import logging
from fastapi import status, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("uvicorn.error")

class APPBaseException(Exception):
    def __init__(
            self, 
            message : str = "An Application Error Accured",
            status_code : int = status.HTTP_400_BAD_REQUEST,
            error_code : str = "APP_ERROR"
        ):

        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        

class NotFoundError(APPBaseException):
    def __init__(self, msg:str):
        super().__init__(
            message=msg, 
            status_code= status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND_ERROR"
        )
    

class InvalidCerdiantials(APPBaseException):
    def __init__(self, msg:str):
        super().__init__(
            message=msg, 
            status_code= status.HTTP_400_BAD_REQUEST,
            error_code="INVALID_CERDERNTIALS"
        )

class UnexpectedErrorAccuerd(APPBaseException):
    def __init__(self, msg:str):
        super().__init__(
            message=msg, 
            status_code= status.HTTP_400_BAD_REQUEST,
            error_code="BAD_REQUEST"
        )


class AlreadyExistsError(APPBaseException):
    def __init__(self, msg:str):
        super().__init__(
            message=msg, 
            status_code= status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN"
        )


class OutOfStock(APPBaseException):
    def __init__(self, msg:str):
        super().__init__(
            message=msg, 
            status_code= status.HTTP_409_CONFLICT,
            error_code="OUT_OF_STOCK")

class ProductNotFound(APPBaseException):
    def __init__(self, msg:str):
        super().__init__(
            message=msg, 
            status_code= status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND_ERROR"
        )

class EmptyCart(APPBaseException):
    def __init__(self, msg:str):
        super().__init__(
            message=msg, 
            status_code= status.HTTP_404_NOT_FOUND,
            error_code="EMPTY_CARD"
        )

class PaymentFailed(APPBaseException):
    def __init__(self, msg:str):
        super().__init__(
            message=msg, 
            status_code= status.HTTP_402_PAYMENT_REQUIRED,
            error_code="PAYMENT_FAILED"
        )


def register_exception_handlers(app : FastAPI):
    @app.exception_handler(APPBaseException)
    def custom_app_exception_handler(req : Request, exc : APPBaseException):
        return JSONResponse(
            status_code=exc.status_code,
            content={""
            "sucess" : False,
            "error_code" : exc.error_code,
            "message" : exc.message}
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error_code": f"HTTP_{exc.status_code}", "message": str(exc.detail)},
        )

    @app.exception_handler(RequestValidationError)
    def request_validation_error(req : Request, exc : RequestValidationError):
        clean_errors = [{"field": " -> ".join(str(loc) for loc in err["loc"]), "issue": err["msg"]} for err in exc.errors()]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"success": False, "error_code": "VALIDATION_ERROR", "message": "Invalid request parameters.", "details": clean_errors},
        )

    @app.exception_handler(Exception)
    async def global_fallback_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled server error on {request.method} {request.url}: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "error_code": "INTERNAL_SERVER_ERROR", "message": "An unexpected internal server error occurred."},
        )