from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
    body= forms.CharField(widget=PagedownWidget())
    publish= forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model= Post
        fields=[
            "title",
            "image",
            "body",
            "draft",
            "publish"
        ]
