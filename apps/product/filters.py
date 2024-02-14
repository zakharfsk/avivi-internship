import django_filters

from apps.product.models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'price': ['lt', 'gt'],
            'colour': ['exact'],
            'brand': ['exact'],
            'size': ['exact'],
            'category': ['exact'],
        }
