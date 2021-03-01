
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('<slug:slug>', views.ProductSlugDetailView.as_view(), name='detail'),
    path('create', views.ProductCreateView.as_view(), name='create'),
    path('featured/', views.ProductListFeaturedView.as_view(), name='featured_list'),
    path('featured/<int:pk>', views.ProductDetailFeaturedView.as_view(),
         name='featured_detail'),
    path('<slug:slug>',
         views.ProductSlugDetailView.as_view(), name='slug_detail')
]
