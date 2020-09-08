from django.urls import path
from .views import LogoutView, ReaderSetup, ComicUploading

app_name = 'authapp'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('setting/', ReaderSetup.as_view(), name='setup'),
    path('setting/upload/<int:pk>', ComicUploading.as_view(), name='cup'),
]
