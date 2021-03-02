from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product
# Create your views here.


class SearchListView(ListView):
    template_name = 'search/view.html'

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            return Product.objects.search(query=query)
        return Product.objects.featured()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context
