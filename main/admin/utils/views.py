from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.urls import reverse


def generic_list(request, model, title, add_url, edit_url, delete_url):
    items = model.objects.all()

    context = {
        "items": items,
        "title": title,
        "add_url": add_url,
        "edit_url": edit_url,
        "delete_url": delete_url,
    }

    return render(request, "common-template/list-items.html", context)

def generic_add(request, form_class, redirect_name, title, template_name=None):
    """Универсальное добавление"""
    if not template_name:
        template_name = "common-template/template-edit-add-page.html"

    form = form_class()
    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Успешно сохранено !")
            url = reverse(redirect_name) + "?tab=list"
            return redirect(url)
        else:
            return render(request, template_name, {"form": form, "title": title})

    context = {
        "form": form,
        "title": title
    }
    return render(request, template_name, context)

def generic_edit(request, pk, model, form_class, redirect_name, title,  template_name=None):
    """Универсальное редактирование"""
    if not template_name:
        template_name = "common-template/template-edit-add-page.html"

    item = get_object_or_404(model, id=pk)

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Успешно сохранено !")
            return redirect(redirect_name)
        else:
            return render(request, template_name, {"form": form, "item": item})

    form = form_class(instance=item)
    context = {
        "form": form,
        "item": item,
        "title": title,
    }
    return render(request, template_name, context)

def generic_delete(request, model, pk):
    item = model.objects.get(id=pk)
    item.delete()
    messages.success(request, 'Успешно удалено!')
    return redirect(request.META.get('HTTP_REFERER'))


def generic_singleton_edit(
    request,
    form_class,
    model_class,
    title,
    edit_url,
    add_url,
    delete_url,
    template_name=None,
    model_list=None,
    model_cat=None
  ):
    """Универсальное редактирование Singleton модели"""
    if not template_name:
        template_name = "common-template/template-edit-add-page.html"

    items = model_list.objects.all()
    categories = model_cat.objects.all()

    # Получаем или создаем единственный экземпляр
    try:
        instance = model_class.objects.get()
    except model_class.DoesNotExist:
        instance = model_class()
        instance.save()
    except Exception as e:
        messages.error(request, f"Ошибка: {e}")
        return redirect(request.META.get('HTTP_REFERER'))

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            try:
                saved_instance = form.save()
                messages.success(request, "Успешно сохранено!")
                return redirect(request.META.get('HTTP_REFERER'))
            except Exception as e:
                messages.error(request, f"Ошибка сохранения: {e}")
        else:
            return render(request, template_name, {
                "form": form,
                "title": title,
                "settings": instance,
                "items": items,
                "edit_url": edit_url,
                "add_url": add_url,
                "delete_url": delete_url,
                "categories": categories
            })

    form = form_class(instance=instance)
    context = {
        "form": form,
        "title": title,
        "settings": instance,
        "items": items,
        "edit_url": edit_url,
        "add_url": add_url,
        "delete_url": delete_url,
        "categories": categories
    }
    return render(request, template_name, context)