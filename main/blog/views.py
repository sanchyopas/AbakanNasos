from django.shortcuts import render

from blog.models import BlogSettings, Post, BlogCategory

def blog(request):
  posts = Post.objects.all()
  category = BlogCategory.objects.all()

  try:
    setup = BlogSettings.objects.get()
  except:
    setup = BlogSettings()
  
  context = {
    "posts": posts,
    "categorys": category,
    "setup_blog": setup
  }
  return render(request, "pages/blog/blog.html", context)

def category_post(request, category_slug):
  category = BlogCategory.objects.get(slug=category_slug)
  categorys = BlogCategory.objects.all()
  post = Post.objects.filter(category=category)

  context = {
    "category": category,
    "categorys": categorys,
    "posts": post
  }
  return render(request, "pages/blog/blog_category.html", context)

def post(request, category_slug, slug):
    post = Post.objects.get(slug=slug)
    viewed_articles = request.session.get('viewed_articles', [])
    
    # Проверяем, просматривал ли пользователь эту статью ранее.
    if slug not in viewed_articles:
      # Увеличиваем счетчик просмотров, если статья просматривается впервые.
      post.view_count += 1
      post.save()

      # Добавляем идентификатор статьи в список просмотренных.
      viewed_articles.append(slug)

      # Обновляем сессию, сохраняя в ней обновленный список.
      request.session['viewed_articles'] = viewed_articles


    context = {
        "post": post,
    }

    return render(request, "pages/blog/blog_detail.html", context)