from django import forms
from .models import Seller

class SellerApplyForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['phone_number']
        
