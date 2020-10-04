from django.db import models
from authapp.models import ComicReader
from taggit.managers import TaggableManager


def comic_banner_directory_path(instance, filename):
    folder = str(instance.comic_name).replace(' ', '_')
    name = str(filename).replace(' ', '_')
    return '/'.join(['title', folder, name])


class Comic(models.Model):
    HENTAI_CMC = 'ht'
    DARCK_CMC = 'dk'
    ADULT_CMC = 'ad'
    MARVEL_CMC = 'mr'
    DC_CMC = 'dc'
    CUSTOM_CMC = 'at'
    CMC_CHOICES = [
        (HENTAI_CMC, 'Hentai'),
        (DARCK_CMC, 'Dark'),
        (ADULT_CMC, 'Adult'),
        (MARVEL_CMC, 'Marvel'),
        (DC_CMC, 'DC'),
        (CUSTOM_CMC, 'Another')
    ]
    comic_name = models.CharField(max_length=500, blank=False, verbose_name='название комикса')
    comic_description = models.TextField(max_length=4000, blank=True, verbose_name='описание комикса')
    comic_author = models.CharField(max_length=250, blank=False, verbose_name='автор комикса')
    comic_artist = models.CharField(max_length=250, blank=False, default='', verbose_name='работающие над комиксом(Artist)')
    comic_genre = models.CharField(max_length=2, choices=CMC_CHOICES, default=CUSTOM_CMC, blank=False,
                                   verbose_name='категория комикса')
    comic_original_link = models.URLField(max_length=128, blank=True)
    comic_banner_image = models.FileField(upload_to=comic_banner_directory_path, blank=False,
                                          help_text="лицо комикса")
    tags = TaggableManager()

    def get_preview(self):
        return self.images_set.all().order_by('image')[0:2]

    def get_bookmark_count(self):
        return self.bookmarkcomic_set.all().count()

    def __str__(self):
        return self.comic_name


def images_directory_path(instance, filename):
    folder = str(instance.comic.comic_name).replace(' ', '_')
    name = str(filename).replace(' ', '_')
    return '/'.join(['comic', folder, name])


class Images(models.Model):
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    image = models.FileField(upload_to=images_directory_path)

    def __str__(self):
        return self.comic.comic_name


class BookmarkBase(models.Model):
    class Meta:
        abstract = True

    comic_reader = models.ForeignKey(ComicReader, verbose_name="Comic_Reader_User", on_delete=models.CASCADE)


class BookmarkComic(BookmarkBase):
    class Meta:
        db_table = "bookmark_comic"

    comic = models.ForeignKey(Comic, verbose_name="Comic", on_delete=models.CASCADE)
    page_number = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.comic.comic_name
