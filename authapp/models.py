from django.db import models
from django.contrib.auth.models import AbstractUser


class ComicReader(AbstractUser):
    age = models.PositiveIntegerField(verbose_name='возраст', default=16)
    is_uploader = models.BooleanField(verbose_name='Uploader', default=False)
    darck_comic = models.BooleanField(verbose_name='Темное', default=False)
    dc_comic = models.BooleanField(verbose_name='Вселенная DC', default=False)
    marvel_comic = models.BooleanField(verbose_name='Вселенная Marvel', default=False)
    adult_comic = models.BooleanField(verbose_name='Для взрослых', default=False)
    hentai_comic = models.BooleanField(verbose_name='hentai', default=False)

    def get_bookmarks(self):
        return self.bookmarkcomic_set.all().order_by('comic')
