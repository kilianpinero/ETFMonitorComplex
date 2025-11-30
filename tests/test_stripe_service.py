import pytest
from unittest.mock import patch, MagicMock
from application.stripe_service import StripeService

@pytest.fixture
def stripe_customer():
    return {'id': 'cus_test123'}

@pytest.fixture
def stripe_payment_method():
    return {'id': 'pm_test123'}

@pytest.fixture
def stripe_price():
    class Price:
        id = 'price_test123'
    return [Price()]

@patch('application.stripe_service.stripe.Customer.create')
def test_create_customer(mock_create, stripe_customer):
    mock_create.return_value = stripe_customer
    customer_id = StripeService.create_customer('test@example.com', 'Test User')
    assert customer_id == 'cus_test123'

@patch('application.stripe_service.stripe.PaymentMethod.create')
def test_create_payment_method(mock_create, stripe_payment_method):
    mock_create.return_value = stripe_payment_method
    payment_method_id = StripeService.create_payment_method('tok_test')
    assert payment_method_id == 'pm_test123'

@patch('application.stripe_service.stripe.PaymentMethod.attach')
@patch('application.stripe_service.stripe.Customer.modify')
def test_attach_payment_method_to_customer(mock_modify, mock_attach):
    mock_attach.return_value = None
    mock_modify.return_value = None
    # Should not raise
    StripeService.attach_payment_method_to_customer('pm_test123', 'cus_test123')

@patch('application.stripe_service.stripe.Price.list')
def test_get_product_prices(mock_list, stripe_price):
    mock_list.return_value = MagicMock(data=stripe_price)
    prices = StripeService.get_product_prices('prod_test123')
    assert prices[0].id == 'price_test123'

@patch('application.stripe_service.stripe.checkout.Session.create')
@patch('application.stripe_service.StripeService.get_product_prices')
def test_create_checkout_session_from_product(mock_get_prices, mock_create_session, stripe_price):
    mock_get_prices.return_value = stripe_price
    mock_create_session.return_value = MagicMock(url='https://checkout.stripe.com/testsession')
    url = StripeService.create_checkout_session_from_product('cus_test123', 'prod_test123', 'https://success', 'https://cancel')
    assert url == 'https://checkout.stripe.com/testsession'

