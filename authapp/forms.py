from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from .models import ComicReader
from mainapp.models import Comic


class ComicUploderForm(ModelForm):
    class Meta:
        model = Comic
        fields = ['comic_name', 'comic_description', 'comic_author', 'comic_artist', 'comic_genre',
                  'comic_original_link', 'comic_banner_image']


class ComicReaderEditForm(UserChangeForm):
    class Meta:
        model = ComicReader
        fields = ['age', 'darck_comic', 'dc_comic', 'marvel_comic', 'adult_comic', 'hentai_comic']

    def __init__(self, *args, **kwargs):
        super(ComicReaderEditForm, self).__init__(*args, **kwargs)
        del self.fields['password']
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 16:
            raise forms.ValidationError("Вы слишком молоды!")

        return data
