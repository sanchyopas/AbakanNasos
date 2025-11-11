def admin_color(request):
  items = ColorProduct.objects.all()

  context = {
    "items": items,
  }

  return render(request, "shop/color/color.html", context)


def admin_color_add(request):
  form = ColorProductForm()

  if request.method == "POST":
    form_new = ColorProductForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_color')
    else:
      return render(request, "shop/color/color_add.html", { "form": form_new })

  context = {
    "form": form,
  }

  return render(request, "shop/color/color_add.html", context)

def admin_color_edit(request, pk):
  item = ColorProduct.objects.get(id=pk)

  if request.method == "POST":
    form_new = ColorProductForm(request.POST, request.FILES, instance=item)

    if form_new.is_valid():
      form_new.save()
      return redirect('admin_color')
    else:
      return render(request, "shop/color/color_edit.html", { "form": form_new })

  form = ColorProductForm(instance=item)
  context = {
    "form": form,
  }

  return render(request, "shop/color/color_edit.html", context)

def admin_color_delete(request, pk):
  subdomain = Subdomain.objects.get(id=pk)
  subdomain.delete()
  return redirect(request.META.get('HTTP_REFERER'))