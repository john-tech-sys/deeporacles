
from django import forms
from froala_editor.widgets import FroalaEditor  
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('user_input',)



