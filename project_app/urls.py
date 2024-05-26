"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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


from django.urls import path, include
from .views import *

urlpatterns = [
    path('',index, name="index"),
    path('index/', index, name="index") ,
    path('login/',log_in, name="log_in"),
    path('logout/', log_out, name="log_out"),
    path('register/',register, name="register"),
    # path('add-product/',add_product, name="add_product"),
    # path("delete-product/<id>/", delete_product, name="delete_product"),
    # path("update-product/<id>/", update_product, name="update_product"),
]
