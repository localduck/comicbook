import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from mainapp.models import Comic
from taggit.models import Tag


def tag_search(slug, token=None):
    tag = get_object_or_404(Tag, slug=slug)
    comics = Comic.objects.filter(tags=tag)
    return comics


def tags_search(slug, token=None):
    result = []
    tags = Tag.objects.filter(slug__startswith=slug)
    if token is not None:
        return tag_search(slug)
    else:
        for tag in tags:
            result.append(['-t ' + tag.slug])
        return result


def name_search(slug, token=None):
    result = []
    comics = Comic.objects.filter(comic_name__startswith=slug)
    if token is not None:
        return comics
    else:
        for comic in comics:
            result.append(['-n ' + comic.comic_name])
        return result


def auth_search(slug, token=None):
    result = []
    comics = Comic.objects.filter(comic_author__startswith=slug)
    if token is not None:
        return comics
    else:
        for comic in comics:
            result.append(['-a ' + comic.comic_author])
        return result


class TagsObserver(View):
    # template_name = 'searchblock/tags_list.html' 4 custom's this page
    template_name = 'mainapp/comic_list.html'
    context_object_name = 'comics'

    def get(self, request, slug):
        context = {'title': "Tags context!"}
        comics = tag_search(slug)
        context['comics'] = comics
        return render(request, self.template_name, context)


class SearchView(View):
    # template_name = 'searchblock/search_list.html' 4 custom's this page
    template_name = 'mainapp/comic_list.html'
    search_tool = {'-t': tags_search, '-n': name_search, '-a': auth_search}

    def get(self, request, searching):
        context = {'title': "Searching result!"}
        if searching[:2] in self.search_tool.keys():
            result = self.search_tool[searching[:2]](searching[3:], token='s')
        else:
            result = Comic.objects.filter(comic_name__startswith=searching)
        context['comics'] = result
        return render(request, self.template_name, context)

    def post(self, request, searching):
        result = []
        if request.is_ajax():
            searching = searching.split('/')[-1]
            print(searching)
            if searching[:2] in self.search_tool.keys():
                result = self.search_tool[searching[:2]](searching[3:])
            else:
                comics = Comic.objects.filter(comic_name__startswith=searching)
                for comic in comics:
                    result.append(comic.comic_name)
            return HttpResponse(json.dumps({"result": result}), content_type="application/json")
