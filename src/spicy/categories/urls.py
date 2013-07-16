from django.conf.urls.defaults import *


admin_urls = patterns(
    'spicy.categories.admin',

    # Categories
    url(r'^$', 'list', name='index'),
    url(r'^create/$', 'create', name='create'),
    url(r'^(?P<category_id>\d+)/$', 'edit', name='edit'),
    url(r'^delete/(?P<category_id>\d+)/$', 'delete', name='delete'),
)


urlpatterns = patterns(
    '',
    url(r'^admin/categories/', include(admin_urls, namespace='admin')),
    )
