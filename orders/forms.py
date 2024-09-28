from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Питер'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Паркер'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'spiderman@gmail.com'}))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'улица Ингрэм 20, Форест-Хиллз, Куинс, Нью-Йорк, Нью-Йорк 11375, США'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
