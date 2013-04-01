from . import models
from django import forms

class CategoryForm(forms.ModelForm):
	class Meta:
		model = models.Category
		fields = 'title', 'slug', 'order_lv', 'site'
