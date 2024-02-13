from django import forms

from .models import Category, Product


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    photo = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ('name', 'price', 'photo', 'category')


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Category
        fields = ('name',)
