from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import Categoria, Orcamento, Pagamento
from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


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

class RestrictedFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop('content_types', None)
        self.max_upload_size = kwargs.pop('max_upload_size', None)
        if not self.max_upload_size:
            self.max_upload_size = settings.MAX_UPLOAD_SIZE
        super(RestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(RestrictedFileField, self).clean(*args, **kwargs)
        try:
            if data.content_type in self.content_types:
                if data.size > self.max_upload_size:
                    raise forms.ValidationError(_('File size must be under %s. Current file size is %s.') % (filesizeformat(self.max_upload_size), filesizeformat(data.size)))
            else:
                raise forms.ValidationError(_('File type (%s) is not supported.') % data.content_type)
        except AttributeError:
            pass

        return data

class PagamentoForm(forms.ModelForm):
	comprovante = RestrictedFileField(content_types=['image/jpeg','image/png', 'application/pdf'], max_upload_size=2621440)
	class Meta:
		model = Pagamento
		fields = (		
		'descricao',
		'dt_pagto',
		'dt_vencto',
		'valor_pagto',
		'valor_multa',
		'valor_desconto',		
		'comprovante',
		)


