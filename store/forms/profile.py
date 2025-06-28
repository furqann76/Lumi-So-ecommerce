from django import forms
from ..models import Customer


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "phone_number",
            "shipping_address",
            "billing_address",
            "date_of_birth",
        ]
