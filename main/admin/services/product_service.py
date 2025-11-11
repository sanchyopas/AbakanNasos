from shop.models import Product
from ..forms import ProductForm, ProductImageForm

def get_all_products():
  return Product.objects.all()

def get_product_by_id(pk):
  return Product.objects.get(id=pk)
