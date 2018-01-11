from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=20)
    descricao = models.CharField(max_length=800)    
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
	valor_multa		= models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)   
	forma_pagto		= models.TextField(blank=True)   
	dt_ult_pagto    = models.DateField(blank=True, null=True)   
	dt_fim_contrato = models.DateField(blank=True, null=True)   
	dt_prox_reuniao	= models.DateField(blank=True, null=True)   
	observacoes		= models.TextField(blank=True)
	def __str__(self):
		return self.empresa

class Pagamento(models.Model):
	orcamento 		= models.ForeignKey('Orcamento', on_delete=models.CASCADE)
	descricao 		= models.CharField(max_length=40)
	dt_pagto 		= models.DateField(blank=True, null=True)
	dt_vencto 		= models.DateField(blank=True, null=True)
	valor_pagto 	= models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
	valor_multa 	= models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
	valor_desconto 	= models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
	def __str__(self):
		return self.descricao