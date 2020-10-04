from django.urls import path
from .views import TagsObserver, SearchView
from django.contrib.auth.decorators import login_required


app_name = 'searchblock'


urlpatterns = [
    path('<str:searching>', SearchView.as_view(), name="by_name"),
    path('tags/<slug>', TagsObserver.as_view(), name="by_tags"),
]
