from django.views.generic import ListView, View
from mainapp.models import Comic, Images, BookmarkComic
from authapp.models import ComicReader
from django.http import HttpResponse
from django.shortcuts import render
import json


class Error404(View):
    template_name = 'mainapp/404.html'

    def get(self, request, exception):
        context = {'title': "Dog's poop!"}
        return render(request, self.template_name, context)


class ComicObserver(ListView):
    model = Comic
    template_name = 'mainapp/comic_list.html'
    context_object_name = 'comics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reading_comic'] = False
        return context


class ComicReading(ListView):
    model = Images
    template_name = 'mainapp/read_comic.html'
    context_object_name = 'images'
    paginate_by = 1

    def get_queryset(self):
        pk = self.kwargs.get('comic_id')
        cr = Images.objects.filter(comic=pk).order_by('image')
        return cr

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('comic_id')
        context['reading_comic'] = True
        context['comic_id'] = pk
        return context


class BookmarkView(View):
    model = BookmarkComic

    def post(self, request, comic_id):
        user = ComicReader.objects.get(username=request.user)
        comic_id = Comic.objects.get(id=comic_id)
        bookmark, created = self.model.objects.get_or_create(comic_reader=user, comic=comic_id)
        if not created:
            bookmark.delete()

        return HttpResponse(json.dumps({
            "result": created,
            "count": self.model.objects.filter(comic=comic_id).count()
        }), content_type="application/json")


class About(View):
    template_name = 'mainapp/about_us.html'

    def get(self, request):
        return render(request, self.template_name, None)
