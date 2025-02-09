from fastapi import FastAPI
from examples.modules import Module
from zlogger_kit import ZLogMiddleware, ZLog, ZLogConfig
from examples.routers.payment_router import router as payment_router

app = FastAPI(title="Payment Service", description="API for payment processing")

zlogger = ZLog.init(
    ZLogConfig(
        module=Module.PAYMENT.value,
        log_path="logs",
        time_zone="Asia/Riyadh",
        json_format=True,
    )
)

app.add_middleware(ZLogMiddleware, logger=zlogger)

app.include_router(payment_router)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {"message": "Welcome to the Payment Service API 💸"}
