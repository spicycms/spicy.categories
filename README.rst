
spicy.categories
================

****

Назначение
---------------------


Для редактора сайта
"""""""""""""""""""
Категории могут быть присвоены любому объекту на сайте, например, документу.

Для создания категории перейти в Категории > Создать категорию. Задать название, слаг и порядок сортировки, сохранить. Теперь созданная категория будет доступна в списке категорий (Категории > Все категории), отсортированном по порядку сортировки.

Для того, чтобы присвоить документу категорию, нужно перейти на страницу документа (Документ > Все документы > нужный документ), и выбрать в выпадающем списке категорий, сохранить.

Документы могут быть сгруппированы на сайте по категориям.

Для frontend разработчика
"""""""""""""""""""""""""
TODO

Для программиста Django приложения
""""""""""""""""""""""""""""""""""
Модуль содержит базовый абстрактный класс для Категории, который может быть расширен для конкретной сборки приложения. Поддерживает работу с несколькими сайтами посредством `Django Sites Framework <https://djbook.ru/rel1.4/ref/contrib/sites.html>`_.

Версии
******************
- Django <1.4.*
- Python 2.7

Docs
*********************

**abs.AbstractCategory()**

    Абстрактный класс Категории

        *title* - заголовок, обязательное поле `CharField <https://djbook.ru/rel1.4/ref/models/fields.html#charfield>`_;

        *slug* - слаг категории, обязательное поле `SlugField <https://djbook.ru/rel1.4/ref/models/fields.html#slugfield>`_;

        *order_lv* - порядок сортировки категорий, поле `PositiveSmallIntegerField <https://djbook.ru/rel1.4/ref/models/fields.html#positivesmallintegerfield>`_, по умолчанию 0;

        *site* - ссылка на сайт, где будет использована категория, обязательное поле `ForeignKey <https://djbook.ru/rel1.4/ref/models/fields.html#foreignkey>`_;

        *objects* - менеджер объектов. Используется стандартный `менеджер Django <https://django.readthedocs.io/en/1.4.X/topics/db/managers.html>`_;

        *on_site* - менеджер объектов, позволяет работать с объектами, связанными с текущим сайтом. Используется стандартный `менеджер сайтов Django <https://djbook.ru/rel1.4/ref/contrib/sites.html#the-currentsitemanager>`_.

    По умолчанию сортировка объектов происходит по полям order_lv и title. Это поведение может быть изменено путем переопределения параметра Meta.ordering у дочернего класса.

    Так как класс является абстрактным, таблица не будет создана в базе данных. Для использования объектов категорий по умолчанию предоставляется класс Category. Вы можете использовать свой класс, для этого необходимо указать в settings.py:

        ``USE_DEFAULT_CATEGORY = False``

        ``CUSTOM_CATEGORY_MODEL = 'yourapp.models.CustomCategory'``



**models.Category()**

    Класс наследник AbstractCategory, предоставляется по умолчанию. Набор полей соответствует AbstractCategory. В базе данных будет создана таблица ctg_category.

    Для использования собственного класса категорий используйте настройки USE_DEFAULT_CATEGORY и CUSTOM_CATEGORY_MODEL. Ваш класс должен наследоваться от AbstractCategory, также нужно указать Meta.abstract = False, чтобы Django создала таблицу для кастомных категорий.

    Может быть использована для связи с любым объектом приложения через FK.

**forms.CategoryForm()**

    Форма по умолчанию для работы с категориями через админку и сайт. Унаследована от `ModelForm Django <https://django.readthedocs.io/en/1.4/topics/forms/modelforms.html>`_.

        *title* - поле `формы CharField <https://django.readthedocs.io/en/1.4/ref/forms/fields.html#charfield>`_ для редактирования title;

        *slug* - поле `формы SlugField <https://django.readthedocs.io/en/1.4/ref/forms/fields.html#slugfield>`_ для редактирования slug;

        *order_lv* - поле `формы IntegerField <https://django.readthedocs.io/en/1.4/ref/forms/fields.html#integerfield>`_

        *site* - поле `формы ModelChoiceField <https://django.readthedocs.io/en/1.4/ref/forms/fields.html#modelchoicefield>`_

    CategoryForm используется по умолчанию, но вы можете изменить это поведение, указав в setting.py:

        ``CREATE_CATEGORY_FORM = 'yourapp.forms.CustomCreateCategoryForm'``

        ``EDIT_CATEGORY_FORM = 'yourapp.forms.CustomEditCategoryForm'``

    Таким образом, вы можете использовать разные формы для редактирования и создания категории.

**admin.AdminApp()**

    Класс приложения для админки, унаследован от AdminAppBase `spicy.core <https://github.com/spicycms/spicy.core>`_. AdminApp используется для отображения в меню и на главной странице разделов по управлению категориями.

        *name* - строковое значение, которое будет использовано для обращения к приложению spicy.category;

        *label* - заголовок для разделов приложения spicy.category, который будет отображен в админке;

        *order_number* - порядок, который задает отображение приложений-модулей в админке;

        *menu_items* - список объектов spicy.core.admin.conf.AdminLink, определяет, какие подразделы будут отображены в меню админки для приложения spicy.category;

        *perms* - TODO

    Переопределяет 2 метода базового класса AdminAppBase:

        *menu(self, request, *args, **kwargs)* - отрисовывает блок меню для spicy.category;

        *dasboard(self, request, *args, **kwargs)* - отрисовывает блок spicy.category на главной странице проекта в админке.


Методы, которые работают с категориями в админке:

    *category_list(request)* - отображает список категорий. Отрисовывается в шаблоне 'spicy.categories/admin/list.html';

    *create(request)* - создает новую категорию. Отрисовывается в шаблоне 'spicy.categories/admin/create.html';

    *edit(request, category_id)* - редактирует категорию. Отрисовывается в шаблоне 'spicy.categories/admin/edit.html';

    *delete(request, category_id)* - удаляет категорию. Отрисовывается в шаблоне 'spicy.categories/admin/delete.html';

    *delete_from_list(request)* - удаляет выбранные категории из списка. Обрабатывает AJAX-запрос.


Примеры
*****************
TODO

