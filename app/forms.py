from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import Categoria, Orcamento, Pagamento, Anexo_Orcamento
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .fields import RestrictedFileField

class EditProfileForm(UserChangeForm):
	password = ReadOnlyPasswordHashField()
	class Meta:
		model = User
		fields = (
		'first_name',
		'last_name',
		'email',
		'password'
		)

class RegisterProfileForm(UserCreationForm):
	email = forms.EmailField(required=True)	
	
	class Meta:
		model = User
		fields = (
		'username',
		'email',
		'first_name',
		'last_name',
		'password1',
		'password2'
		)		

	def save(self, commit=True):
		user = super(RegisterProfileForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists() == True:
			raise ValidationError("Já existe outro usuário cadastrado com este e-mail.")			
		return email


class CategoriaForm(forms.ModelForm):	
	#descricao = forms.CharField(widget=forms.Textarea)
	class Meta:
		model = Categoria
		fields = (
		'nome',
		'descricao',		
		)

	#def clean_responsavel(self):
	#	responsavel = self.cleaned_data['responsavel']
	#	if Responsavel.objects.filter(responsavel=responsavel).exists() == False:
	#		raise ValidationError("Responsavel não cadastrado")			
	#	return responsavel

class CategoriaFormView(forms.ModelForm):	
	nome 			= forms.CharField(disabled=True)	
	descricao 		= forms.CharField(disabled=True)	
	dt_implant		= forms.CharField(disabled=True)	
	dt_ult_alter	= forms.CharField(disabled=True)	
	usuar_implant	= forms.CharField(disabled=True)	
	usuar_ult_alter	= forms.CharField(disabled=True)	
	class Meta:
		model = Categoria
		fields = (
		'nome',
		'descricao',	
		'dt_implant',	
		'dt_ult_alter',	   
		'usuar_implant',	   
		'usuar_ult_alter',	
		)	

class OrcamentoForm(forms.ModelForm):	
	
	class Meta:
		model = Orcamento
		fields = (
		'categoria',       
		'empresa',         
		'cidade',          
		'endereço',		
		'nome_contato',	
		'num_contato',		
		'valor_total',		
		'valor_multa',		
		'forma_pagto',		
		'dt_ult_pagto',    
		'dt_fim_contrato', 
		'dt_prox_reuniao',	
		'observacoes',
		'assinado',
		)

class OrcamentoFormView(forms.ModelForm):

	#categoria       = forms.ModelChoiceField(queryset=Categoria.objects.all())
	#categoria       = forms.ChoiceField(disabled=True)
	empresa         = forms.CharField(disabled=True)
	cidade          = forms.CharField(disabled=True)
	endereço        = forms.CharField(disabled=True)
	nome_contato    = forms.CharField(disabled=True)
	num_contato     = forms.CharField(disabled=True)
	valor_total     = forms.DecimalField(disabled=True)  
	valor_multa     = forms.DecimalField(disabled=True)   
	forma_pagto     = forms.CharField(disabled=True, widget=forms.Textarea)
	dt_ult_pagto    = forms.DateField(disabled=True) 
	dt_fim_contrato = forms.DateField(disabled=True) 
	dt_prox_reuniao = forms.DateField(disabled=True)
	observacoes     = forms.CharField(disabled=True, widget=forms.Textarea)

	class Meta:
		model = Orcamento
		fields = (
		'categoria',       
		'empresa',         
		'cidade',          
		'endereço',		
		'nome_contato',	
		'num_contato',		
		'valor_total',		
		'valor_multa',		
		'forma_pagto',		
		'dt_ult_pagto',    
		'dt_fim_contrato', 
		'dt_prox_reuniao',	
		'observacoes',				
		)

class PagamentoForm(forms.ModelForm):
	comprovante = RestrictedFileField(content_types=['image/jpeg','image/png', 'application/pdf'],
									  max_upload_size=8000000, 
									  required=False,									  
									  help_text='Arquivos válidos: jpg, png, pdf. Tamanho máximo: 8mb')
	class Meta:
		model = Pagamento
		fields = (		
		'descricao',
		'dt_pagto',		
		'valor_pagto',		
		'comprovante',
		)

class AnexoForm(forms.ModelForm):
	file_name = RestrictedFileField(content_types=['image/jpeg','image/png', 'application/pdf'],
									max_upload_size=8000000, 
									help_text='Arquivos válidos: jpg, png, pdf. Tamanho máximo: 8mb')
	class Meta:
		model = Anexo_Orcamento
		fields = (		
		'descricao',
		'file_name',		
		)