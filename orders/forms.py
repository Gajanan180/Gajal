from django import forms


class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter delivery address'}),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Special instructions (optional)'}),
    )
