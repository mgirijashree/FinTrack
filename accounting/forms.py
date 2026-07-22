from django import forms
from .models import Transaction, Category


class TransactionForm(forms.ModelForm):

    class Meta:

        model = Transaction

        fields = [
            "category",
            "date",
            "description",
            "amount",
            "type",
        ]

        widgets = {

            "category": forms.Select(
                attrs={
                    "class": "w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "class": "w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
                }
            ),

            "type": forms.Select(
                attrs={
                    "class": "w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
                }
            ),

        }


class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category

        fields = [
            "name",
            "gst_percentage",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter Category Name",
                    "class": "w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
                }
            ),

            "gst_percentage": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "placeholder": "GST %",
                    "class": "w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
                }
            ),

        }