from django import forms

from ckeditor.fields import RichTextFormField


class PostForm(forms.Form):
    content = RichTextFormField(config_name='post_ckeditor')
