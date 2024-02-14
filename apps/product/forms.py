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
    colour = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    brand = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    size = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ('name', 'price', 'photo', 'colour', 'brand', 'size', 'category')


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Category
        fields = ('name',)
