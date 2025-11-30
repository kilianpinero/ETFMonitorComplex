from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from application.stripe_service import StripeService

router = APIRouter(prefix="/stripe", tags=["stripe"])

class CreateCustomerRequest(BaseModel):
    email: str
    name: str | None = None

class CheckoutSessionRequest(BaseModel):
    customer_id: str
    product_id: str
    success_url: str
    cancel_url: str
    recurring: bool = True

@router.post("/customer")
def create_customer(data: CreateCustomerRequest):
    try:
        customer_id = StripeService.create_customer(data.email, data.name)
        return {"customer_id": customer_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/checkout-session")
def create_checkout_session(data: CheckoutSessionRequest):
    try:
        url = StripeService.create_checkout_session_from_product(
            data.customer_id, data.product_id, data.success_url, data.cancel_url, data.recurring
        )
        return {"checkout_url": url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cancel-subscription")
def cancel_subscription(email: str = Query(..., description="Email del usuario")):
    try:
        result = StripeService.cancel_subscription_by_email(email)
        if not result:
            raise HTTPException(status_code=404, detail="No se pudo cancelar la suscripción")
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/product-prices/{product_id}")
def get_product_prices(product_id: str):
    try:
        prices = StripeService.get_product_prices(product_id)
        return {"prices": [p.id for p in prices]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))