from .abs import AbstractCategory
from .defaults import USE_DEFAULT_CATEGORY


if USE_DEFAULT_CATEGORY:
    class Category(AbstractCategory):
        class Meta:
            db_table = 'ctg_category'
