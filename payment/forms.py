from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'full_name'}), 
        required=True)
    shipping_email = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email'}), 
        required=True)
    shipping_address1 = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address1'}), 
        required=True)
    shipping_address2 = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address2'}), 
        required=True)
    shipping_city = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}), 
        required=True)
    shipping_state = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'state'}), 
        required=False)
    shipping_zipcode = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'zipcode'}), 
        required=False)
    shipping_country = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'country'}), 
        required=True)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']

        exclude = ['user',]

class GuestCheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)

