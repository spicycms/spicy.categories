spicy.categories
================

**Версии**
- Django 1.3 - 1.5
- Python 2.7

Назначение
==========

Категории сделаны для того, чтобы редактор сайта, мог группировать данные.
Быстро искать в панели адимнистратора и дать задачу разработчику на вывод данных по категрии в любом шаблоне сайта.
Реализация под ваш проекта настаривается через settings.py и наследование модели ``abs.AbstractCategory``, все доступные настройки по умолчанию находятся в [defaults.py](./src/spicy/categories/defaults.py). 

Для редактора сайта
-------------------

{TODO} сделать автоматический вывод сортировки по категории для списка статей или любых других объектов CMS.
Динамическое подключение.

Вывод объектов категорий в шаблонах сайта (frontend)
-------------------------

[Django-templatetags](./src/spicy/categories/templatetags/)


Подключаем категорию к вашей модели
----------------------------------

    # yourapp.models.py
    from django.db import models
    
    class YourModel(models.Model):
        # other fields
        category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('Category'))


Делаем свою модель категорий
----------------------------

Модуль содержит базовый абстрактный класс для Категории, который может быть расширен для конкретной сборки приложения. Поддерживает работу с несколькими сайтами посредством [django sites framework](https://djbook.ru/rel1.4/ref/contrib/sites.html).

Для использования объектов категорий по умолчанию предоставляется класс Category. Вы можете использовать свой класс, для этого необходимо указать в settings.py:

    USE_DEFAULT_CATEGORY = False
    CUSTOM_CATEGORY_MODEL = 'yourapp.models.CustomCategory'

Ваш класс должен наследоваться от AbstractCategory, также нужно указать Meta.abstract = False, чтобы Django создала таблицу для кастомных категорий.

    # yourapp.models.py
    from django.db import models
    from spicy.categories.abs import AbstractCategory

    class CustomCategory(AbstractCategory):
        new_field = models.IntegerField('New field', null=True, blank=True)

        @models.permalink
        def get_absolute_url(self):
            return 'webapp:public:category', None, {'slug': self.slug}

        class Meta:
            abstract = False

По умолчанию для работы с категориями через админку и сайт используется форма forms.CategoryForm. Вам нужно изменить это поведение, указав в setting.py:

    CREATE_CATEGORY_FORM = 'yourapp.forms.CustomCreateCategoryForm'
    EDIT_CATEGORY_FORM = 'yourapp.forms.CustomEditCategoryForm'
    
Добавить новую форму, в которой объявлено поле new_field:

    # yourapp.forms.py
    from django.conf import settings
    from spicy.utils import get_custom_model_class
    CustomCategory = get_custom_model_class(settings.CUSTOM_CATEGORY_MODEL)

    class CategoryForm(forms.ModelForm):
        class Meta:
            model = CustomCategory
            fields = 'title', 'slug', 'order_lv', 'site', 'new_field'
            
Добавить поле new_field в шаблоны админки:

    

Таким образом, вы можете использовать разные формы для редактирования и создания категории.
admin.AdminApp используется для отображения в меню и на главной странице разделов по управлению категориями.
