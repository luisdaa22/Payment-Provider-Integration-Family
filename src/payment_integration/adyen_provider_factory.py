from .adyen_authorizer import AdyenAuthorizer
from .adyen_refund_processor import AdyenRefundProcessor
from .adyen_webhook_verifier import AdyenWebhookVerifier
from .payment_provider_factory import PaymentProviderFactory


class AdyenProviderFactory(PaymentProviderFactory):
    def create_authorizer(self) -> AdyenAuthorizer:
        return AdyenAuthorizer()

    def create_refund_processor(self) -> AdyenRefundProcessor:
        return AdyenRefundProcessor()

    def create_webhook_verifier(self) -> AdyenWebhookVerifier:
        return AdyenWebhookVerifier()
