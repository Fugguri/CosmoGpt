from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from uuid import uuid4


class Product(BaseModel):
    id: str
    title: int


class PaymentEntry(BaseModel):
    product: Product
    contractId: str
    amount: int
    currency: str
    timestamp: str
    status: str
    errorMessage: str


{
    "product": {
        "id": "9f735241-90a9-43db-858a-9ccc13094673",
        "title": "Subscription 2177602705"
    },
    "contractId": "7a29f895-0cdf-4e2a-91a4-7dc875292646",
    "amount": 0.01,
    "currency": "USD",
    "timestamp": "2024-02-13T10:34:36Z",
    "status": "subscription-failed",
    "errorMessage": "Cancelled by customer"
}
