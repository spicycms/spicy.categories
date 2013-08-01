from . import defaults
from django import forms
from spicy.utils import get_custom_model_class


Category = get_custom_model_class(defaults.CUSTOM_CATEGORY_MODEL)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = 'title', 'slug', 'order_lv', 'site'
