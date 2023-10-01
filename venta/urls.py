from django.urls import path

from .views import clients,delete_client,create_client,client_detail,categories,ver_categoria,create_factura,mostrar_factura,generar_pdf
urlpatterns = [
    path('clients/',clients,name="clients"),
    path('delete_client/<int:id>/',delete_client,name="delete_client"),
    path('create_client/',create_client,name="create_client"),
    path('client_detail/<int:id>/',client_detail,name="client_detail"),
    path('categories/',categories,name="categories"),
    path('categoria/<int:categoria_id>/', ver_categoria, name='ver_categoria'),
    path('create_factura/',create_factura,name="create_factura"),
    path('mostrar_factura/<int:id>/',mostrar_factura, name='mostrar_factura'),
    path('generar_pdf/<int:id>/',generar_pdf, name='generar_pdf'),
]