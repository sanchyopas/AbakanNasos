def gallery_settings(request):
  try:
    setup = GalleryCategory.objects.get()
    form = GalleryCategorySettingsForm(instance=setup)
  except:
    form = GalleryCategorySettingsForm()

  if request.method == "POST":
    try:
      setup = BlogSettings.objects.get()
    except BlogSettings.DoesNotExist:
      setup = None
    form_new = GalleryCategorySettingsForm(request.POST, request.FILES, instance=setup)

    if form_new.is_valid:
      form_new.save()

      return redirect('.')
    else:
      return render(request, "gallery/gallery_settings.html", {"form": form})

  context = {
    "form": form,
  }
  return render(request, "gallery/gallery_settings.html", context)


def admin_attribute(request):
  chars = ProductSpecification.objects.all()

  context = {
    "title": "Характеристики товара",
    "chars": chars,
  }

  return render(request, "shop/char/char.html", context)

folder = 'upload/'

from PIL import Image

def upload_goods(request):
    form = UploadFileForm()
    if request.method == 'POST':
      form = UploadFileForm(request.POST, request.FILES)
      if form.is_valid():
          file = request.FILES['file']

          destination = open(os.path.join('upload/', file.name), 'wb+')
          for chunk in file.chunks():
              destination.write(chunk)
          destination.close()

          # Распаковка архива
          with zipfile.ZipFile('upload/upload.zip', 'r') as zip_ref:
              zip_ref.extractall('media/')

          # Удаление загруженного архива
          os.remove('upload/upload.zip')

          # Сжатие фотографий
          for filename in os.listdir('media/upload'):

            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.JPG') or filename.endswith('.JPEG') or filename.endswith('.jpeg'):
              with Image.open(os.path.join('media/upload', filename)) as img:
                temp = filename.replace('.jpeg', '')
                temp_one = temp.replace('№', '')
                temp_b = temp_one.replace('В', 'B')
                temp_e = temp_one.replace('Э', 'E')
                img.save(os.path.join('media/goods', temp_e), quality=60)  # quality=60 для JPEG файла

          # Очистка временной папки
          os.system('rm -rf media/upload')
          return redirect('upload-succes')
      else:
        form = UploadFileForm()
    return render(request, 'upload/upload.html', {'form': form})

def upload_succes(request):
  return render(request, "upload/upload-succes.html")

from pytils.translit import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

def admin_category(request):
  categorys = Category.objects.all()

  context ={
    "items": categorys,
  }
  return render(request, "shop/category/category.html", context)
