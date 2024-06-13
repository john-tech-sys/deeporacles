from django import forms
from django.forms import ModelForm
from .models import *
from django.utils.translation import gettext, gettext_lazy as _

class EducationForm(forms.ModelForm):
	period = forms.CharField(
        label='',
		widget=forms.TextInput(
			attrs={
				'class': 'form-control ','placeholder': 'Write your period',
			}
		)
	)
	qualification = forms.CharField(
        label='',
		widget=forms.TextInput(
			attrs={
				'class': 'form-control ','placeholder': 'Write your qualification',
			}
		)
	)
	institution = forms.CharField(
        label='',
		widget=forms.TextInput(
			attrs={
				'class': 'form-control ','placeholder': 'Write your institution',
			}
		)
	)
	class Meta:
		model = Education
		fields = ('institution', 'qualification', 'period', 'is_highest_level', 'is_active')

class SkillForm(forms.ModelForm):
	class Meta:
		model = Skill
		fields = ('title', 'score', 'details', 'image', 'is_active', 'is_key_skill')

class FileForm(forms.ModelForm):
	class Meta:
		model = Files
		fields = ('title', 'image', 'document')

class PotfolioForm(forms.ModelForm):
	class Meta:
		model = Potfolio
		fields = ('title', 'image', 'description', 'details')

# Profile Updates


class ProfilePictureForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProfilePictureForm, self).__init__(*args, **kwargs)
		self.fields['picture'].widget.attrs.update(
			{'class': '', 'id': ''})

	picture = forms.ImageField(label='')

	class Meta:
		model = Profile
		fields = ['picture']

class ProfileWallForm(forms.ModelForm):
	image = forms.ImageField(label='')

	class Meta:
		model = Profile
		fields = ['image']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('first_name', 'middle_name', 'last_name', 'picture', 'image', 'gender', 'phone', 'email', 'birth_date', 'bio')


class EditUserForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs.update(
            {'class': 'form_edit_user', 'name': 'gender'})
        self.fields['image'].widget.attrs.update(
            {'class': 'field field__file', 'type': 'file', 'id': 'field__file-2'})

    class Meta:
        model = Profile
        fields = ['gender', 'image']
