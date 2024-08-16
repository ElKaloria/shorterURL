from .models import ShortUrl


def get_original_url(url: str) -> str:
    try:
        full_url = ShortUrl.objects.get(short_url__exact=url)

    except ShortUrl.DoesNotExist:
        raise KeyError("This url does not exist")

    full_url.request_count += 1
    full_url.save()
    return full_url.original_url


def original_url_exist(url: str) -> bool:
    try:
        ShortUrl.objects.get(original_url__exact=url)
        return True
    except ShortUrl.DoesNotExist:
        return False


def get_short_url(url: str) -> str:
    try:
        return ShortUrl.objects.get(original_url__exact=url).short_url
    except ShortUrl.DoesNotExist:
        raise KeyError("This url does not exist")