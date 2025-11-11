from django.contrib import admin
from .models import Reviews
from .forms import ReviewsForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from main.settings import BASE_DIR
from django.shortcuts import render, get_object_or_404, get_list_or_404


def admin_reviews(request):
  reviews = Reviews.objects.all()

  context = {
    "items": reviews
  }

  return render(request, "reviews/reviews.html", context)

def admin_reviews_edit(request, pk):
  review = Reviews.objects.get(id=pk)
  form = ReviewsForm(instance=review)

  if request.method == "POST":
    form_new = ReviewsForm(request.POST, request.FILES, instance=review)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_reviews")
    else:
      return render(request, "reviews/reviews_edit.html", {"form": form_new})

  context = {
    "review":review,
    "form": form
  }

  return render(request, "reviews/reviews_edit.html", context)

def admin_reviews_add(request):
  form = ReviewsForm()
  if request.method == "POST":
    form_new = ReviewsForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_reviews")
    else:
      return render(request, "reviews/reviews_add.html", {"form": form_new})

  context = {
    "form": form
  }

  return render(request, "reviews/reviews_add.html", context)

def admin_reviews_delete(request, pk):
  review = Reviews.objects.get(id=pk)
  review.delete()
  return redirect("admin_reviews")


