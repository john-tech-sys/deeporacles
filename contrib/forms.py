
from django import forms
from contrib.models import SearchTerm
from .models import *
from django.forms import ModelForm, TextInput, Textarea, FileInput
from django.utils.translation import gettext, gettext_lazy as _

class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchTerm
        fields = ('q',)
    q = forms.CharField(
        label= '', 
    )
    

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        default_text = 'Search for Posts'
        self.fields['q'].widget.attrs['value'] = default_text
        self.fields['q'].widget.attrs['onfocus'] = "if (this.value=='" + default_text + "')this.value = ''"

    include = ('q',)

    
class AllSearchForm(forms.ModelForm):
    class Meta:
        model = SearchTerm
        fields = ('q',)
    q = forms.CharField(
        label= '', 
    )

    def __init__(self, *args, **kwargs):
        super(AllSearchForm, self).__init__(*args, **kwargs)
        default_text = 'Search All'
        self.fields['q'].widget.attrs['value'] = default_text
        self.fields['q'].widget.attrs['class'] = 'form-control'
        self.fields['q'].widget.attrs['class'] = 'form-control-sm'
        self.fields['q'].widget.attrs['onfocus'] = "if (this.value=='" + default_text + "')this.value = ''"

    include = ('q',)


class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ('name', 'phone', 'email', 'message')

