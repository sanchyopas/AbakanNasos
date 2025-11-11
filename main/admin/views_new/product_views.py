from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from ..forms import ProductForm, ProductImageForm
from shop.models import Product,ProductImage
from ..services.product_service import get_all_products, get_product_by_id, update_product, save_image_product,create_product

def admin_product(request):
    page = request.GET.get('page', 1)
    products = get_all_products()

    paginator = Paginator(products, 10)
    current_page = paginator.page(int(page))

    context = {
    "items": current_page
    }
    return render(request, "shop/product/product.html", context)

def product_edit(request, pk):
  """
    View, которая получает данные из формы редактирования товара
    и изменяет данные внесенные данные товара в базе данных
  """
  product = Product.objects.get(id=pk)
  form = ProductForm(instance=product)
  image_form = ProductImageForm()

  form_new = ProductForm(request.POST, request.FILES, instance=product)
  if request.method == 'POST':
    if form_new.is_valid():
      form_new.save()
      product = Product.objects.get(slug=request.POST['slug'])
      images = request.FILES.getlist('src')

      for image in images:
          img = ProductImage(parent=product, src=image)
          img.save()
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return render(request, 'shop/product/product_edit.html', {'form': form_new})
  context = {
    "form":form,
    'image_form': image_form,
  }
  return render(request, "shop/product/product_edit.html", context)

  context = {
  "form":form,
  'image_form': image_form,
  }

  return render(request, "shop/product/product_edit.html", context)

def product_add(request):
    """Добавление нового товара"""
    form = ProductForm()

    if request.method == "POST":
        product = create_product(request.POST, request.FILES)
        if product:
            return redirect('admin_product')  # Успех
        return render(request, "shop/product/product_add.html", {"form": ProductForm(request.POST, request.FILES)})  # Ошибка

    return render(request, 'shop/product/product_add.html', {"form": form})

def product_delete(request,pk):
  product = Product.objects.get(id=pk)
  product.delete()

  return redirect('admin_product')