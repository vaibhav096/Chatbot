from django import template
from django.utils.html import escape
import markdown2

register = template.Library()

@register.filter
def escape_and_preserve_indentation(content):
    # Escape HTML tags and preserve indentation
    escaped_content = escape(content)
    return markdown2.markdown(escaped_content)

@register.filter
def preserve_indentation(content):
    # Preserve indentation using <pre> tags
    return f"<pre>{content}</pre>"