from django import forms


class CheckoutForm(forms.Form):
    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3})
    )
    phone = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    shipping_address = forms.CharField(widget=forms.Textarea)
    payment_method = forms.ChoiceField(
        choices=[
            ("COD", "Cash on Delivery"),
            ("Card", "Credit/Debit Card"),
            ("Bank", "Bank Transfer"),
        ]
    )
