from django import forms
from .models import Friend

class FindForm(forms.Form):
  find = forms.CharField(label="Find", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))

class CheckForm(forms.Form):
  str = forms.CharField(label="Name", widget=forms.TextInput(attrs={"class":"form-control"}))