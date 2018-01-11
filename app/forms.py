from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import Categoria, Orcamento, Pagamento

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
			raise ValidationError("A user with that email already exists.")			
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
	nome = forms.CharField(disabled=True)	
	descricao = forms.CharField(disabled=True)	
	class Meta:
		model = Categoria
		fields = (
		'nome',
		'descricao',		
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
	readonly_fields = ('orcamento',)
	class Meta:
		model = Pagamento
		fields = (
		'orcamento',
		'descricao',
		'dt_pagto',
		'dt_vencto',
		'valor_pagto',
		'valor_multa',
		'valor_desconto',		
		)