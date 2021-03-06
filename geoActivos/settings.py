"""
Django settings for geoActivos project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')6(m(*bes1$d@n_^cm7jsq=fg1*!)^!9w0!0^t9pe&ki82@5#&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'cuser',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventario.apps.InventarioConfig',
    'geo.apps.GeoConfig',
    'django_select2',
    'import_export',
    'supra',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cuser.middleware.CuserMiddleware',
]

ROOT_URLCONF = 'geoActivos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]


WSGI_APPLICATION = 'geoActivos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'geo',
        'USER': 'postgres',
        'PASSWORD': 'Exile*74522547',
        'HOST': '104.236.33.228',
        'PORT': '5432',
    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'geo.db'),
    }
}
"""
# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

SUIT_CONFIG = {
    'ADMIN_NAME': 'GeoActivos',
    'SEARCH_URL': '',
    'MENU_OPEN_FIRST_CHILD': True,
    'MENU_ICONS': {
        'sites': 'icon-leaf',
        'auth': 'icon-lock',
        'inventario': 'icon-briefcase',
        'luminaria': 'icon-map-marker',
    },
    'MENU': (
        # To reorder existing apps use following definition
        'sites',
        {'app': 'auth', 'icon': 'icon-lock', 'models': ('user', 'group')},
        {'app': 'inventario', 'icon': 'icon-briefcase', 'label': 'Inventario', 'models': (
            'cuenta', 'custodio', 'bodega', 'central', 'proveedor', 'fabricante', 'articulo', 'tipoactivo', 'activo', 'articulonoserial', 'activonoserial')},
        {'app': 'inventario', 'icon': 'icon-cog', 'label': 'Operaciones de bodega',
            'models': ('actarequisicion', 'actasalida', 'actaentrada')},
        {'app': 'geo', 'icon': 'icon-map-marker', 'label': 'Geo',
            'models': ('zona', 'direccion', 'geoactivo')},

    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-CO'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/mario/geoactivos/media/'
