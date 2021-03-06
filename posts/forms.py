from django import forms
from .models import Post, post_save

class NewPostForm(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption =forms.CharField(widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': 'Image Caption'}), required=True)
    tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': 'Image Name '}), required=True)
    
    class Meta:
        model = Post
        fields = ['picture', 'caption', 'tag']