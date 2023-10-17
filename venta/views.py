from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from .models import Client,Category,Product,Invoice
from .forms import ClientForm,InvoiceForm,ProductForm
from decimal import Decimal
from django.db.models import Q
from django.contrib.auth.decorators import login_required
#paginator
from django.core.paginator import Paginator
# Para generar pdf
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template.loader import render_to_string

#clientes
@login_required
def clients(request):
    clients = Client.objects.filter(status=True)
    busqueda = request.GET.get('buscar')
    if busqueda:
        clients = Client.objects.filter(
            Q(client_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda) |
            Q(identy=busqueda)
        ).distinct()
        if not clients:
            error = "No se encontraron clientes con ese nombre"
            return render(request, 'clientes/clientes.html', {'error': error})
    paginator = Paginator(clients, 10)
    page = request.GET.get('page')
    clients_paginated = paginator.get_page(page)
    return render(request, 'clientes/clientes.html', {'clients': clients_paginated})
@login_required
def delete_client(request,id):
    client=get_object_or_404(Client,pk=id)
    if request.method == 'POST':
        client.status=False
        client.save()
        return redirect('clients')
    return HttpResponse("metodo no permitido")
@login_required
def create_client(request):
    if request.method == 'GET':
        form_client = ClientForm()
        return render(request, 'clientes/create_client.html', {'form_client': form_client})
    elif request.method == 'POST':
        form_client = ClientForm(request.POST)
        if form_client.is_valid():
            form_client.save()
            mensaje="Cliente guardado con exito!"
            return render(request, 'clientes/create_client.html', {'form_client': form_client,'exito':mensaje})
            
    else:
        mensaje="No se pudo guardar"
        return render(request, 'clientes/create_client.html', {'form_client': form_client,'alerta':mensaje})
       
@login_required    
def client_detail(request, id):
    cliente = get_object_or_404(Client, pk=id)
    if request.method == 'GET':
        form_detail = ClientForm(instance=cliente)
        return render(request, 'clientes/client_detail.html', {'form_detail':form_detail})
    else:
        form_detail = ClientForm(request.POST, instance=cliente)
        if form_detail.is_valid():
            form_detail.save()
            return redirect('clients')
        else:
            print(form_detail.errors)  # Imprime errores del formulario en la consola
    return render(request, 'clientes/client_detail.html', {'form_detail':form_detail})
            
#categoria          
@login_required       
def categories(request):
    categories=Category.objects.all()
    return render(request,'productos/categorias.html',{'categories':categories})
@login_required
def ver_categoria(request, categoria_id):
    categoria = get_object_or_404(Category, pk=categoria_id)
    productos = Product.objects.filter(category=categoria,stock__gt=0)
    busqueda=request.GET.get("buscar")
    if busqueda:     
        productos=Product.objects.filter(
            Q(product_name__icontains=busqueda)
        ).distinct()
        
    paginator=Paginator(productos,10)
    page=request.GET.get('page')
    product_paginated=paginator.get_page(page)
    return render(request, 'productos/ver_categoria.html', {'categoria': categoria, 'product_paginated': product_paginated})
@login_required
def crear_producto(request):
    if request.method == 'GET':
       product_form=ProductForm()
       return render(request,'productos/crear_producto.html',{'product_form':product_form})
    else:
        product_form=ProductForm(request.POST,request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect('categories')
    return render(request,'productos/crear_producto.html',{'product_form':product_form})
@login_required
def eliminar_producto(request,id):
    producto=get_object_or_404(Product,pk=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('categories')
    return HttpResponse("metodo no permitido")
@login_required   
def editar_producto(request,id):
    producto=get_object_or_404(Product,pk=id)
    if request.method == 'GET':
        form_product=ProductForm(instance=producto)
        return render(request,'productos/editar_producto.html',{'form_product':form_product})
    else:
        form_product=ProductForm(request.POST,request.FILES,instance=producto)
        if form_product.is_valid():
            form_product.save()
            mensaje="producto Guardado con exito"
            return render(request,'productos/editar_producto.html',{'form_product':form_product, 'alerta':mensaje})
        else:
            mensaje="no se pudo guardar"
            return render(request,'productos/editar_producto.html',{'form_product':form_product, 'alerta':mensaje})
            
        
#factura
@login_required
def mostrar_factura(request,id):
    factura=Invoice.objects.get(pk=id)
    return render(request,'factura/mostrar_factura.html',{'factura':factura})            
@login_required
def create_factura(request):
    form_factura=InvoiceForm()
    if request.method == 'POST':   
        form_factura=InvoiceForm(request.POST)
        if form_factura.is_valid():
            factura=form_factura.save(commit=False)
            subtotal=Decimal('0.00')
            for producto in form_factura.cleaned_data['product']:
                subtotal += producto.price * Decimal(str(form_factura.cleaned_data['quantity']))
            inpuestos=Decimal('0.12')
            total=subtotal + (subtotal * inpuestos)
            #actualizar datos
            for producto in form_factura.cleaned_data['product']:
                cantidad_vendida=form_factura.cleaned_data['quantity']
                producto.stock -= cantidad_vendida
                producto.save()
            factura.subtotal=subtotal
            factura.total=total
            factura.save()
            form_factura.save_m2m()          
            return redirect('mostrar_factura',id=factura.id)
    return render(request,'factura/crear_factura.html',{'form_factura':form_factura})
@login_required
def generar_pdf(request,id):
    factura=Invoice.objects.get(pk=id)
    context = {'factura': factura}
    template='factura/factura_pdf.html'
    html_string=render_to_string(template,context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura_generada.pdf"'
    pisa_status=pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response

#ventas
@login_required
def misventas(request):
    misventas=Invoice.objects.filter(active=True)
    paginator=Paginator(misventas,10)
    page=request.GET.get('page')
    ventas=paginator.get_page(page)
    return render(request,'ventas/misventas.html',{'ventas':ventas})
@login_required
def delete_sale(request,id):
    sale=get_object_or_404(Invoice,pk=id)
    if request.method == 'POST':   
       sale.active=False
       sale.save()
       return redirect('misventas')
    return HttpResponse("metodo no permitido")
    
    

   