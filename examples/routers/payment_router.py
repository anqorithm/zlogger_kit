from fastapi import APIRouter, HTTPException
from examples.modules import Module
from zlogger_kit import ZLogConfig, ZLog

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
    responses={404: {"description": "Not found"}},
)

logger = ZLog.init(
    ZLogConfig(
        module=Module.PAYMENT.value,
        log_path="logs",
        time_zone="Asia/Riyadh",
        json_format=True,
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
