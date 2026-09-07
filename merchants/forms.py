from django import forms

from .models import Category, FoodItem, Store


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'address', 'phone', 'cuisines', 'image', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['category', 'name', 'description', 'price', 'image', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, store=None, **kwargs):
        super().__init__(*args, **kwargs)
        if store:
            self.fields['category'].queryset = Category.objects.filter(store=store)
