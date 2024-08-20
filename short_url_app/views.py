from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .forms import UrlForm
from .models import ShortUrl
from .utils import get_original_url, original_url_exist, get_short_url


# Create your views here.
def redirect_to_original_url(request, short_url):
    try:
        original_url = get_original_url(short_url)
        return redirect(original_url)
    except Exception as e:
        return HttpResponse(e.args)


@login_required
def form_view(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        original_url = form.data['original_url']
        if original_url_exist(original_url):
            return render(request, 'url_app/form_redirect.html',
                          {'short_url': get_short_url(original_url)})

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return render(request, 'url_app/form_redirect.html',
                          {'short_url': new_form.short_url})
    else:
        form = UrlForm()
    return render(request, 'url_app/index.html', {'form': form})


class URLList(ListView):
    model = ShortUrl
    template_name = 'url_app/list_url.html'
    context_object_name = 'urls'

    def get_queryset(self):
        user = self.kwargs.get('username')
        return ShortUrl.objects.filter(user__username__exact=user)


class UserList(ListView):
    model = User
    template_name = 'url_app/list_user.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all()


