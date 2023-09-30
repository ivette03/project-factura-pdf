from django import forms
from django.forms import ModelForm
from .models import Client

class ClientForm(ModelForm):
    class Meta:
        model=Client
        fields=['client_name','last_name','address','identy','number_phone']
        widgets={
            'client_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'identy':forms.TextInput(attrs={'class':'form-control'}),
            'number_phone':forms.TextInput(attrs={'class':'form-control'})       
        }
       