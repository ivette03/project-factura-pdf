from django.urls import path
from .views import clients,delete_client,create_client
urlpatterns = [
    path('clients/',clients,name="clients"),
    path('delete_client/<int:id>/',delete_client,name="delete_client"),
    path('create_client/',create_client,name="create_client")
]
