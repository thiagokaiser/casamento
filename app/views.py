from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import date
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
from django.contrib.postgres.search import SearchVector
from django.utils import timezone
from django.db.models import Sum, Q, Count
from django.db.models.functions import Lower
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import (    
    EditProfileForm,
    RegisterProfileForm,    
    CategoriaForm,
    CategoriaFormView,
    OrcamentoForm,
    OrcamentoFormView,
    PagamentoForm,
    AnexoForm,
    )
from .models import (    
    Categoria,
    Orcamento,
    Pagamento,
    Anexo_Orcamento,
    )
from .funcoes import funcao_data, gera_excel
import csv
import itertools

# Create your views here.
def Home(request):

    orcamentos = Orcamento.objects.all()
    pagamentos = Pagamento.objects.all().order_by('dt_pagto')
    
    home = dict()
        
    #----- GERAR GRAFICO BARRA ----------    
    pagtomes = Pagamento.objects.values('dt_pagto','valor_pagto').order_by('dt_pagto')
    pagtomesgrp = itertools.groupby(pagtomes, lambda d: d.get('dt_pagto').strftime('%Y-%m'))    
    pagtomesresult = [{'mes': month, 'valor': sum([x['valor_pagto'] for x in this_day])} 
        for month, this_day in pagtomesgrp]

    teste = funcao_data(11)
    newdict = dict()
    arraydict = []

    for arraydata in teste:
        mes = arraydata.strftime('%Y-%m')
        valor = 0
        for i in pagtomesresult:        
            if mes == i['mes']:
                valor = i['valor']        
        newdict = {'mes': mes , 'valor': valor}
        arraydict.append(newdict)    

    home['pagtomes'] = arraydict
    #------------------------------------

    today = date.today()    
    home['prox_reuniao'] = orcamentos.filter(dt_prox_reuniao__gte=today).order_by('dt_prox_reuniao')[:10]
    home['ult_orcamen'] = orcamentos.order_by('dt_implant')[:10]
    home['ult_pagto'] = pagamentos.order_by('dt_pagto')[:10]

    for i in home.get('prox_reuniao'):
        i.data = (i.dt_prox_reuniao - today).days
        if i.data <= 5:
            i.label_data = 'label-danger'
        elif i.data <= 10:
            i.label_data = 'label-warning'
        else:
            i.label_data = 'label-success'

    
    #----- GERAR GRAFICO PIZZA ----------    
    listacor = ['#f56954','#00a65a','#f39c12','#00c0ef','#3c8dbc','#3366CC','#DC3912','#FF9900','#109618','#990099','#3B3EAC','#0099C6',
                '#DD4477','#66AA00','#B82E2E','#316395','#994499','#22AA99','#AAAA11','#6633CC','#E67300','#8B0707','#329262','#5574A6','#3B3EAC']

    orcamentos = orcamentos.filter(assinado=True)
    i = 0
    for orcamento in orcamentos:
        if orcamento.valor_total == None:
            orcamento.valor_total = 0
        home['total'] = home.get('total', 0) + orcamento.valor_total
        i = i + 1
        orcamento.cor = listacor[i]
    #------------------------------------ 

    for pagamento in pagamentos:
        home['pagto'] = home.get('pagto', 0) + pagamento.valor_pagto               
    home['orcamentos'] = orcamentos
    if home.get('total', 0) != 0:
        home['percent'] =  round((home.get('pagto', 0) * 100) / home.get('total', 0), 0)
    else:
        home['percent'] =  0
    home['dias'] = abs(date(2019, 9, 21) - date.today())

    args = {'home': home} 
    return render(request, 'app/home.html', args)

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
                messages.success(request, "Usuário criado com sucesso", extra_tags='alert alert-success alert-dismissible')            
                return redirect('app:profile')                    
        else:
            messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert alert-error alert-dismissible')            
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

    if not request.user.has_perm('app.add_categoria'):
        messages.error(request, "Usuário sem permissao para adicionar", extra_tags='alert alert-error alert-dismissible')            
        return redirect('app:categoria_list', filtro='all')

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)                        
            categoria.dt_implant        = timezone.now()
            categoria.dt_ult_alter      = timezone.now()
            categoria.usuar_implant     = request.user.username
            categoria.usuar_ult_alter   = request.user.username
            categoria.save()            
            messages.success(request, "Categoria adicionada com sucesso.", extra_tags='alert alert-success alert-dismissible')
            return redirect('app:categoria_list', filtro='all')
    else:
        form = CategoriaForm()

    return render(request, 'app/categoria_new.html', {'form': form})

def Categoria_Edit(request, pk): 
    CategoriaEdit = get_object_or_404(Categoria, pk=pk)

    if not request.user.has_perm('app.change_categoria'):
        messages.error(request, "Usuário sem permissao para alterar", extra_tags='alert alert-error alert-dismissible')            
        return redirect('app:categoria_detail', pk=CategoriaEdit.pk)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=CategoriaEdit)

        if form.is_valid():            
            categoriasave = form.save(commit=False)                        
            categoriasave.dt_ult_alter      = timezone.now()            
            categoriasave.usuar_ult_alter   = request.user.username
            categoriasave.save()
            messages.success(request, "Categoria editada com sucesso.", extra_tags='alert alert-success alert-dismissible')
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

    if not request.user.has_perm('app.del_orcamento'):
        messages.error(request, "Usuário sem permissao para deletar", extra_tags='alert alert-error alert-dismissible')            
        return redirect('app:categoria_detail', pk=categoria.pk)

    form = CategoriaFormView(instance=categoria)
    if request.method=='POST':
        categoria.delete()
        messages.success(request, "Categoria eliminada com sucesso.", extra_tags='alert alert-success alert-dismissible')
        return redirect('app:categoria_list', filtro='all')

    return render(request, 'app/categoria_del.html', {'categoria':categoria, 'form': form})

def Orcamento_New(request):

    if not request.user.has_perm('app.add_orcamento'):
        messages.error(request, "Usuário sem permissao para adicionar", extra_tags='alert alert-error alert-dismissible')            
        return redirect('app:orcamento_list', filtro1='all', filtro2='all')

    if request.method == 'POST':
        form = OrcamentoForm(request.POST)
        if form.is_valid():
            orcamento = form.save(commit=False)                        
            orcamento.dt_implant        = timezone.now()
            orcamento.dt_ult_alter      = timezone.now()
            orcamento.usuar_implant     = request.user.username
            orcamento.usuar_ult_alter   = request.user.username
            if orcamento.assinado == True:
                orcamento.dt_assinado = timezone.now()            
            else:
                orcamento.dt_assinado = None
            orcamento.save()            
            messages.success(request, "Orcamento adicionado com sucesso.", extra_tags='alert alert-success alert-dismissible')
            return redirect('app:orcamento_list', filtro1='all', filtro2='all')
    else:
        form = OrcamentoForm(initial={'valor_total': '0',
                                      'valor_multa': '0',                                                                            
                                     })

    return render(request, 'app/orcamento_new.html', {'form': form})

def Orcamento_Edit(request, pk): 
    OrcamentoEdit = get_object_or_404(Orcamento, pk=pk)

    if not request.user.has_perm('app.change_orcamento'):
        messages.error(request, "Usuário sem permissao para alterar", extra_tags='alert alert-error alert-dismissible')            
        return redirect('app:orcamento_detail', pk=OrcamentoEdit.pk)

    if request.method == 'POST':
        form = OrcamentoForm(request.POST, instance=OrcamentoEdit)

        if form.is_valid():
            orcamentosave = form.save(commit=False)                        
            orcamentosave.dt_ult_alter      = timezone.now()            
            orcamentosave.usuar_ult_alter   = request.user.username
            if orcamentosave.assinado == True:
                orcamentosave.dt_assinado = timezone.now()            
            else:
                orcamentosave.dt_assinado = None
            orcamentosave.save()
            messages.success(request, "Orcamento editado com sucesso.", extra_tags='alert alert-success alert-dismissible')
            return redirect('app:orcamento_detail', pk=pk)

    else:
        form = OrcamentoForm(instance=OrcamentoEdit)

    return render(request, 'app/orcamento_edit.html', {'form': form, 'orcamento':OrcamentoEdit})

def Orcamento_Detail(request, pk):        
    OrcamentoDetail = get_object_or_404(Orcamento, pk=pk)    
    form = OrcamentoFormView(instance=OrcamentoDetail)
    return render(request, 'app/orcamento_detail.html', {'form': form, 'orcamento':OrcamentoDetail})

def Orcamento_List(request, filtro1, filtro2):    
    page              = request.GET.get('page', 1)  
    filtro_empresa    = request.GET.get('input_search', '')    
    filtro_categ      = request.GET.get('id_categ', 'all')    
    reg_pag           = request.GET.get('reg_pag', 10)    
    order_orc         = request.GET.get('order_orc', 'empresa')  

    filtro_url = '?input_search=' + filtro_empresa + '&id_categ=' + filtro_categ + '&reg_pag=' + str(reg_pag) + '&order_orc=' + order_orc
    filtro = {'url': filtro_url,
              'filtro1': filtro_empresa,
              'filtro2': filtro_categ,
              'pag': reg_pag,
              'order_orc': order_orc
              }    
    
    if order_orc[:1] == '-':
        order_orc = order_orc[1:]
        orcamento_list = Orcamento.objects.filter(empresa__contains=filtro_empresa).order_by(Lower(order_orc).desc())
    else:
        orcamento_list = Orcamento.objects.filter(empresa__contains=filtro_empresa).order_by(Lower(order_orc))
    if filtro_categ != 'all':
        orcamento_list = orcamento_list.filter(categoria=filtro_categ)
    
    paginator = Paginator(orcamento_list, reg_pag)
    try:
        orcamentos = paginator.page(page)
    except PageNotAnInteger:
        orcamentos = paginator.page(1)
    except EmptyPage:
        orcamentos = paginator.page(paginator.num_pages)    

    categoria = Categoria.objects.all()

    return render(request, 'app/orcamento_list.html', {'orcamento_list': orcamentos,
                                                       'filtro': filtro,                                                       
                                                       'categoria': categoria})


def Orcamento_Del(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)    

    if not request.user.has_perm('app.del_orcamento'):
        messages.error(request, "Usuário sem permissao para deletar", extra_tags='alert alert-error alert-dismissible')            
        return redirect('app:orcamento_detail', pk=orcamento.pk)

    form = OrcamentoFormView(instance=orcamento)
    if request.method=='POST':
        orcamento.delete()
        messages.success(request, "Orçamento eliminado com sucesso.", extra_tags='alert alert-success alert-dismissible')
        return redirect('app:orcamento_list', filtro1='all', filtro2='all')

    return render(request, 'app/orcamento_del.html', {'orcamento':orcamento, 'form': form})


def Pagamento_List(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)
    pagamento = Pagamento.objects.filter(orcamento=pk)    
    
    return render(request, 'app/pagamento_list.html', {'orcamento':orcamento, 'pagamento': pagamento})

def Pagamento_List_All(request):    
    orcamento = Orcamento.objects.all()    
    filtro_descricao  = request.GET.get('input_search', '')
    filtro_empresa    = request.GET.get('id_orcto', 'all')
    reg_pag           = request.GET.get('reg_pag', 10)    
    order_pagto       = request.GET.get('order_pagto', 'orcamento')  

    filtro_url = '?input_search=' + filtro_descricao + '&id_orcto=' + filtro_empresa + '&reg_pag=' + str(reg_pag) + '&order_pagto=' + order_pagto
    filtro = {'url': filtro_url,
              'filtro1': filtro_descricao,
              'filtro2': filtro_empresa,
              'pag': reg_pag,
              'order_pagto': order_pagto
              }

    order_pagto = '-' + order_pagto
    pagamento = Pagamento.objects.filter(descricao__contains=filtro_descricao).order_by(order_pagto)    
    if filtro_empresa != 'all':
        pagamento = pagamento.filter(orcamento=filtro_empresa)


    page    = request.GET.get('page', 1)    

    paginator = Paginator(pagamento, reg_pag)
    try:
        pagamentos = paginator.page(page)
    except PageNotAnInteger:
        pagamentos = paginator.page(1)
    except EmptyPage:
        pagamentos = paginator.page(paginator.num_pages)    
    
    return render(request, 'app/pagamento_list_all.html', {'pagamento': pagamentos, 'orcamento': orcamento, 'filtro': filtro})

def Pagamento_New(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)

    if not request.user.has_perm('app.add_pagamento'):
        messages.error(request, "Usuário sem permissao para adicionar", extra_tags='alert alert-error alert-dismissible')            
        return redirect('app:pagamento_list', pk=orcamento.pk)

    if request.method == 'POST':
        form = PagamentoForm(request.POST, request.FILES)        
        if form.is_valid():
            pagamento = form.save(commit=False)   
            pagamento.orcamento         = orcamento
            pagamento.dt_implant        = timezone.now()
            pagamento.dt_ult_alter      = timezone.now()
            pagamento.usuar_implant     = request.user.username
            pagamento.usuar_ult_alter   = request.user.username
            pagamento.save()            
            orcamento.RecalculaSaldo()
            messages.success(request, "Pagamento adicionado com sucesso.", extra_tags='alert alert-success alert-dismissible')
            return redirect('app:pagamento_detail', pk=pagamento.pk)
        else:
            messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert alert-error alert-dismissible')
    else:
        form = PagamentoForm(initial={'valor_pagto': '0',
                                      'dt_pagto': timezone.now(),                                      
                                     })

    return render(request, 'app/pagamento_new.html', {'form': form, 'orcamento': orcamento})

def Pagamento_Detail(request, pk):        
    PagamentoDetail = get_object_or_404(Pagamento, pk=pk)
    orcamento = Orcamento.objects.get(pk=PagamentoDetail.orcamento_id)
    return render(request, 'app/pagamento_detail.html', {'pagamento':PagamentoDetail, 'orcamento': orcamento})

def Pagamento_Del(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)        
    orcamento = Orcamento.objects.get(pk=pagamento.orcamento_id)

    if not request.user.has_perm('app.del_pagamento'):
        messages.error(request, "Usuário sem permissao para excluir", extra_tags='alert alert-error alert-dismissible')            
        return redirect('app:pagamento_detail', pk=pagamento.pk)

    if request.method=='POST':
        pagamento.delete()
        orcamento.RecalculaSaldo()
        messages.success(request, "Pagamento eliminado com sucesso.", extra_tags='alert alert-success alert-dismissible')
        return redirect('app:pagamento_list', pk=orcamento.pk)

    return render(request, 'app/pagamento_del.html', {'pagamento':pagamento, 'orcamento':orcamento})

def Pagamento_Edit(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)        
    orcamento = Orcamento.objects.get(pk=pagamento.orcamento_id)

    if not request.user.has_perm('app.change_pagamento'):
        messages.error(request, "Usuário sem permissao para alterar", extra_tags='alert alert-error alert-dismissible')            
        return redirect('app:pagamento_detail', pk=pagamento.pk)

    if request.method == 'POST':
        form = PagamentoForm(request.POST, request.FILES, instance=pagamento)

        if form.is_valid():            
            pagamentosave = form.save(commit=False)                        
            pagamentosave.dt_ult_alter      = timezone.now()            
            pagamentosave.usuar_ult_alter   = request.user.username
            pagamentosave.save()
            orcamento.RecalculaSaldo()
            messages.success(request, "Pagamento editado com sucesso.", extra_tags='alert alert-success alert-dismissible')            
            return redirect('app:pagamento_detail', pk=pk)           
        else:
            messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert alert-error alert-dismissible')            

    else:        
        form = PagamentoForm(instance=pagamento)

    return render(request, 'app/pagamento_edit.html', {'form': form, 'pagamento':pagamento, 'orcamento': orcamento})

def Anexo_List(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)
    anexos = Anexo_Orcamento.objects.filter(orcamento=pk)    
    
    return render(request, 'app/anexo_list.html', {'orcamento':orcamento, 'anexos': anexos})

def Anexo_New(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)    

    if not request.user.has_perm('app.add_anexo_orcamento'):
        messages.error(request, "Usuário sem permissao para adicionar", extra_tags='alert alert-error alert-dismissible')            
        return redirect('app:anexo_list', pk=orcamento.pk)

    if request.method == 'POST':
        form = AnexoForm(request.POST, request.FILES)        
        if form.is_valid():
            anexo = form.save(commit=False)   
            anexo.orcamento         = orcamento
            anexo.dt_implant        = timezone.now()
            anexo.dt_ult_alter      = timezone.now()
            anexo.usuar_implant     = request.user.username
            anexo.usuar_ult_alter   = request.user.username
            anexo.save()            
            messages.success(request, "Anexo adicionado com sucesso.", extra_tags='alert alert-success alert-dismissible')
            return redirect('app:anexo_detail', pk=anexo.pk)
        else:
            messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert alert-error alert-dismissible')
    else:
        form = AnexoForm()

    return render(request, 'app/anexo_new.html', {'form': form, 'orcamento': orcamento})    

def Anexo_Detail(request, pk):        
    anexo = get_object_or_404(Anexo_Orcamento, pk=pk)
    orcamento = Orcamento.objects.get(pk=anexo.orcamento_id)
    return render(request, 'app/anexo_detail.html', {'anexo':anexo, 'orcamento': orcamento})

def Anexo_Del(request, pk):
    anexo = get_object_or_404(Anexo_Orcamento, pk=pk)        
    orcamento = Orcamento.objects.get(pk=anexo.orcamento_id)

    if not request.user.has_perm('app.del_pagamento'):
        messages.error(request, "Usuário sem permissao para excluir", extra_tags='alert alert-error alert-dismissible')            
        return redirect('app:anexo_detail', pk=anexo.pk)

    if request.method=='POST':
        anexo.delete()
        messages.success(request, "Anexo eliminado com sucesso.", extra_tags='alert alert-success alert-dismissible')
        return redirect('app:anexo_list', pk=orcamento.pk)

    return render(request, 'app/anexo_del.html', {'anexo':anexo, 'orcamento':orcamento})

def Anexo_Edit(request, pk):
    anexo = get_object_or_404(Anexo_Orcamento, pk=pk)        
    orcamento = Orcamento.objects.get(pk=anexo.orcamento_id)

    if not request.user.has_perm('app.change_anexo_orcamento'):
        messages.error(request, "Usuário sem permissao para alterar", extra_tags='alert alert-error alert-dismissible')            
        return redirect('app:anexo_detail', pk=anexo.pk)

    if request.method == 'POST':
        form = AnexoForm(request.POST, request.FILES, instance=anexo)

        if form.is_valid():            
            anexosave = form.save(commit=False)                        
            anexosave.dt_ult_alter      = timezone.now()            
            anexosave.usuar_ult_alter   = request.user.username
            anexosave.save()
            messages.success(request, "Anexo editado com sucesso.", extra_tags='alert alert-success alert-dismissible')            
            return redirect('app:anexo_detail', pk=pk)           
        else:
            messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert alert-error alert-dismissible')
    else:        
        form = AnexoForm(instance=anexo)

    return render(request, 'app/anexo_edit.html', {'form': form, 'anexo':anexo, 'orcamento': orcamento})


def Pagamento_CSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pagamentos.csv"'

    writer = csv.writer(response, delimiter=';')    
    writer.writerow(['orcamento',
                     'descricao',       
                     'dt_pagto',                             
                     'valor_pagto',                          
                     'dt_implant',     
                     'dt_ult_alter',   
                     'usuar_implant',  
                     'usuar_ult_alter',
                    ])

    pagamentos = Pagamento.objects.all().values_list('orcamento',
                                                     'descricao',       
                                                     'dt_pagto',                                                             
                                                     'valor_pagto',                                                          
                                                     'dt_implant',     
                                                     'dt_ult_alter',   
                                                     'usuar_implant',  
                                                     'usuar_ult_alter',
                                                    )
    for pagamento in pagamentos:
        writer.writerow(pagamento)

    return response

def Gera_XLS(request):
    orcamentos = Orcamento.objects.all()

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
    xlsx_data = gera_excel(orcamentos)
    response.write(xlsx_data)
    return response

def Side_Menu(request):
    if request.session.get('menu_aberto') != '':
        request.session['menu_aberto'] = not(request.session.get('menu_aberto'))

    return HttpResponse('')