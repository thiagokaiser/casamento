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
    )
from .models import (    
    Categoria,
    Orcamento,
    )
from django.contrib.postgres.search import SearchVector

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
    
    categoria_list = Categoria.objects.filter(nome__contains=filtro)

    paginator = Paginator(categoria_list, 10)
    try:
        categorias = paginator.page(page)
    except PageNotAnInteger:
        categorias = paginator.page(1)
    except EmptyPage:
        categorias = paginator.page(paginator.num_pages)    

    return render(request, 'app/categoria_list.html', { 'categoria_list': categorias })

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
        return redirect('app:categoria_list')

    return render(request, 'app/categoria_del.html', {'categoria':categoria, 'form': form})

def Orcamento_New(request):
    if request.method == 'POST':
        form = OrcamentoForm(request.POST)
        if form.is_valid():
            #anotacao = form.save(commit=False)            
            #anotacao.data = timezone.now()
            form.save()            
            return redirect('app:home')
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

def Orcamento_List(request, filtro):    
    #categoria_list = Categoria.objects.all()
    if filtro == 'all':
        filtro = ''

    page    = request.GET.get('page', 1)
    
    orcamento_list = Orcamento.objects.filter(empresa__contains=filtro)

    paginator = Paginator(orcamento_list, 10)
    try:
        orcamentos = paginator.page(page)
    except PageNotAnInteger:
        orcamentos = paginator.page(1)
    except EmptyPage:
        orcamentos = paginator.page(paginator.num_pages)    

    return render(request, 'app/orcamento_list.html', { 'orcamento_list': orcamentos })

def Orcamento_Filtro(request):
    filtro = request.POST.get('input_search', 'all')
    if filtro == '':
        filtro = 'all'
    
    return redirect('app:orcamento_list', filtro=filtro)

def Orcamento_Del(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)    
    form = OrcamentoFormView(instance=orcamento)
    if request.method=='POST':
        orcamento.delete()
        return redirect('app:orcamento_list')

    return render(request, 'app/orcamento_del.html', {'orcamento':orcamento, 'form': form})