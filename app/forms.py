from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

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