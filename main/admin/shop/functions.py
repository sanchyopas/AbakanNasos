def admin_product(request):
  """
  View, которая возвращаяет и отрисовывает все товары на странице
  и разбивает их на пагинацию
  """
  page = request.GET.get('page', 1)
  products = Product.objects.all()
  paginator = Paginator(products, 20)
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
  product_image = ProductImage.objects.filter(parent=product)
  form = ProductForm(instance=product)

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
    "product_image": product_image,
  }
  return render(request, "shop/product/product_edit.html", context)

def product_add(request):
  form = ProductForm()

  if request.method == "POST":
    form_new = ProductForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_product')
    else:
      return render(request, "shop/product/product_add.html", {"form": form_new})

  context = {
    "form": form
  }

  return render(request, 'shop/product/product_add.html', context)

def product_delete(request,pk):
  product = Product.objects.get(id=pk)
  product.delete()

  return redirect('admin_product')