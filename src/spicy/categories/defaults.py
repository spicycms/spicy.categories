from django.conf import settings


USE_DEFAULT_CATEGORY = getattr(settings, 'USE_DEFAULT_CATEGORY', True)
CUSTOM_CATEGORY_MODEL = (
    'categories.Category' if USE_DEFAULT_CATEGORY else
    settings.CUSTOM_CATEGORY_MODEL)

CREATE_CATEGORY_FORM = getattr(                                                                   
    settings, 'CREATE_CATEGORY_FORM',                                                             
    'spicy.categories.forms.CategoryForm')                                                 

EDIT_CATEGORY_FORM = getattr(                                                                     
    settings, 'EDIT_CATEGORY_FORM',
    'spicy.categories.forms.CategoryForm')
