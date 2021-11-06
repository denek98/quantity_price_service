from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('initialize',views.initialize, name = 'initialize'),
    path('generate_price_list',views.generate_price_list, name = 'generate_price_list'),
    path('generate_suppliers_file',views.generate_suppliers_file, name = 'generate_suppliers_file'),
    
]