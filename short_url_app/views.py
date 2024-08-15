from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import UrlForm
from .utils import get_original_url


# Create your views here.
def redirect_to_original_url(request, short_url):
    try:
        original_url = get_original_url(short_url)
        return redirect(original_url)
    except Exception as e:
        return HttpResponse(e.args)


@login_required
def index(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return render(request, 'url_app/form_redirect.html',
                          {'short_url': form.cleaned_data['short_url']})
    else:
        form = UrlForm()
    return render(request, 'url_app/index.html', {'form': form})
