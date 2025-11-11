INSTALLED_APPS = [
    # "django.contrib.admin",
    "admin",
    "accounts",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_ckeditor_5',
    # "debug_toolbar",
    # "corsheaders",
    'sorl.thumbnail',
    'django.contrib.sitemaps',
    "home",
    "shop",
    # "coupons",
    "users",
    "reviews",
    "service",
    "cart",
    "order",
    "payment",
    "subdomain",
    'allauth',
    'allauth.account',
    # 'tinymce',
    "blog",
    "news",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    # "corsheaders.middleware.CorsMiddleware",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'avroraweb_maxim',
        'USER': 'avroraweb_maxim',
        'PASSWORD': 'EC%qwzizE4xd',
        'HOST': 'localhost',
    }
}
