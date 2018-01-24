from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
import os
import uuid

class Categoria(models.Model):
	nome 			= models.CharField(max_length=20)
	descricao 		= models.CharField(max_length=800)    
	dt_implant 		= models.DateField(blank=True, null=True)   
	dt_ult_alter	= models.DateField(blank=True, null=True)   
	usuar_implant	= models.CharField(max_length=40, blank=True)
	usuar_ult_alter	= models.CharField(max_length=40, blank=True)
	def __str__(self):
		return self.nome

class Orcamento(models.Model):    
	categoria       = models.ForeignKey('Categoria', on_delete=models.CASCADE)
	empresa         = models.CharField(max_length=40)
	cidade          = models.CharField(max_length=40, blank=True)
	endereço		= models.CharField(max_length=80, blank=True)
	nome_contato	= models.CharField(max_length=40, blank=True)
	num_contato		= models.CharField(max_length=40, blank=True)
	valor_total		= models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)   
	valor_saldo     = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)   
	valor_multa		= models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)   
	forma_pagto		= models.TextField(blank=True)   
	dt_ult_pagto    = models.DateField(blank=True, null=True)   
	dt_fim_contrato = models.DateField(blank=True, null=True)   
	dt_prox_reuniao	= models.DateField(blank=True, null=True)   
	observacoes		= models.TextField(blank=True)
	dt_implant      = models.DateField(blank=True, null=True)   
	dt_ult_alter    = models.DateField(blank=True, null=True)   
	usuar_implant   = models.CharField(max_length=40, blank=True)
	usuar_ult_alter = models.CharField(max_length=40, blank=True)
	assinado        = models.BooleanField(default=False)
	dt_assinado     = models.DateField(blank=True, null=True)   
	def __str__(self):
		return self.empresa	

	def RecalculaSaldo(self):
		from .models import (Pagamento)
		pagamento = Pagamento.objects.filter(orcamento_id=self.pk)
		tot_pago = 0
		for i in pagamento:
			if i.valor_pagto != None:
				tot_pago = tot_pago + i.valor_pagto
		if self.valor_total != None and tot_pago != None:
			self.valor_saldo = self.valor_total - tot_pago
			self.save()

class Pagamento(models.Model):
	orcamento 		= models.ForeignKey('Orcamento', on_delete=models.CASCADE)
	descricao 		= models.CharField(max_length=40)
	dt_pagto 		= models.DateField(blank=True, null=True)
	dt_vencto 		= models.DateField(blank=True, null=True)
	valor_pagto 	= models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
	valor_multa 	= models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
	valor_desconto 	= models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
	comprovante     = models.FileField(upload_to='comprovantes/', blank=True, null=True)
	dt_implant      = models.DateField(blank=True, null=True)   
	dt_ult_alter    = models.DateField(blank=True, null=True)   
	usuar_implant   = models.CharField(max_length=40, blank=True)
	usuar_ult_alter = models.CharField(max_length=40, blank=True)
	def __str__(self):
		return self.descricao

class Anexo_Orcamento(models.Model):
	orcamento 		= models.ForeignKey('Orcamento', on_delete=models.CASCADE)
	descricao       = models.CharField(max_length=40, blank=True)
	file_name 		= models.FileField(upload_to='orcamento/')
	dt_implant      = models.DateField(blank=True, null=True)   
	dt_ult_alter    = models.DateField(blank=True, null=True)   
	usuar_implant   = models.CharField(max_length=40, blank=True)
	usuar_ult_alter = models.CharField(max_length=40, blank=True)

@receiver(models.signals.post_delete, sender=Pagamento)
def delete_file_on_del_pagto(sender, instance, **kwargs):    
    if instance.comprovante:
        if os.path.isfile(instance.comprovante.path):
            os.remove(instance.comprovante.path)

@receiver(models.signals.pre_save, sender=Pagamento)
def delete_file_on_change_pagto(sender, instance, **kwargs):    
    if not instance.pk:
        return False

    try:
        old_file = Pagamento.objects.get(pk=instance.pk).comprovante
    except Pagamento.DoesNotExist:
        return False

    new_file = instance.comprovante
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

@receiver(models.signals.post_delete, sender=Anexo_Orcamento)
def delete_file_on_del_anexo(sender, instance, **kwargs):    
    if instance.file_name:
        if os.path.isfile(instance.file_name.path):
            os.remove(instance.file_name.path)

@receiver(models.signals.pre_save, sender=Anexo_Orcamento)
def delete_file_on_change_anexo(sender, instance, **kwargs):    
    if not instance.pk:
        return False

    try:
        old_file = Anexo_Orcamento.objects.get(pk=instance.pk).file_name
    except Anexo_Orcamento.DoesNotExist:
        return False

    new_file = instance.file_name
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)