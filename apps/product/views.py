from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.product.filters import ProductFilter
from apps.product.forms import CategoryForm, ProductForm
from apps.product.models import Category, Product
from common.mixins import FilterMixin, GroupRequiredMixin, TitleMixin


class ProductListView(TitleMixin, FilterMixin, ListView):
    title = 'Products'
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 3
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        query = self.request.GET.get('query', None)
        return queryset.filter(Q(name__icontains=query) | Q(category__name__icontains=query)) if query else queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category_id'] = self.kwargs.get('category_id', None)
        return context


class ProductDetailView(TitleMixin, LoginRequiredMixin, GroupRequiredMixin, DetailView):
    title = 'Product detail'
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    group_required = 'manager'


class ProductCreateView(TitleMixin, LoginRequiredMixin, GroupRequiredMixin, CreateView):
    title = 'Create product'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:products')
    template_name = 'product/product_create.html'
    group_required = 'manager'


class ProductUpdateView(TitleMixin, LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    title = 'Update product'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:products')
    template_name = 'product/product_update.html'
    group_required = 'manager'


class ProductDeleteView(TitleMixin, LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    title = 'Delete product'
    model = Product
    template_name = 'product/product_delete.html'
    success_url = reverse_lazy('product:products')
    group_required = 'manager'


class CategoryCreateView(TitleMixin, LoginRequiredMixin, GroupRequiredMixin, CreateView):
    title = 'Create category'
    model = Category
    form_class = CategoryForm
    template_name = 'product/category/category_create.html'
    success_url = reverse_lazy('product:products')
    group_required = 'manager'
