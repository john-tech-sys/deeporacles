
from django import forms
from .models import *

from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, FileInput


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, help_text='100 characters maximum')
    email = forms.EmailField(required=True)
    comment = forms.CharField(required=True, widget=forms.Textarea)


class Admin_MessageForm(forms.ModelForm):
	content = forms.CharField(required=False ,max_length=255)
	class Meta:
		model=Admin_Message
		fields = ('content', 'details')

	def clean(self):
		if not self.cleaned_data['content']:
			raise ValidationError("You must specify either content")
