from django.conf import settings


USE_DEFAULT_CATEGORY = getattr(settings, 'USE_DEFAULT_CATEGORY', True)
CUSTOM_CATEGORY_MODEL = (
    'categories.Category' if USE_DEFAULT_CATEGORY else
    settings.CUSTOM_CATEGORY_MODEL)
