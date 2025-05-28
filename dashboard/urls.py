from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path("", CustomLoginView.as_view(), name="login"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registro/', views.registro, name='registro'),
    path('recuperar/', views.recuperar, name='recuperar'),
    path('Clientes/', views.clientes, name='clientes'),
    path('proveedores/', views.proveedores, name='proveedores'),
    path('inventario/', views.inventario, name='inventario'),
    path('index/', views.index, name='index'), 
]

