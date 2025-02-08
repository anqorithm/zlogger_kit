# ZLogger Kit

<p align="center">
  <img src="assets/zlogger-logo.svg" alt="ZLoggerKit Logo" width="400"/>
</p>

[![Downloads](https://img.shields.io/pypi/dm/zlogger-kit)](https://pypi.org/project/zlogger-kit/)
[![PyPI version](https://img.shields.io/pypi/v/zlogger-kit)](https://img.shields.io/pypi/v/zlogger-kit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![ZLogger Kit](https://img.shields.io/badge/ZLogger_Kit-0.0.1-blue)
![Python](https://img.shields.io/badge/Python->=3.11,<4.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI->=0.109.0,<0.115.8-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/Tests-Pytest-green)](https://docs.pytest.org/)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)](https://coverage.py/)

ZLogger Kit is a well-rounded logging kit around structlog. It provides middleware for logging requests and responses, as well as a logger for logging messages, with priority levels for each log level: [WARNING, INFO, DEBUG, ERROR].

## Features

- **Logging requests and responses** for all `requests` and `responses`
- **Support Timezone** with the ability to set the timezone, default is `Asia/Riyadh`
- **Logging messages** with priority levels (`P10`, `P20`, `P30`, `P40`)
- **Logging errors, warnings, info, and debug**
- **Logging to file** with the ability to set the log `file path` and `file name`
- **Logging to console** with the ability to set the log `level`
- **Logging with 2 different log formats**
    - **JSON**
    - **TEXT**
- **Easy to use and setup**


## Priority Levels

| Level   | Description                     | Priority |
|---------|---------------------------------|----------|
| DEBUG   | Debug level logging with lowest priority. | P10      |
| INFO    | Informational level logging with low-medium priority. | P20      |
| WARNING | Warning level logging with medium-high priority. | P30      |
| ERROR   | Error level logging with highest priority. | P40      |

## Installation

### Poetry (Recommended)

```bash
poetry add zlogger-kit
```

### Pip

```bash
pip install zlogger-kit
```

## Quick Start

#### Example 1

In this example, we will use the `ZLog` class to log messages to the console and file, with the JSON & TEXT formats and the `AUTH` module.


```python
from zlogger_kit.zlog import ZLog
from zlogger_kit.models import ZLogConfig
from examples.modules import Module

config = ZLogConfig(
    module=Module.AUTH.value,
    json_format=True,
    log_path="logs/auth",
)
logger = ZLog.init(config)

logger.info("Starting authentication process", client_ip="192.168.1.100")
logger.info("Login successful", user_id="user_123")
logger.error(
    "Login failed",
    username="suspicious_user",
    ip="10.0.0.5",
    reason="Invalid credentials",
)
logger.warn(
    "Failed login attempt",
    username="suspicious_user",
    ip="10.0.0.5",
    reason="Invalid credentials",
)
logger.debug("Debug message", user_id="user_123")
logger.warn(
    "Failed login attempt",
    username="suspicious_user",
    ip="10.0.0.5",
    reason="Invalid credentials",
)
```

#### JSON Format

```json
{"timestamp": "2025-02-09T00:25:39.953773+03:00", "module": "AUTH", "priority": "P20", "message": "Starting authentication process", "level": "INFO", "client_ip": "192.168.1.100"}
{"timestamp": "2025-02-09T00:25:39.954158+03:00", "module": "AUTH", "priority": "P20", "message": "Login successful", "level": "INFO", "user_id": "user_123"}
{"timestamp": "2025-02-09T00:25:39.954199+03:00", "module": "AUTH", "priority": "P40", "message": "Login failed", "level": "ERROR", "username": "suspicious_user", "ip": "10.0.0.5", "reason": "Invalid credentials"}
{"timestamp": "2025-02-09T00:25:39.954224+03:00", "module": "AUTH", "priority": "P30", "message": "Failed login attempt", "level": "WARNING", "username": "suspicious_user", "ip": "10.0.0.5", "reason": "Invalid credentials"}
{"timestamp": "2025-02-09T00:25:39.954260+03:00", "module": "AUTH", "priority": "P10", "message": "Debug message", "level": "DEBUG", "user_id": "user_123"}
{"timestamp": "2025-02-09T00:25:39.954293+03:00", "module": "AUTH", "priority": "P30", "message": "Failed login attempt", "level": "WARNING", "username": "suspicious_user", "ip": "10.0.0.5", "reason": "Invalid credentials"}
```

```python
config = ZLogConfig(
    module=Module.AUTH.value,
    json_format=False,
    log_path="logs/auth",
)
```

#### TEXT Format

```json
[INFO]:[P20] [2025-02-09T00:27:14.375037+03:00] Starting authentication process {"level": "INFO", "client_ip": "192.168.1.100"}
[INFO]:[P20] [2025-02-09T00:27:14.375318+03:00] Login successful {"level": "INFO", "user_id": "user_123"}
[ERROR]:[P40] [2025-02-09T00:27:14.375380+03:00] Login failed {"level": "ERROR", "username": "suspicious_user", "ip": "10.0.0.5", "reason": "Invalid credentials"}
[WARNING]:[P30] [2025-02-09T00:27:14.375410+03:00] Failed login attempt {"level": "WARNING", "username": "suspicious_user", "ip": "10.0.0.5", "reason": "Invalid credentials"}
[DEBUG]:[P10] [2025-02-09T00:27:14.375453+03:00] Debug message {"level": "DEBUG", "user_id": "user_123"}
[WARNING]:[P30] [2025-02-09T00:27:14.375493+03:00] Failed login attempt {"level": "WARNING", "username": "suspicious_user", "ip": "10.0.0.5", "reason": "Invalid credentials"}
```


#### Example 2

In this example, we will use the `ZLogMiddleware` class to log requests and responses, with the JSON format and the `PAYMENT` module.

#### example2.py
```python
from fastapi import FastAPI
from examples.modules import Module
from zlogger_kit.middleware import ZLogMiddleware
from zlogger_kit.zlog import ZLog
from zlogger_kit.models import ZLogConfig
from examples.routers.payment_router import router as payment_router

app = FastAPI(title="Payment Service", description="API for payment processing")

zlogger = ZLog.init(
    ZLogConfig(
        module=Module.PAYMENT.value,
        log_path="logs",
        time_zone="Asia/Riyadh",
        json_format=False,
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
```

#### routers/payment_router.py
```python
from fastapi import APIRouter, HTTPException
from examples.modules import Module
from zlogger_kit.models import ZLogConfig
from zlogger_kit.zlog import ZLog

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
    responses={404: {"description": "Not found"}},
)

logger = ZLog.init(
    ZLogConfig(
        module=Module.PAYMENT.value, log_path="logs", time_zone="UTC", json_format=False
    )
)


@router.post("")
async def create_payment():
    """Create a new payment"""
    try:
        return {"payment_id": "pay_123", "status": "succeeded", "amount": 1000}
    except Exception as e:
        logger.error(f"Payment failed: {str(e)}")
        raise HTTPException(status_code=400, detail="Payment failed")


@router.get("/{payment_id}")
async def get_payment(payment_id: str):
    """Get payment details by ID"""
    return {
        "payment_id": payment_id,
        "status": "succeeded",
        "amount": 1000,
        "created_at": "2024-03-20T10:00:00Z",
    }


@router.post("/{payment_id}/refund")
async def refund_payment(payment_id: str):
    """Refund a payment"""
    try:
        return {
            "refund_id": "ref_123",
            "payment_id": payment_id,
            "status": "succeeded",
            "amount": 1000,
        }
    except Exception as e:
        logger.error(f"Refund failed: {str(e)}")
        raise HTTPException(status_code=400, detail="Refund failed")
```


#### Run the example

```bash
poetry run uvicorn examples.example2:app --reload
```

#### logs/payment-2025-02-08.log
```json
[INFO]:[P20] [2025-02-08T21:01:35.591221+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:35.592402+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:40.856986+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:40.857824+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:41.037139+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:41.037928+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:41.246457+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:41.248872+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:41.404536+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:41.406234+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:41.645548+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:41.646162+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:41.856706+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:41.857794+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:42.054642+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:42.056361+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:42.251813+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:42.252793+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:42.459729+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:42.461131+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:42.676245+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:42.676921+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:47.542951+00:00] GET http://127.0.0.1:8000/payments/x {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/payments/x", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:47.545053+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:47.927676+00:00] GET http://127.0.0.1:8000/payments/x {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/payments/x", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:47.929678+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:48.070223+00:00] GET http://127.0.0.1:8000/payments/x {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/payments/x", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:48.071336+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:48.241849+00:00] GET http://127.0.0.1:8000/payments/x {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/payments/x", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:48.243180+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:48.523776+00:00] GET http://127.0.0.1:8000/payments/x {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/payments/x", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:48.526742+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:48.610995+00:00] GET http://127.0.0.1:8000/payments/x {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/payments/x", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:48.611653+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:05:52.487501+00:00] GET http://127.0.0.1:8000/ {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:05:52.490832+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:05:53.274430+00:00] GET http://127.0.0.1:8000/ {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:05:53.275630+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:20.180720+00:00] GET http://127.0.0.1:8000/ {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:20.181940+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:20.604669+00:00] GET http://127.0.0.1:8000/ {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:20.607153+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:20.823974+00:00] GET http://127.0.0.1:8000/ {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:20.825775+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:21.201352+00:00] GET http://127.0.0.1:8000/ {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:21.202818+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:21.484787+00:00] GET http://127.0.0.1:8000/ {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:21.486668+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:54.681627+00:00] GET http://127.0.0.1:8000/ {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:54.684434+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:55.071603+00:00] GET http://127.0.0.1:8000/ {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:55.072919+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:55.285652+00:00] GET http://127.0.0.1:8000/ {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:55.287813+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:55.486956+00:00] GET http://127.0.0.1:8000/ {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:55.488290+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:55.820560+00:00] GET http://127.0.0.1:8000/ {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:06:55.821623+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:33.635075+00:00] GET http://127.0.0.1:8000/docs {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/docs", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:33.636704+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:34.422301+00:00] GET http://127.0.0.1:8000/openapi.json {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/openapi.json", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:34.433079+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:38.733771+00:00] GET http://127.0.0.1:8000/payments/xx {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/payments/xx", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:38.734675+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:38.987348+00:00] GET http://127.0.0.1:8000/payments/xx {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/payments/xx", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:38.989115+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:39.229833+00:00] GET http://127.0.0.1:8000/payments/xx {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/payments/xx", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:39.233149+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:45.905579+00:00] POST http://127.0.0.1:8000/payments/xxx/refund {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/xxx/refund", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:45.906401+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:46.278236+00:00] POST http://127.0.0.1:8000/payments/xxx/refund {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/xxx/refund", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:46.279239+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:46.428104+00:00] POST http://127.0.0.1:8000/payments/xxx/refund {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/xxx/refund", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:46.429115+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:46.652729+00:00] POST http://127.0.0.1:8000/payments/xxx/refund {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/xxx/refund", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:46.654283+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:46.842222+00:00] POST http://127.0.0.1:8000/payments/xxx/refund {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/xxx/refund", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:46.843769+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:47.006513+00:00] POST http://127.0.0.1:8000/payments/xxx/refund {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/xxx/refund", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:47.007901+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:47.199977+00:00] POST http://127.0.0.1:8000/payments/xxx/refund {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/xxx/refund", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:47.201612+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:47.315819+00:00] POST http://127.0.0.1:8000/payments/xxx/refund {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/xxx/refund", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:47.316780+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:47.471488+00:00] POST http://127.0.0.1:8000/payments/xxx/refund {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/xxx/refund", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:47.473025+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:56.189940+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:56.191389+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:56.576386+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:56.577287+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:56.688954+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:07:56.689819+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}

```

## Contributing

Contributions are welcome! Please feel free to submit a PR.


## Contributors

- [Abdullah Alqahtani](https://github.com/anqorithm)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.