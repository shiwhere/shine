from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


@deconstructible
class RusValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Only rus language is allowed'


    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, self.code)


class AddPostForm(forms.ModelForm):

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Category", empty_label='category not choised')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label="Husband", empty_label='dont marryed')

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo','is_published', 'cat', 'husband', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols':50, 'rows':5}),
        }
        labels = {
            'slug':'URL'
        }
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Title too long')
        return title


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Upload file')

    class Meta:
        model = Women
        fields = ['file']