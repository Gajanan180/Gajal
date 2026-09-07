from django import forms

from .models import Payment


class PaymentForm(forms.Form):
    method = forms.ChoiceField(
        choices=Payment.Method.choices,
        widget=forms.RadioSelect,
    )
    card_number = forms.CharField(
        required=False,
        max_length=19,
        widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'}),
    )
    card_expiry = forms.CharField(
        required=False,
        max_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}),
    )
    card_cvv = forms.CharField(
        required=False,
        max_length=4,
        widget=forms.PasswordInput(attrs={'placeholder': 'CVV'}),
    )

    def clean(self):
        cleaned = super().clean()
        method = cleaned.get('method')
        if method == Payment.Method.CARD:
            for field in ['card_number', 'card_expiry', 'card_cvv']:
                if not cleaned.get(field):
                    self.add_error(field, 'Required for card payment.')
        return cleaned
