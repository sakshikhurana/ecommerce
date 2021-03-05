"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views
from django.conf.urls.static import static
from django.conf import settings
from products.views import home_page, about_page
from django.contrib.auth.views import LogoutView
from cart.views import cart_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_page, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register_page, name='register'),
    path('products/', include('products.urls')),
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('search', include('search.urls', namespace='search')),
    path('cart/', include('cart.urls', namespace='cart'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
