from django.conf.urls import url
from django.contrib.auth.views import (
	login,
	logout,
	password_reset,
	password_reset_done,
	password_reset_confirm,
	password_reset_complete,
	)

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.Home, name='home'),
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),        
    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}, name='logout'), 
    url(r'^profile/$', views.Profile , name='profile'),
    url(r'^profile/edit/$', views.Edit_profile , name='edit_profile'),
    url(r'^register/$', views.Register , name='register'),
    url(r'^change-password/$', views.Change_Password , name='change_password'),    
    url(r'^reset-password/$', password_reset, {'template_name': 'accounts/reset_password.html',
    										   'post_reset_redirect': 'app:password_reset_done', 
    										   'email_template_name': 'accounts/reset_password_email.html'},
    										    name='reset_password'),
    url(r'^reset-password/done/$', password_reset_done, {'template_name': 'accounts/reset_password_done.html'},
    													  name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
												password_reset_confirm,
												{'template_name': 'accounts/reset_password_confirm.html',
												 'post_reset_redirect': 'app:password_reset_complete'},
												  name='password_reset_confirm'),
    url(r'^reset-password/complete/$', password_reset_complete,{'template_name': 'accounts/reset_password_complete.html'},
                                                                 name='password_reset_complete'),
    url(r'^categoria/cadastra/$', views.Categoria_New , name='categoria_new'),
    url(r'^categoria/lista/(?P<filtro>\w+)/$', views.Categoria_List , name='categoria_list'),
    url(r'^categoria/filtro/$', views.Categoria_Filtro , name='categoria_filtro'),
    url(r'^categoria/(?P<pk>\d+)/detalhe/$', views.Categoria_Detail , name='categoria_detail'),
    url(r'^categoria/(?P<pk>\d+)/edita/$', views.Categoria_Edit , name='categoria_edit'),
    url(r'^categoria/(?P<pk>\d+)/delete/$', views.Categoria_Del , name='categoria_del'),
    url(r'^orcamento/cadastra/$', views.Orcamento_New , name='orcamento_new'),
    url(r'^orcamento/lista/(?P<filtro>\w+)/$', views.Orcamento_List , name='orcamento_list'),
    url(r'^orcamento/filtro/$', views.Orcamento_Filtro , name='orcamento_filtro'),
    url(r'^orcamento/(?P<pk>\d+)/detalhe/$', views.Orcamento_Detail , name='orcamento_detail'),
    url(r'^orcamento/(?P<pk>\d+)/edita/$', views.Orcamento_Edit , name='orcamento_edit'),
    url(r'^orcamento/(?P<pk>\d+)/delete/$', views.Orcamento_Del , name='orcamento_del'),
    
]
