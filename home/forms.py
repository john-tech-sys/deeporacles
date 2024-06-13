
from django import forms
from froala_editor.widgets import FroalaEditor    
from contrib.models import Comment
from .models import Post

class PostCreateForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=FroalaEditor(
            attrs={
                'class': 'form-control ',
            }
        )
    )
    class Meta:
        model = Post
        fields = ('title', 'picture', 'Video_file', 'Audio_file', 'content', 'forum', 'space')
        widgets = {
            'picture': forms.FileInput(),  # Make picture field not required
        }

    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False

 

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=FroalaEditor(
            attrs={
                'class': 'px-4 border border-secondary border-rounded w-100 ',
                'placeholder': 'Write your Response',
                'rows': '2'
            }
        )
    )
    class Meta:
        model = Comment
        fields = ['comment']



