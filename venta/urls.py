from django.urls import path

from .views import clients,delete_client,create_client,client_detail,categories
urlpatterns = [
    path('clients/',clients,name="clients"),
    path('delete_client/<int:id>/',delete_client,name="delete_client"),
    path('create_client/',create_client,name="create_client"),
    path('client_detail/<int:id>/',client_detail,name="client_detail"),
    path('categories/',categories,name="categories"),
]