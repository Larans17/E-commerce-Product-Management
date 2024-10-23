from django.urls import path
from Web.views import *


urlpatterns = [
    # category url ------------
    path('create-category/',create_category,name='create-category'),
    path('category-list-datatable/',category_list_datatable,name='category-list-datatable'),
    path('delete-category/',delete_category,name='delete-category'),
    path('get-category/',get_category,name='get-category'),
    # product url ------------
    path('create-product/',create_product,name='create-product'),
    path('product-list-datatable/',product_list_datatable,name='product-list-datatable'),
    path('delete-product/',delete_product,name='delete-product'),
    path('get-product/',get_product,name='get-product'), 
    # search product ----------
    path('product-list/',product_list_page,name='product-list'), 
    path('search-related-product/',search_related_Product_results,name='search-related-product'), 
]