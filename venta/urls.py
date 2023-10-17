from django.urls import path

from .views import clients,delete_client,create_client,client_detail,categories,ver_categoria,create_factura,mostrar_factura,generar_pdf,misventas,delete_sale,crear_producto,eliminar_producto,editar_producto
urlpatterns = [
    path('Anahion/clients/',clients,name="clients"),
    path('Anahion/delete_client/<int:id>/',delete_client,name="delete_client"),
    path('Anahion/create_client/',create_client,name="create_client"),
    path('Anahion/crear_producto/',crear_producto,name="crear_producto"),
    path('Anahion/client_detail/<int:id>/',client_detail,name="client_detail"),
    path('Anahion/categories/',categories,name="categories"),
    path('Anahion/categoria/<int:categoria_id>/', ver_categoria, name='ver_categoria'),
    path('Anahion/create_factura/',create_factura,name="create_factura"),
    path('Anahion/mostrar_factura/<int:id>/',mostrar_factura, name='mostrar_factura'),
    path('Anahion/generar_pdf/<int:id>/',generar_pdf, name='generar_pdf'),
    path('Anahion/misventas',misventas,name="misventas"),
    path('Anahion/delete_sale/<int:id>/',delete_sale,name='delete_sale'),
    path('Anahion/eliminar_producto/<int:id>/',eliminar_producto,name="eliminar_producto"),
    path('Anahion/editar_producto/<int:id>/',editar_producto,name="editar_producto"),
]