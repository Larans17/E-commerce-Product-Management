from django.urls import path
from APIApp.views import *

urlpatterns = [
    path('login/',LoginAPI.as_view(),name='login'), 
    # category api url----------------------
    path('post-category/',PostCategoryAPI.as_view()),
    path('getall-category-list/',CategoryListDatatableAPI.as_view()),
    path('put-category/',PutCategoryAPI.as_view()),
    path('get-category/',PutCategoryAPI.as_view()),
    path('delete-category/',PutCategoryAPI.as_view()),
    
    # product crud url ---------------------------
    path('post-product/',PostProductAPI.as_view()),
    path('get-datatable-productlist/',ProductListDatatableAPI.as_view()),
    path('get-product/',PutProductAPI.as_view()),
    path('put-product/',PutProductAPI.as_view()),
    path('delete-product/',PutProductAPI.as_view()),
    # search product
    path('search-product/',GetSearchProductApi.as_view()),
    
    
]
