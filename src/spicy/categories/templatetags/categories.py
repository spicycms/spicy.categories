from __future__ import absolute_import
from datetime import datetime
from django.conf import settings
from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from spicy.categories import defaults
from spicy.core.errors import EmptyModelError
from spicy.utils import get_custom_model_class


Category = get_custom_model_class(defaults.CUSTOM_CATEGORY_MODEL)


# TODO: make default value for categories
DEFAULT_CATEGORIES_OBJECTS_PER_PAGE = getattr(
    settings, 'DEFAULT_CATEGORIES_OBJECTS_PER_PAGE', 10)

register = template.Library()


class CategoryNode(template.Node):
    def __init__(
            self, nodelist, slug, app=None, model=None, num_per_page=None,
            paginate=False, object_name='doc', filter_query=None, labels=None,
            show_all=False):
        self.nodelist = nodelist
        self.slug = template.Variable(slug)
        self.app = template.Variable(app)
        self.model = template.Variable(model)
        self.labels = labels and template.Variable(labels)
        self.num_per_page = template.Variable(
            num_per_page if num_per_page else unicode(
                DEFAULT_CATEGORIES_OBJECTS_PER_PAGE))
        self.paginate = paginate
        self.object_name = object_name
        self.show_all = show_all
        self.filter_query = [
            q.split('=') for q in (filter_query or '').split(',') if q]

    def render(self, context):
        for var in (True, False, None):
            # Not needed in Django 1.5?
            context[unicode(var)] = var
        
        try:
            slug = self.slug.resolve(context)
        except:
            slug = None 
        app = self.app.resolve(context)
        model = self.model.resolve(context)

        try:
            obj_type = ContentType.objects.get(app_label=app, model=model)
            objects = obj_type.model_class().objects.all()
            if not self.show_all:
                objects = objects.filter(
                    is_public=True, pub_date__lte=datetime.now())
        except AttributeError:
            return EmptyModelError(app, model)

        if slug:
            objects = objects.filter(category__slug=slug)

        def get_vars((k, v)):
            try:
                return k, template.Variable(v).resolve(context)
            except template.VariableDoesNotExist:
                return ()

        if self.filter_query:
            objects = objects.filter(
                **dict(filter(
                    None, (get_vars(item) for item in self.filter_query))))

        if self.labels:
            try:
                labels = self.labels.resolve(context)
            except template.VariableDoesNotExist:
                labels = None
            if labels:
                objects = objects.filter(label__text__in=labels.split(','))

        if self.paginate:
            request = context.get('request')
            if request:
                try:
                    page_num = int(request.GET.get('page', 1))
                except ValueError:
                    page_num = 1

            paginator = Paginator(objects, self.num_per_page.resolve(context))
            context['paginator'] = paginator
            page = paginator.page(page_num)
            context['pages'] = page
            paginator.current_page = page
            objs = page.object_list
        else:
            objs = objects[:self.num_per_page.resolve(context)]

        results = []
        last_obj = len(objs) - 1
        for i, obj in enumerate(objs):
            context[self.object_name] = obj
            context['loop_counter'] = i
            context['last_category'] = i == last_obj
            try:
                result = self.nodelist.render(context)
                results.append(result)
            except Exception:
                pass
        return ''.join(results)


@register.tag
def category(parser, token):
    """
    This will render a block of text with docs by category.

    Usage::

        {% category "blog" "presscenter" "document" 10 %}
        This is {{ doc.title }} document!
        {% endcategory %}

    Additionally, it can be used for displaying pagination:

        {% category "blog" 10 paginate as doc %}
        This is {{ doc.title }} document!
        {% endcategory %}

    Documents can be filtered (only simple queries are implemented):
        {% category "blog" "presscenter" "document" all 10 where
         owner__is_banned=True %}
        Document {{ doc }} from a user that isn't banned. Parameter "all"
         disables default filtering.
        {% endcategory %}
    """
    bits = token.split_contents()

    options = {'show_all': False}
    remaining_bits = bits[1:]

    try:
        options['slug'] = remaining_bits.pop(0)
        options['app'] = remaining_bits.pop(0)
        options['model'] = remaining_bits.pop(0)
    except IndexError:
        raise template.TemplateSyntaxError('Invalid category block syntax')

    try:
        num_per_page = remaining_bits.pop(0)
    except IndexError:
        num_per_page = unicode(DEFAULT_CATEGORIES_OBJECTS_PER_PAGE)

    if num_per_page == u'all':
        num_per_page = None
    else:
        options['num_per_page'] = num_per_page

    if remaining_bits and remaining_bits[0].startswith('labels='):
        options['labels'] = remaining_bits.pop(0)[7:]

    is_as = False
    while remaining_bits:
        option = remaining_bits.pop(0)
        if option == 'paginate':
            options['paginate'] = True
            continue
        elif option == 'all':
            options['show_all'] = True
            continue
        elif option in ('as', 'where'):
            obj_name = remaining_bits.pop(0)
            if option == 'as':
                options['object_name'] = obj_name
            else:
                options['filter_query'] = obj_name
            continue
        else:
            raise template.TemplateSyntaxError('Invalid category block syntax')

    nodelist = parser.parse(('endcategory',))
    parser.delete_first_token()
    return CategoryNode(nodelist, **options)


@register.filter
def category_by_slug(value):
    try:
        return Category.objects.get(slug=value)
    except Category.DoesNotExist:
        return


@register.simple_tag(takes_context=True)
def all_category(context):
    context['category'] = Category.objects.select_related()
    return ""
