# coding=utf-8
from . import forms, models
from django import http
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from spicy.core.profile.decorators import is_staff
from spicy.core.siteskin.common import NavigationFilter
from spicy.core.siteskin.decorators import ajax_request, render_to


@is_staff(required_perms='categories.change_category')
@render_to('categories/index.html', use_admin=True)
def categories(request):
    nav = NavigationFilter(request)
    paginator = nav.get_queryset_with_paginator(models.Category)
    objects_list = paginator.current_page.object_list
    return {'paginator': paginator, 'objects_list': objects_list, 'nav': nav}


@is_staff(required_perms='categories.add_category')
@render_to('categories/add.html', use_admin=True)
def category_add(request):
    if request.method == 'POST':
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(reverse(
                'categories:admin:index'))
    else:
        form = forms.CategoryForm(initial={'site': Site.objects.get_current()})
    return {'form': form}


@is_staff(required_perms='categories.change_category')
@render_to('categories/edit.html', use_admin=True)
def category_edit(request, category_id):
    category = get_object_or_404(models.Category, pk=category_id)
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
@ajax_request
def categories_delete(request):
    message = ''
    status = 'ok'
    try:
        for category in models.Category.objects.filter(
            id__in=request.POST.getlist('id')):
            category.delete()
        message = _('All objects have been deleted successfully')
    except KeyError:
        message = settings.MESSAGES['error']
        status = 'error'
    except Exception, e:
        print e
    return dict(message=unicode(message), status=status)
