import pytest

from payment_integration.checkout_service import CheckoutService
from payment_integration.payment_authorizer import PaymentAuthorizer
from payment_integration.payment_provider_registry import PaymentProviderRegistry
from payment_integration.refund_processor import RefundProcessor
from payment_integration.webhook_verifier import WebhookVerifier


class FakeAuthorizer(PaymentAuthorizer):
    def authorize(self, amount: float) -> str:
        return "fake:authorized"


class FakeRefundProcessor(RefundProcessor):
    def refund(self, amount: float) -> str:
        return "fake:refunded"


class FakeWebhookVerifier(WebhookVerifier):
    def verify(self, signature: str) -> bool:
        return True


class FakeFactory:
    def create_authorizer(self) -> PaymentAuthorizer:
        return FakeAuthorizer()

    def create_refund_processor(self) -> RefundProcessor:
        return FakeRefundProcessor()

    def create_webhook_verifier(self) -> WebhookVerifier:
        return FakeWebhookVerifier()


def checkout_for(provider: str) -> CheckoutService:
    return CheckoutService(PaymentProviderRegistry.default().get(provider))


def test_stripe_family_is_selected_together():
    checkout = checkout_for("stripe")

    assert checkout.authorize_payment(125.50) == "stripe:authorized:125.50"
    assert checkout.refund_payment(25.00) == "stripe:refunded:25.00"
    assert checkout.verify_webhook("stripe-valid") is True
    assert checkout.verify_webhook("adyen-valid") is False


def test_adyen_family_is_selected_together():
    checkout = checkout_for("adyen")

    assert checkout.authorize_payment(125.50) == "adyen:authorized:125.50"
    assert checkout.refund_payment(25.00) == "adyen:refunded:25.00"
    assert checkout.verify_webhook("adyen-valid") is True
    assert checkout.verify_webhook("stripe-valid") is False


def test_mercado_pago_family_is_selected_together():
    checkout = checkout_for("mercado_pago")

    assert checkout.authorize_payment(125.50) == "mercado_pago:authorized:125.50"
    assert checkout.refund_payment(25.00) == "mercado_pago:refunded:25.00"
    assert checkout.verify_webhook("mercado_pago-valid") is True
    assert checkout.verify_webhook("stripe-valid") is False


def test_checkout_accepts_any_factory_without_provider_classes():
    checkout = CheckoutService(FakeFactory())

    assert checkout.authorize_payment(1.0) == "fake:authorized"
    assert checkout.refund_payment(1.0) == "fake:refunded"
    assert checkout.verify_webhook("anything") is True


def test_unsupported_provider_is_rejected():
    with pytest.raises(ValueError):
        PaymentProviderRegistry.default().get("paypal")
