from django import forms
from .models import Client,Order

class ClientForm(forms.ModelForm):
    class Meta:
        model=Client
        fields=[
            "client_name",
            "phone_number",
            "contact_email"
        ]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "drug_name",
            "drug_brand",
            "quantity",
            "strength",
            "doctor_name",
            "doctor_email",
            "comment"
        ]
