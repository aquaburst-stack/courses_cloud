from django import forms


class SearchModules(forms.Form):
    module = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-0', 'placeholder': 'Module Name'}))