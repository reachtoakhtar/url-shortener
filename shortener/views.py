from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import View
from .forms import SubmitUrlForm
from .models import ShortURL


class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        bg_image = 'http://www.gayalliance.org/wp-content/uploads/2015/04/234436-solid-color-backgrounds-1140x600.jpg'
        context = {
            "title": "akhtar.com",
            "form": the_form,
            "bg_image": bg_image
        }
        return render(request, "shortener/home.html", context)

    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {
            "title": "akhtar.com",
            "form": form
        }
        template = "shortener/home.html"
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            obj, created = ShortURL.objects.get_or_create(url=new_url)
            context = {
                "object": obj,
                "created": created,
            }
            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"

        return render(request, template ,context)


class URLRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        qs = ShortURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        return HttpResponseRedirect(obj.url)

