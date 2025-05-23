'''
urls.py is created in the my_web_app directory
'''

from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home, name='home'),
    path('category/', views.category, name='category'),
    path('product/', views.product, name='product'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('admin-page/', views.admin, name='admin'),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('category/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('category/add/', views.add_category, name='add_category'),
    path('product/add/', views.add_product, name='add_product'),
]

'''secound index
    localhost:8000/a/b
'''
