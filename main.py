from fastapi import FastAPI
from app.routers import auth_router, customer_router, warehouse_router, product_router
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions import register_exception_handlers, APPBaseException

app = FastAPI(debug=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all frontend origins
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

register_exception_handlers(app)






app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(warehouse_router)
app.include_router(product_router)


