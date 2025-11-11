from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from .forms import CategoryForm

def admin_category(request):
    categorys = Category.objects.all()
    context = {
        "items": categorys,
    }
    return render(request, "shop/category/category.html", context)

def category_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_category")
    else:
        form = CategoryForm()

    context = {
        "form": form
    }
    return render(request, "shop/category/category_add.html", context)

def category_edit(request, pk):
    category = get_object_or_404(Category, id=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect("admin_category")
    else:
        form = CategoryForm(instance=category)

    context = {
        "form": form,
        "category": category
    }
    return render(request, "shop/category/category_edit.html", context)

def category_delete(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.delete()
    return redirect("admin_category")