from django.forms import ModelForm
from .models import Post
from django import forms
from tinymce.widgets import TinyMCE

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = '__all__'

class RawPostForm(forms.Form):
    title       = forms.CharField(label='Enter Title', max_length=255, widget=forms.TextInput(attrs={'placeholder':'Enter a Title...'}))
    content     = forms.CharField(widget = TinyMCE())
    summary     = forms.CharField(required=False)
    image       = forms.ImageField()
    