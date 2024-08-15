from .models import ShortUrl


def get_original_url(url: str) -> str:
    try:
        full_url = ShortUrl.objects.get(short_url__exact=url)

    except ShortUrl.DoesNotExist:
        raise KeyError("This url does not exist")

    full_url.request_count += 1
    full_url.save()
    return full_url.original_url
