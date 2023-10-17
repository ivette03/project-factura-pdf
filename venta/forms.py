from django import forms
from django.forms import ModelForm
from .models import Client,Invoice,Product


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
class InvoiceForm(ModelForm):
    class Meta:
        model=Invoice
        fields=['invoice_number','date','client','product','quantity']
        widgets={
            'invoice_number':forms.TextInput(attrs={'class':'form-control'}),
            'date':forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'client':forms.Select(attrs={'class':'form-control'}),
            'product':forms.SelectMultiple(attrs={'class':'form-control'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),        
        }
class ProductForm(ModelForm):
    class Meta:
        model=Product
        fields=['product_name','price','img','category','stock']
        widgets={
            'product_name':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'stock':forms.TextInput(attrs={'class':'form-control'})
        }
