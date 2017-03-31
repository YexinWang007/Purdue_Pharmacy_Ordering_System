from django import forms
from .models import Client,Order,Drug,Wish_List, Shopping_Cart
from django.forms.formsets import BaseFormSet

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
            "comment"
        ]


class DrugForm(forms.ModelForm):
    class Meta:
        model = Shopping_Cart
        fields = [
            "shopping_drug_name",
            "shopping_drug_brand",
            "shopping_quantity",
            "shopping_strength"
        ]
        widgets = {
            'shopping_drug_name': forms.TextInput(attrs={'placeholder': 'Drug Name'}),
            'shopping_drug_brand': forms.TextInput(attrs={'placeholder': 'Drug Brand'}),
            'shopping_quantity': forms.TextInput(attrs={'placeholder': 'Quantity'}),
            'shopping_strength': forms.TextInput(attrs={'placeholder': 'Strength'}),
        }



class BaseDrugFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        drug_names = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                drug_name = form.cleaned_data['shopping_drug_name']
                if drug_name:
                    if drug_name in drug_names:
                        duplicates = True
                    drug_names.append(drug_name)

                if duplicates:
                    raise forms.ValidationError(
                        'Please fill in a drug form with different drugs.',
                        code='duplicate_drugs'
                    )

class Wish_ListForm(forms.ModelForm):
    class Meta:
        model=Wish_List
        fields=[
            "wish_drug_name",
            #"wish_drug_brand",
            #"wish_drug_strength"
        ]

