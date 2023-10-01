from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from .models import Client,Category,Product,Invoice
from .forms import ClientForm,InvoiceForm
from decimal import Decimal
#paginator
from django.core.paginator import Paginator
from django.db.models import Q
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template.loader import render_to_string




#clientes
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
def delete_client(request,id):
    client=get_object_or_404(Client,pk=id)
    if request.method == 'POST':
        client.status=False
        client.save()
        return redirect('clients')
    return HttpResponse("metodo no permitido")
def create_client(request):
    if request.method == 'GET':
        form_client = ClientForm()
        return render(request, 'clientes/create_client.html', {'form_client': form_client})
    elif request.method == 'POST':
        form_client = ClientForm(request.POST)
        if form_client.is_valid():
            form_client.save()
            return redirect('create_client')
    else:
        return render(request, 'clientes/create_client.html', {'form_client': form_client})
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
            
            
            
#categoria
def categories(request):
    categories=Category.objects.all()
    return render(request,'productos/categorias.html',{'categories':categories})

def ver_categoria(request, categoria_id):
    categoria = get_object_or_404(Category, pk=categoria_id)
    productos = Product.objects.filter(category=categoria,stock__gt=0)
    busqueda=request.GET.get("buscar")
    if busqueda:
        productos=Product.objects.filter(
            Q(product_name__icontains=busqueda)
        ).distinct()
        if not  productos:
           error="no se encontro ese producto"
           return render(request, 'productos/ver_categoria.html', {'error':error})
    paginator=Paginator(productos,10)
    page=request.GET.get('page')
    product_paginated=paginator.get_page(page)
    return render(request, 'productos/ver_categoria.html', {'categoria': categoria, 'product_paginated': product_paginated})




def mostrar_factura(request,id):
    factura=Invoice.objects.get(pk=id)
    return render(request,'factura/mostrar_factura.html',{'factura':factura})
            



#factura
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
    
    

   