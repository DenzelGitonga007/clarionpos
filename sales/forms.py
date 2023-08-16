from django import forms

class ExpenseForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    description = forms.CharField()
    amount = forms.DecimalField(decimal_places=2)
