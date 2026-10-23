from .adyen_provider_factory import AdyenProviderFactory
from .mercado_pago_provider_factory import MercadoPagoProviderFactory
from .payment_provider_factory import PaymentProviderFactory
from .stripe_provider_factory import StripeProviderFactory


class PaymentProviderRegistry:
    def __init__(self, factories: dict[str, PaymentProviderFactory]):
        self._factories = factories

    @classmethod
    def default(cls) -> "PaymentProviderRegistry":
        return cls(
            {
                "stripe": StripeProviderFactory(),
                "adyen": AdyenProviderFactory(),
                "mercado_pago": MercadoPagoProviderFactory(),
            }
        )

    def get(self, provider: str) -> PaymentProviderFactory:
        if provider not in self._factories:
            raise ValueError(f"Unsupported provider: {provider}")
        return self._factories[provider]
