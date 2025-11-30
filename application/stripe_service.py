import stripe
import os
from dotenv import load_dotenv
import logging
from domain.user import User
from infrastructure.repository.user_repository import UserRepository

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env.local'))
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class StripeService:
    @staticmethod
    def create_customer(email: str, name: str = None) -> str:
        try:
            customer = stripe.Customer.create(email=email, name=name)
            return customer.id
        except stripe.error.StripeError as e:
            logging.error(f"Stripe error (create_customer): {e}")
            raise
        except Exception as e:
            logging.error(f"General error (create_customer): {e}")
            raise

    @staticmethod
    def get_product_prices(product_id: str):
        try:
            prices = stripe.Price.list(product=product_id, active=True)
            return prices.data
        except stripe.error.StripeError as e:
            logging.error(f"Stripe error (get_product_prices): {e}")
            raise
        except Exception as e:
            logging.error(f"General error (get_product_prices): {e}")
            raise

    @staticmethod
    def create_checkout_session_from_product(customer_id: str, product_id: str, success_url: str, cancel_url: str, recurring: bool = True) -> str:
        try:
            prices = StripeService.get_product_prices(product_id)
            if not prices:
                raise ValueError("No hay prices activos para este producto.")
            price_id = prices[0].id
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=["card"],
                line_items=[{
                    "price": price_id,
                    "quantity": 1
                }],
                mode="subscription" if recurring else "payment",
                success_url=success_url,
                cancel_url=cancel_url
            )
            return session.url
        except stripe.error.StripeError as e:
            logging.error(f"Stripe error (create_checkout_session_from_product): {e}")
            raise
        except Exception as e:
            logging.error(f"General error (create_checkout_session_from_product): {e}")
            raise

    @staticmethod
    def cancel_subscription_by_email(email: str,) -> bool:
        """
        Cancela la suscripción activa de un usuario en Stripe usando su email.
        Args:
            email (str): Email del usuario en la base de datos.
        Returns:
            bool: True si se cancela correctamente, False si no.
        """
        try:
            users = UserRepository()
            user = users.get_by_email(email)
            if not user or not user.stripe_customer_id:
                logging.error(f"Usuario no encontrado o sin stripe_customer_id: {email}")
                return False
            customer_id = user.stripe_customer_id
            subscriptions = stripe.Subscription.list(customer=customer_id, status='active', limit=1)
            if not subscriptions.data:
                logging.error(f"No hay suscripción activa para el usuario: {email}")
                return False
            subscription_id = subscriptions.data[0].id
            subscription = stripe.Subscription.cancel(subscription_id)
            logging.info(f"Suscripción cancelada: {subscription.id}")
            return True
        except stripe.error.StripeError as e:
            logging.error(f"Stripe error (cancel_subscription_by_email): {e}")
            return False
        except Exception as e:
            logging.error(f"General error (cancel_subscription_by_email): {e}")
            return False


# ESTOS METODOS NO SON NECESARIOS UTILIZANDO CHECKOUT SESSION DE STRIPE
    # @staticmethod
    # def create_payment_method(card_token: str) -> str:
    #     try:
    #         payment_method = stripe.PaymentMethod.create(
    #             type="card",
    #             card={"token": card_token}
    #         )
    #         return payment_method.id
    #     except stripe.error.StripeError as e:
    #         logging.error(f"Stripe error (create_payment_method): {e}")
    #         raise
    #     except Exception as e:
    #         logging.error(f"General error (create_payment_method): {e}")
    #         raise
    #
    # @staticmethod
    # def attach_payment_method_to_customer(payment_method_id: str, customer_id: str):
    #     try:
    #         stripe.PaymentMethod.attach(
    #             payment_method_id,
    #             customer=customer_id
    #         )
    #         stripe.Customer.modify(
    #             customer_id,
    #             invoice_settings={"default_payment_method": payment_method_id}
    #         )
    #     except stripe.error.StripeError as e:
    #         logging.error(f"Stripe error (attach_payment_method_to_customer): {e}")
    #         raise
    #     except Exception as e:
    #         logging.error(f"General error (attach_payment_method_to_customer): {e}")
    #         raise