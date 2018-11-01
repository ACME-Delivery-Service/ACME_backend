"""acme_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from pprint import pprint
from django.contrib import admin
from django.urls import path

from acme_backend.settings import DEBUG
from web_app.routers import ApiRouter
from web_app.view_sets.AccountViewSet import AccountViewSet
from web_app.view_sets.DriverViewSet import DriverViewSet
from web_app.view_sets.OrderViewSet import OrderViewSet
from web_app.view_sets.CustomerViewSet import CustomerViewSet

router = ApiRouter(trailing_slash=False)
router.register(r'account', AccountViewSet, base_name='account')
router.register(r'driver', DriverViewSet, base_name='driver')
router.register(r'order', OrderViewSet, base_name='order')
router.register(r'customer', CustomerViewSet, base_name='customer')

if DEBUG:
    pprint(router.urls)

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += router.urls
