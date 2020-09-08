from django.urls import path
from .views import ComicObserver, ComicReading, BookmarkView, About
from django.contrib.auth.decorators import login_required


app_name = 'mainapp'


urlpatterns = [
    path('', ComicObserver.as_view(), name="observer"),
    path('read/<int:comic_id>', ComicReading.as_view(), name="reader"),
    path('bookmark/<int:comic_id>', login_required(BookmarkView.as_view()), name='bookmark'),
    path('aboutus/', About.as_view(), name='about'),
]
