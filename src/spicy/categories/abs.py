from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractCategory(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    order_lv = models.PositiveSmallIntegerField(default=0)

    site = models.ForeignKey(Site, verbose_name=_('Site'))

    objects = models.Manager()
    on_site = CurrentSiteManager(field_name='site')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'categories:admin:edit', [self.id], {}

    class Meta:
        abstract = True
        ordering = 'order_lv', 'title'
