from django import forms

from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField


class PostForm(forms.Form):
    content = RichTextUploadingFormField(config_name='post_ckeditor')
