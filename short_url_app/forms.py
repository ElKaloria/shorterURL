from django.forms import models

from .models import ShortUrl


class UrlForm(models.ModelForm):
    class Meta:
        model = ShortUrl
        fields = ['original_url']
        labels = {
            'original_url': 'Your url',
        }
