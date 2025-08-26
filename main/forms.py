from django import forms
from django.core.exceptions import ValidationError

from .models import Sale


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        product = self.cleaned_data.get("product")

        if product and quantity:
            if product.amount < quantity:
                raise ValidationError(
                    f"Mahsulot yetarli emas! Omborda faqat {product.amount} dona bor."
                )
        return quantity
