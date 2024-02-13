from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    photo = models.ImageField(upload_to='products', verbose_name='Photo')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
