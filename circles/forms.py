from django import forms
from .models import *



class ForumForm(forms.ModelForm):
	forum_bio = forms.CharField(
		widget=forms.Textarea(
			attrs={
				'class': 'form-control mr-4',
			}
		)
	)
	# picture = forms.CharField(
	# 	widget=forms.FileInput(
	# 		attrs={
	# 			'class': 'form-control mr-4',
	# 			'placeholder': 'Upload Forum picture',
	# 		}
	# 	)
	# )
	# forum_cover_photo = forms.CharField(
	# 	widget=forms.FileInput(
	# 		attrs={
	# 			'class': 'form-control mr-4',
	# 			'placeholder': 'Upload Forum Wall Image',
	# 		}
	# 	)
	# )
	forum_name = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control mr-4',
				'placeholder': 'Write your comment',
			}
		)
	)
	class Meta:
		model = Forum
		fields = ('forum_name', 'picture', 'forum_cover_photo', 'forum_bio')

