from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)91x)z3-_(j8roi)=^ugd%d1g960m!a^pcp$0%57n=6)#9wz6@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["cardinsuv.uz", "www.cardinsuv.uz"]

CSRF_TRUSTED_ORIGINS = ['https://cardinsuv.uz']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'waterApp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'waterConf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'waterApp.views.site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'waterConf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

from django.utils.translation import gettext_lazy as _
LANGUAGE_CODE = 'uz'

LANGUAGES = [
    ('uz', _('Uzbek')),
    ('ru', _('Russian')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True  # Enable localization

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JAZZMIN_SETTINGS = {
    # Sayt sarlavhasi (brauzer tabida ko'rinadi)
    "site_title": "TozaSuv Admin",

    # Navbar tepasidagi sarlavha (kichik ekranlarda "TSA")
    "site_header": "TozaSuv Admin",
    "site_brand": "TozaSuv",

    # Admin panelga kirish sahifasidagi logo
    "login_logo": "waterApp/images/logo.png", # static papkangizdagi logo yo'li

    # Sayt logotipi (navbar'da ko'rinadi)
    # "site_logo": "waterApp/images/logo-small.png", # static papkangizdagi logo yo'li

    # Admin panelga xush kelibsiz matni
    "welcome_sign": "TozaSuv boshqaruv paneliga xush kelibsiz!",

    # Mualliflik huquqi (pastki qismda)
    "copyright": "TozaSuv LLC",

    # Qidiruv maydoni qaysi modellarda ishlashi
    "search_model": ["auth.User", "waterApp.Product", "waterApp.Order"],

    ############
    # Top Menu #
    ############
    "topmenu_links": [
        {"name": "Bosh sahifa", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Saytni ko'rish", "url": "/", "new_window": True},
        {"model": "auth.User"},
        {"app": "waterApp"},
    ],

    #############
    # Side Menu #
    #############
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["waterApp", "auth"],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "waterApp.Order": "fas fa-shopping-cart",
        "waterApp.Product": "fas fa-box-open",
        "waterApp.Category": "fas fa-stream",
        "waterApp.News": "fas fa-newspaper",
        "waterApp.ContactMessage": "fas fa-envelope",
        "waterApp.Testimonial": "fas fa-comment-dots",
        "waterApp.Partner": "fas fa-handshake",
        "waterApp.FAQ": "fas fa-question-circle",
        "waterApp.About": "fas fa-info-circle",
        "waterApp.HomePage": "fas fa-images",
        "waterApp.SiteConfig": "fas fa-cogs",
    },

    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    "related_modal_active": True,

    #############
    # UI Tweaks #
    #############
    "show_ui_builder": False, # UI o'zgartirishni yoqish/o'chirish

    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default", # "flatly", "cerulean", "cosmo", "darkly", "litera", "lumen" va boshqalar
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}