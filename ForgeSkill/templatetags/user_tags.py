from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse

register = template.Library()

@register.simple_tag
def user_link(user, text=None):
    """Return a safe anchor linking to the public profile of `user`.
    Usage: {% user_link user %} or {% user_link user "Custom text" %}
    """
    if not user:
        return ''
    display = text if text is not None else (user.get_full_name() or user.username)
    # Prefer username-based public profile URL if available
    try:
        url = reverse('public_profile_username', args=[user.username])
    except Exception:
        # Fallback to id-based route
        url = reverse('public_profile', args=[user.id])
    return mark_safe(f'<a href="{url}" class="user-link">{display}</a>')
