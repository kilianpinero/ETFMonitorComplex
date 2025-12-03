from application.stripe_service import StripeService

# Datos de prueba reales (modifica según tu cuenta y entorno)
email = "testuser_prueba1@example.com"
name = "Test Userprueba1"
card_token = "tok_visa"  # Usa un token de prueba de Stripe 4242424242424242
product_id = "prod_TPROPMxiBSc3F3"  # Tu product_id real
success_url = "https://example.com/success"
cancel_url = "https://example.com/cancel"

# 1. Crear cliente en Stripe
customer_id = StripeService.create_customer(email=email, name=name)
print(f"Customer ID: {customer_id}")

# 4. Obtener prices del producto
prices = StripeService.get_product_prices(product_id)
print(f"Prices for product: {[p.id for p in prices]}")

# 5. Crear sesión de checkout para suscripción
checkout_url = StripeService.create_checkout_session_from_product(
    customer_id=customer_id,
    product_id=product_id,
    success_url=success_url,
    cancel_url=cancel_url,
    recurring=True
)
print(f"Checkout Session URL: {checkout_url}")

# print(StripeService.cancel_subscription_by_email("testuser_prueba@example.com"))

