from django import forms 
from django.forms import ModelForm
from .models import Post,Profile

class postForm(ModelForm):
    content= forms.CharField(widget=forms.Textarea(attrs={'class':'form-control fm', 'rows':'3', 'cols':'5'}),label='')
    class Meta:
        model = Post
        fields=('content',)
class NewEditPostForm(forms.Form):
    
    """The edit post form class
    """
    id_post_edit_text = forms.Field(widget=forms.Textarea(
        {'rows': '3', 'maxlength': 160, 'class': 'form-control', 'placeholder': "What's happening?", 'id': 'id_post_edit_text' }), label="New Post", required=True)  


class profileForm(ModelForm):
    class meta:
        model=Profile        
