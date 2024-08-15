import random

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.


class ShortUrl(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=10,
                                 unique=True,
                                 blank=True)
    request_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['original_url']),
            models.Index(fields=['short_url']),
        ]

    def save(self, *args, **kwargs):
        if not self.short_url:
            while True:
                short_url = ''.join(random.choices(
                    settings.ALPHABET,
                    k=settings.SHORT_URL_LENGTH
                ))
                if not ShortUrl.objects.filter(short_url=short_url).exists():
                    break
        super().save(*args, **kwargs)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.original_url} -> {self.short_url}'



