spicy.categories
================

Приложение использует [концепцию разработки djangо-приложений SpicyCMS](https://github.com/spicycms/spicy.core).
Это приложение-простое и использует шаблоны для интрефейса администрирования spicy.core.admin.
Вы можете путем конфигурации settings.py и наследования ``abs.AbstractCategory``,
создать собственную модель категорий и добавить логику к существующему приложению.
Все доступные настройки по умолчанию находятся в [defaults.py](./src/spicy/categories/defaults.py). 

**Версии**
- Django 1.3 - 1.5
- Python 2.7

Назначение
==========

Категории сделаны для того, чтобы редактор сайта, мог группировать данные.
Быстро искать в панели адимнистратора и дать задачу разработчику на вывод данных по категрии в любом шаблоне сайта.


Для редактора сайта
-------------------

{TODO} сделать автоматический вывод сортировки по категории для списка статей или любых других объектов CMS.
Динамическое подключение.


Подключаем категорию к вашей модели
----------------------------------

Настраиваем Django приложение ``settings.py``

```
INSTALLED_APPS = (
...
'spicy.categories',
...

)
```

Подключаем категорию к вашей модели данных

```
# yourapp.models.py
from django.db import models

class YourModel(models.Model):
# other fields
category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('Category'))
```

Выводим в шаблоне сайта модели по заданной категории, по slug:
```
{% category "slug" "app" "model" 10 %}
    This is {{ doc.title }} document!
{% endcategory %}
```

Выводим в шаблоне сайта модели по заданной категории, по slug, с пажинацией по 10 объектов на странице:
```
{% category "slug" 10 paginate as doc %}
    This is {{ doc.title }} document!
{% endcategory %}
```

Фильтрация объектов в шаблоне (реализованы только простые запросы):
```
{% category "slug" "app" "model" all 10 where owner__is_banned=True %}
    Document {{ doc }} from a user that isn't banned. Parameter "all" disables default filtering.
{% endcategory %}
```

Сортировка объектов (возможна по нескольким полям), с ключевым словом sorted:
```
{% category "slug" "app" "model" sorted title -pub_date %}
    Document {{ doc }} sorted by title field ascending and pub_date field descending.
{% endcategory %}
```

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

```
    CREATE_CATEGORY_FORM = 'yourapp.forms.CustomCreateCategoryForm'
    EDIT_CATEGORY_FORM = 'yourapp.forms.CustomEditCategoryForm'
```

Добавить новую форму, в которой объявлено поле new_field:

```
    # yourapp.forms.py
    from django.conf import settings
    from spicy.utils import get_custom_model_class
    CustomCategory = get_custom_model_class(settings.CUSTOM_CATEGORY_MODEL)

    class CategoryForm(forms.ModelForm):
        class Meta:
            model = CustomCategory
            fields = 'title', 'slug', 'order_lv', 'site', 'new_field'
```    

Настройки индивидуальной панель администрирования для категорий
---------------------------------------------------------------

По умолчанию, как и в Django приложении, все модели редактируются в панели администрирования,
но концепция SpicyCMS, предполагает разработку интерфейсов под нужды оператора, чтобы ускорить и упросить его работу.

Для индивидуального редактирования новых полей вашей модели в админке, 
нужно создать копии шаблонов templates/spicy.category/admin/edit.html и templates/spicy.category/admin/create.html в своем проекте темы сайта или приложения:

```
...
{% block content %}
    {# standard fields #}
    {% formfield "" form "new_field" "li-select" %}
    ...
{% endblock %}
...
```    

Таким образом, вы можете использовать разные формы для редактирования и создания категории.


admin.AdminApp используется для отображения в меню и на главной странице разделов по управлению категориями.
