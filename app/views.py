from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    update_session_auth_hash
    )
from django.contrib.auth.forms import (
    UserChangeForm, 
    UserCreationForm, 
    PasswordChangeForm
    )
from .forms import (    
    EditProfileForm,
    RegisterProfileForm,    
    CategoriaForm,
    CategoriaFormView,
    OrcamentoForm,
    OrcamentoFormView,
    PagamentoForm,
    )
from .models import (    
    Categoria,
    Orcamento,
    Pagamento,
    )
from django.contrib.postgres.search import SearchVector
from django.utils import timezone


# Create your views here.
def Home(request):
	return render(request, 'app/base.html', {})

def Profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)

def Edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('app:profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

def Register(request):
    if request.method == 'POST':
        form = RegisterProfileForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('app:profile')            
                
        args = {'form': form}
        return render(request,'accounts/register.html', args)
        
    else:
        form = RegisterProfileForm()
        args = {'form': form}
        return render(request,'accounts/register.html', args)

def Change_Password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('app:profile')
        else:
            args = {'form': form}
            return render(request,'accounts/change_password.html', args)


    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

def Categoria_New(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            #anotacao = form.save(commit=False)            
            #anotacao.data = timezone.now()
            form.save()            
            return redirect('app:home')
    else:
        form = CategoriaForm()

    return render(request, 'app/categoria_new.html', {'form': form})

def Categoria_Edit(request, pk): 
    CategoriaEdit = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=CategoriaEdit)

        if form.is_valid():
            form.save()
            return redirect('app:categoria_detail', pk=pk)

    else:
        form = CategoriaForm(instance=CategoriaEdit)

    return render(request, 'app/categoria_edit.html', {'form': form, 'categoria':CategoriaEdit})

def Categoria_Detail(request, pk):        
    CategoriaDetail = get_object_or_404(Categoria, pk=pk)
    form = CategoriaFormView(instance=CategoriaDetail)
    return render(request, 'app/categoria_detail.html', {'form': form, 'categoria':CategoriaDetail})

def Categoria_List(request, filtro):    
    #categoria_list = Categoria.objects.all()
    if filtro == 'all':
        filtro = ''

    page    = request.GET.get('page', 1)
    
    categoria_list = Categoria.objects.filter(nome__contains=filtro).order_by('nome')

    paginator = Paginator(categoria_list, 10)
    try:
        categorias = paginator.page(page)
    except PageNotAnInteger:
        categorias = paginator.page(1)
    except EmptyPage:
        categorias = paginator.page(paginator.num_pages)    

    return render(request, 'app/categoria_list.html', { 'categoria_list': categorias , 'filtro': filtro})

def Categoria_Filtro(request):
    filtro = request.POST.get('input_search', 'all')
    if filtro == '':
        filtro = 'all'
    
    return redirect('app:categoria_list', filtro=filtro)

def Categoria_Del(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)    
    form = CategoriaFormView(instance=categoria)
    if request.method=='POST':
        categoria.delete()
        return redirect('app:categoria_list', filtro='all')

    return render(request, 'app/categoria_del.html', {'categoria':categoria, 'form': form})

def Orcamento_New(request):
    if request.method == 'POST':
        form = OrcamentoForm(request.POST)
        if form.is_valid():
            #anotacao = form.save(commit=False)            
            #anotacao.data = timezone.now()
            form.save()            
            return redirect('app:orcamento_list', filtro1='all', filtro2='all')
    else:
        form = OrcamentoForm()

    return render(request, 'app/orcamento_new.html', {'form': form})

def Orcamento_Edit(request, pk): 
    OrcamentoEdit = get_object_or_404(Orcamento, pk=pk)
    if request.method == 'POST':
        form = OrcamentoForm(request.POST, instance=OrcamentoEdit)

        if form.is_valid():
            form.save()
            return redirect('app:orcamento_detail', pk=pk)

    else:
        form = OrcamentoForm(instance=OrcamentoEdit)

    return render(request, 'app/orcamento_edit.html', {'form': form, 'orcamento':OrcamentoEdit})

def Orcamento_Detail(request, pk):        
    OrcamentoDetail = get_object_or_404(Orcamento, pk=pk)
    form = OrcamentoFormView(instance=OrcamentoDetail)
    return render(request, 'app/orcamento_detail.html', {'form': form, 'orcamento':OrcamentoDetail})

def Orcamento_List(request, filtro1, filtro2):    

    if filtro1 == 'all':
        filtro1 = ''        
    orcamento_list = Orcamento.objects.filter(empresa__contains=filtro1).order_by('empresa')
    if filtro2 != 'all':
        orcamento_list = orcamento_list.filter(categoria=filtro2).order_by('empresa')

    page    = request.GET.get('page', 1)
    paginator = Paginator(orcamento_list, 10)
    try:
        orcamentos = paginator.page(page)
    except PageNotAnInteger:
        orcamentos = paginator.page(1)
    except EmptyPage:
        orcamentos = paginator.page(paginator.num_pages)    

    categoria = Categoria.objects.all()

    return render(request, 'app/orcamento_list.html', {'orcamento_list': orcamentos,
                                                       'filtro1': filtro1,
                                                       'filtro2': filtro2,
                                                       'categoria': categoria})

def Orcamento_Filtro(request):
    filtro1 = request.POST.get('input_search', 'all')
    filtro2 = request.POST.get('id_categ', 'all')
    if filtro1 == '':
        filtro1 = 'all'
    
    return redirect('app:orcamento_list', filtro1=filtro1, filtro2=filtro2)

def Orcamento_Del(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)    
    form = OrcamentoFormView(instance=orcamento)
    if request.method=='POST':
        orcamento.delete()
        return redirect('app:orcamento_list', filtro1='all', filtro2='all')

    return render(request, 'app/orcamento_del.html', {'orcamento':orcamento, 'form': form})


def Pagamento_List(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)
    pagamento = Pagamento.objects.filter(orcamento=pk)
    
    return render(request, 'app/pagamento_list.html', {'orcamento':orcamento, 'pagamento': pagamento})

def Pagamento_List_All(request):    
    pagamento = Pagamento.objects.all()
    
    return render(request, 'app/pagamento_list_all.html', {'pagamento': pagamento})


def Pagamento_New(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)

    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)            
            pagamento.orcamento = orcamento
            pagamento.save()            
            return redirect('app:pagamento_detail', pk=pagamento.pk)
    else:
        form = PagamentoForm(initial={'valor_pagto': '0',
                                      'valor_desconto': '0',
                                      'valor_multa': '0',                                      
                                      'dt_pagto': timezone.now(),
                                      'dt_vencto': timezone.now(),
                                     })

    return render(request, 'app/pagamento_new.html', {'form': form, 'orcamento': orcamento})

def Pagamento_Detail(request, pk):        
    PagamentoDetail = get_object_or_404(Pagamento, pk=pk)
    orcamento = Orcamento.objects.get(pk=PagamentoDetail.orcamento_id)
    return render(request, 'app/pagamento_detail.html', {'pagamento':PagamentoDetail, 'orcamento': orcamento})

def Pagamento_Del(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)        
    orcamento = Orcamento.objects.get(pk=pagamento.orcamento_id)
    if request.method=='POST':
        pagamento.delete()
        return redirect('app:pagamento_list', pk=orcamento.pk)

    return render(request, 'app/pagamento_del.html', {'pagamento':pagamento, 'orcamento':orcamento})

def Pagamento_Edit(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)        
    orcamento = Orcamento.objects.get(pk=pagamento.orcamento_id)
    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=pagamento)

        if form.is_valid():
            form.save()
            return redirect('app:pagamento_detail', pk=pk)

    else:
        form = PagamentoForm(instance=pagamento)

    return render(request, 'app/pagamento_edit.html', {'form': form, 'pagamento':pagamento, 'orcamento': orcamento})


def Anexo_List(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)
    pagamento = Pagamento.objects.filter(orcamento=pk)
    
    return render(request, 'app/anexo_list.html', {'orcamento':orcamento, 'pagamento': pagamento})