from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.http import HttpResponseRedirect
from django.conf import settings
from authapp.models import ComicReader
from authapp.forms import ComicUploderForm, ComicReaderEditForm
from django.forms.models import model_to_dict
from django.urls import reverse
from mainapp.models import Comic, Images


class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)


class ComicUploading(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, DetailView):
    model = Comic
    context_object_name = 'comic_details'
    template_name = 'authapp/comic_details_list.html'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        dv = Comic.objects.filter(id=pk)
        return dv

    def post_ajax(self, request, *args, **kwargs):
        try:
            upload_comic = Comic.objects.get(id=kwargs.get('pk'))
        except upload_comic.DoesNotExist:
            error_dict = {'message': 'Comic not found.'}
            return self.render_json_response(error_dict, status=404)

        uploaded_file = request.FILES['file']
        Images.objects.create(comic=upload_comic, image=uploaded_file)

        response_dict = {
            'message': 'File uploaded successfully!',
        }

        return self.render_json_response(response_dict, status=200)


class ReaderSetup(LoginRequiredMixin, ListView):
    # TODO: rewrite this ugly class
    model = ComicReader
    context_object_name = 'settings'
    template_name = 'authapp/setting_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reading_comic'] = False
        if 'opener' not in context['settings']:
            context['opener'] = 'bookmarks'
        else:
            context['opener'] = context['settings']['opener']

        if 'uploader_form' not in context and 'uploader_form' not in context['object_list']:
            context['uploader_form'] = ComicUploderForm
        elif 'uploader_form' in context['object_list']:
            context['uploader_form'] = context['object_list']['uploader_form']
        if 'edit_form' not in context and 'edit_form' not in context['object_list']:
            context['edit_form'] = ComicReaderEditForm(context['object_list'])
        elif 'edit_form' in context['object_list']:
            context['edit_form'] = context['object_list']['edit_form']

        return context

    def get(self, request, *args, **kwargs):
        default_data = {'age': request.user.age,
                        'darck_comic': request.user.darck_comic,
                        'dc_comic': request.user.dc_comic,
                        'marvel_comic': request.user.marvel_comic,
                        'adult_comic': request.user.adult_comic,
                        'hentai_comic': request.user.hentai_comic}
        return render(request, self.template_name, self.get_context_data(object_list=default_data))

    def post(self, request):
        context = {}

        if 'uploading' in request.POST:
            uploader_form = ComicUploderForm(request.POST, files=request.FILES)

            if uploader_form.is_valid():
                if not Comic.objects.filter(comic_name=request.POST['comic_name']):
                    comic_step_one = uploader_form.save()
                    context['opener'] = 'uploading'
                    return redirect('/auth/setting/upload/{}'.format(comic_step_one.pk))
                else:
                    context['opener'] = 'uploading'
                    context['errors'] = 'Такой комикс уже существует'
            else:
                context['uploader_form'] = uploader_form
                context['opener'] = 'uploading'

        if 'editing' in request.POST:
            edit_form = ComicReaderEditForm(request.POST, instance=request.user)

            if edit_form.is_valid():
                check_list = ['age', 'darck_comic', 'dc_comic', 'marvel_comic', 'adult_comic', 'hentai_comic']
                edit_form.save()
                context['opener'] = 'settings'
                comic = model_to_dict(ComicReader.objects.get(username=request.user))
                comic = {k: comic[k] for k in check_list}
                return render(request, self.template_name, self.get_context_data(object_list=comic, settings=context))
            else:
                context['edit_form'] = edit_form
                context['opener'] = 'settings'

        return render(request, self.template_name, self.get_context_data(object_list=context))


class ReaderSetting(ListView):
    model = ComicReader
    template_name = 'authapp/setting_list.html'
    context_object_name = 'settings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reading_comic'] = False
        return context
