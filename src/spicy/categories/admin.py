# coding=utf-8
from django import http
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from spicy.core.admin.conf import AdminAppBase, AdminLink, Perms
from spicy.core.profile.decorators import is_staff
from spicy.core.siteskin.common import NavigationFilter
from spicy.core.siteskin.decorators import ajax_request, render_to
from spicy.utils import get_custom_model_class
from . import defaults, forms


Category = get_custom_model_class(defaults.CUSTOM_CATEGORY_MODEL)


class AdminApp(AdminAppBase):
    name = 'categories'
    label = _('Categories')
    order_number = 3

    menu_items = (
        AdminLink('categories:admin:create', _('Create category')),
        AdminLink('categories:admin:index', _('All categories')),
    )

    create = AdminLink('categories:admin:create', _('Create category'),)

    perms = Perms(view=[],  write=[], manage=[])

    @render_to('menu.html', use_admin=True)
    def menu(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)

    @render_to('dashboard.html', use_admin=True)
    def dashboard(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)


@is_staff(required_perms='categories.change_category')
@render_to('list.html', use_admin=True)
def category_list(request):
    nav = NavigationFilter(request)
    paginator = nav.get_queryset_with_paginator(Category)
    objects_list = paginator.current_page.object_list
    return {'paginator': paginator, 'objects_list': objects_list, 'nav': nav}


@is_staff(required_perms='categories.add_category')
@render_to('create.html', use_admin=True)
def create(request):
    if request.method == 'POST':
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(reverse('categories:admin:index'))
    else:
        form = forms.CategoryForm(initial={'site': Site.objects.get_current()})
    return {'form': form}


@is_staff(required_perms='categories.change_category')
@render_to('edit.html', use_admin=True)
def edit(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = forms.CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(reverse(
                'categories:admin:index'))
    else:
        form = forms.CategoryForm(instance=category)
    return {'form': form}


@is_staff(required_perms='categories.delete_category')
@render_to('delete.html', use_admin=True)
def delete(request, category_id):
    message = ''
    status = 'ok'

    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        if 'confirm' in request.POST:
            category.delete()
            return http.HttpResponseRedirect(
                reverse('categories:admin:index'))

    return dict(message=unicode(message), status=status, instance=category)


@is_staff(required_perms='categories.delete_category')
@ajax_request
def delete_from_list(request):
    message = ''
    status = 'ok'
    try:
        for category in Category.objects.filter(
                id__in=request.POST.getlist('id')):
            category.delete()
        message = _('All objects have been deleted successfully')
    except KeyError:
        message = settings.MESSAGES['error']
        status = 'error'
    except Exception, e:
        print e
    return dict(message=unicode(message), status=status)
