from django.conf.urls.defaults import *


admin_urls = patterns(
    'spicy.categories.admin',

    # Categories
    url(r'^$', 'categories', name='index'),
    url(r'^add/$', 'category_add', name='add'),
    url(r'^(?P<category_id>\d+)/$', 'category_edit', name='edit'),
    url(r'^delete/$', 'categories_delete', name='delete'),
)


urlpatterns = patterns(
    '',
    url(r'^admin/categories/', include(admin_urls, namespace='admin')),
    )
