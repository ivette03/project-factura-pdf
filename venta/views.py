from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from .models import Client,Category
from .forms import ClientForm
#paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

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
def categories(request):
    categories=Category.objects.all()
    return render(request,'productos/categorias.html',{'categories':categories})
        
            
    
   