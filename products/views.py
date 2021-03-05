from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Product
from .forms import ProductForm
from django.http import Http404
from cart.models import Cart


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('id')
        instance = Product.objects.get_object_by_id(id=pk)
        if instance is None:
            raise Http404("Product not found")
        return instance


class ProductCreateView(CreateView):
    model = Product
    template_name = 'products/create.html'
    form_class = ProductForm
    success_url = 'detail.html'


class ProductListFeaturedView(ListView):
    template_name = 'products/featured_list.html'

    def get_queryset(self):
        return Product.objects.featured()


class ProductDetailFeaturedView(DetailView):
    template_name = 'products/featured_detail.html'

    def get_queryset(self):
        return Product.objects.featured()


class ProductSlugDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404('Not found')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Exception raised")
        return instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


def home_page(request):
    return render(request, 'home_page.html')


def about_page(request):
    return render(request, 'about_page.html')
