from django.urls import path
from products import views

urlpatterns = [
    path('hello/',views.hello),
    path('allproducts/',views.get_products),
    path('product/<int:id>',views.get_product),
    path('product/',views.create_product),
    path('delete/<int:id>',views.delete_product),
    path('products/filter/',views.filter_products),
    path('category/',views.create_category)
]