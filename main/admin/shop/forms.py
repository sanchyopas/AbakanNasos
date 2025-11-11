from shop.models import Product, ProductImage

class ProductForm(forms.ModelForm):
    """ Form, отвечает за создание товара и редактирование товара"""
    # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            'article': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                "id":"article"
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                "id":"name"
            }),
            'slug': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                "id": "slug"
            }),
            'category': forms.Select(attrs={
                'class': INPUT_CLASS,
            }),
#             'categories': forms.CheckboxSelectMultiple,
            'manufacturer': forms.TextInput(attrs={
                'class': INPUT_CLASS,
            }),
            'manufacturer_description': forms.TextInput(attrs={
                'class': INPUT_CLASS,
            }),
             'manufacturer_description': forms.TextInput(attrs={
                'class': INPUT_CLASS,
            }),
            'price': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
            }),
            'sale': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
            }),
            'installment': forms.Textarea(attrs={
                'class': INPUT_CLASS,
            }),
            'quantity': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
            }),
            'quantity_purchase': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
            }),
            'status': forms.CheckboxInput(attrs={
              'class': 'form__controls-checkbox',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': INPUT_CLASS,
            }),
            'meta_title': forms.TextInput(attrs={
                'class': INPUT_CLASS,
            }),
            'meta_description': forms.Textarea(attrs={
                'class': INPUT_CLASS,
                "id": "meta_description"
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': INPUT_CLASS,
            }),
        }

# Товар и опции товара
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage

        fields = [
            'parent',
            'src'
        ]
        labels = {
            'src': 'Выбрать изображение'
        }
        widgets = {
            'parent': forms.Select(attrs={
                'class': INPUT_CLASS,
            }),
            'src': CustomImageWidget(),
        }
