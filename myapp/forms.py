from django import forms
from.models  import user
from.models import product
from .models import phar

class editprofileform(forms.ModelForm):
    class Meta:
        model=user
        fields=['name','email','address']

class editproductform(forms.ModelForm):
    class Meta:
        model=product
        fields=['medicinename','price','company','type','image']

class pharmacyprofileform(forms.ModelForm):
    class Meta:
        model = phar
        fields = ['name', 'email', 'phone_no']

