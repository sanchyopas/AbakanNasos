from django import forms
from .models import Reviews

class ReviewsForm(forms.ModelForm):
  """ Form, добавление и редактирование отзыва"""
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())

  class Meta:
    model = Reviews
    fields = "__all__"
    labels = {}
    widgets = {
      'name': forms.TextInput(attrs={
        'class': "form__controls",
        'id': 'name'
      }),
      'slug': forms.TextInput(attrs={
        'class': "form__controls",
        "id": "slug"
      }),
      'date': forms.DateInput(attrs={
        'class': "form__controls",
      }),
      'text': forms.Textarea(attrs={
        'class': "form__controls",
        'rows': 5,
      }),
      'status': forms.CheckboxInput(attrs={
        'class': 'form__controls-checkbox',
      }),
      'meta_h1': forms.TextInput(attrs={
        'class': "form__controls",
      }),
      'meta_title': forms.TextInput(attrs={
        'class': "form__controls",
      }),
      'meta_description': forms.Textarea(attrs={
        'class': 'form-controls',
        'rows': 5,
      }),
      'meta_keywords': forms.TextInput(attrs={
        'class': "form__controls"
      })
    }