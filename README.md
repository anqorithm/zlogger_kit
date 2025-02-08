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
```


#### Example 2

In this example, we will use the `ZLogMiddleware` class to log requests and responses, with both JSON and TEXT formats for the `PAYMENT` module.

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

#### TEXT Format (logs/payment-2025-02-08.log)
```text
[INFO]:[P20] [2025-02-08T21:01:35.591221+00:00] POST http://127.0.0.1:8000/payments {"level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:35.592402+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:40.856986+00:00] GET http://127.0.0.1:8000/payments/xx {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/payments/xx", "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:40.857824+00:00] 200 {"level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
[INFO]:[P20] [2025-02-08T21:01:41.037139+00:00] GET http://127.0.0.1:8000/health {"level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/health", "ip": "127.0.0.1"}
```

#### JSON Format (logs/payment-2025-02-08.json)
```json
{"timestamp": "2025-02-09T01:26:43.047064+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:43.048061+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:48.822486+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/payments/xx", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/payments/xx", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:48.826271+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:48.971760+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/health", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/health", "ip": "127.0.0.1"}
```


```json
{"timestamp": "2025-02-09T01:26:43.047064+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:43.048061+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:48.822486+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/payments/xx", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/payments/xx", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:48.826271+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:48.971760+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/health", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/health", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:48.972386+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:49.179571+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:49.180813+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:49.325711+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:49.327166+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:52.853706+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/docs", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/docs", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:52.854178+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:53.099283+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/openapi.json", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/openapi.json", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:53.103588+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:55.427086+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:55.427798+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:55.658851+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:55.660167+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:55.828116+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:55.828691+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:56.001061+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:56.001544+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:56.167089+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:56.167591+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:56.321529+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:26:56.322359+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:00.966151+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/payments/x", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/payments/x", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:00.966840+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:06.637737+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments/x/refund", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/x/refund", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:06.638379+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:06.865040+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments/x/refund", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/x/refund", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:06.865722+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:07.021724+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments/x/refund", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/x/refund", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:07.022278+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:07.215648+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments/x/refund", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/x/refund", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:07.217003+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:07.385277+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments/x/refund", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/x/refund", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:07.385928+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:07.537922+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments/x/refund", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/x/refund", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:07.538546+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:07.697902+03:00", "module": "PAYMENT", "priority": "P20", "message": "POST http://127.0.0.1:8000/payments/x/refund", "level": "INFO", "operation": "request", "method": "POST", "url": "http://127.0.0.1:8000/payments/x/refund", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:07.698389+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:13.702432+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/health", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/health", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:13.702826+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:17.311468+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/health", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/health", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:17.311948+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:20.880413+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:20.881079+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:21.115057+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:21.115713+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:21.310658+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:21.311205+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:21.507362+03:00", "module": "PAYMENT", "priority": "P20", "message": "GET http://127.0.0.1:8000/", "level": "INFO", "operation": "request", "method": "GET", "url": "http://127.0.0.1:8000/", "ip": "127.0.0.1"}
{"timestamp": "2025-02-09T01:27:21.508475+03:00", "module": "PAYMENT", "priority": "P20", "message": "200", "level": "INFO", "operation": "response", "status_code": 200, "ip": "127.0.0.1"}

```

## Contributing

Contributions are welcome! Please feel free to submit a PR.


## Contributors

- [Abdullah Alqahtani](https://github.com/anqorithm)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.