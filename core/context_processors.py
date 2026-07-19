"""Global context processors available to all templates."""
from django.conf import settings


def global_settings(request):
    """Expose site-wide settings to every template."""
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_TAGLINE': settings.SITE_TAGLINE,
    }