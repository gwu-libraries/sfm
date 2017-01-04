from django import template
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import intcomma
import json as json_lib
from collections import OrderedDict

from ui.models import Harvest

register = template.Library()


@register.filter
def json(value, name=None):
    rend = u""
    if value:
        try:
            j = json_lib.loads(value, object_pairs_hook=OrderedDict)
        except ValueError:
            j = value
        if isinstance(j, dict):
            rend = render_paragraphs_dict(j)
        elif name:
            rend = render_paragraphs_dict({name: j})
        else:
            rend = render_value(j)
    return mark_safe(rend)


@register.filter
def json_list(value, name=None):
    rend = u""
    if value:
        try:
            j = json_lib.loads(value)
        except ValueError:
            j = value
        if isinstance(j, dict):
            rend = render_dict(j)
        elif name:
            rend = render_dict({name: j})
        else:
            rend = render_value(j)
    return mark_safe(rend)


def render_key(value):
    return value.capitalize().replace(u"_", u" ")


def render_paragraphs_dict(value):
    rend = u""
    for k, v in value.items():
        rend += u"<p><strong>{}</strong>: {}</p>".format(render_key(k), render_value(v))
    return rend


def render_dict(value, ishtml=True):
    rend = u"<ul>" if ishtml else u""
    prefix = u"<li>" if ishtml else u""
    suffix = u"</li>" if ishtml else u","
    for k, v in value.items():
        rend += u"{}{}: {}{}".format(prefix, render_key(k), render_value(v), suffix)
    rend = u"{}</ul>".format(rend) if ishtml else rend[:-1]
    return rend


def render_value(value, ishtml=True):
    if isinstance(value, dict):
        return render_dict(value, ishtml)
    elif isinstance(value, list):
        return render_list(value, ishtml)
    elif value is True:
        return "Yes"
    elif value is False:
        return "No"
    else:
        return value


def render_list(value, ishtml=True):
    rend = u"<ul>" if ishtml else u""
    prefix = u"<li>" if ishtml else u""
    suffix = u"</li>" if ishtml else u","
    for v in value:
        rend += u"{}{}{}".format(prefix, render_value(v), suffix)
    rend = u"{}</ul>".format(rend) if ishtml else rend[:-1]
    return rend


@register.assignment_tag
def json_text(value, ishtml=True, name=None):
    rend = u""
    if value:
        try:
            j = json_lib.loads(value)
        except ValueError:
            j = value
        if isinstance(j, dict):
            rend = render_paragraphs_dict_text(j, ishtml)
        elif name:
            rend = render_paragraphs_dict_text({name: j}, ishtml)
        else:
            rend = render_value(j)
    return mark_safe(rend)


@register.filter
def json_list_text(value, name=None):
    rend = u""
    if value:
        try:
            j = json_lib.loads(value)
        except ValueError:
            j = value
        if isinstance(j, dict):
            rend = render_dict_text(j)
        elif name:
            rend = render_dict_text({name: j})
        else:
            rend = render_value(j)
    return rend


def render_paragraphs_dict_text(value, ishtml=True):
    rend = u""
    for k, v in value.items():
        rend += u"{}: {}\n".format(render_key(k), render_value(v, ishtml))
    return rend


def render_dict_text(value):
    rend = u""
    for k, v in value.items():
        rend += u"{}: {}\n".format(render_key(k), render_value(v))
    return rend


@register.assignment_tag
def join_stats(d, status, sep=", "):
    joined = ""

    empty_extras = ""
    if status == Harvest.RUNNING:
        empty_extras = "Nothing yet"
    elif status == Harvest.REQUESTED:
        empty_extras = "Waiting for update"

    if d:
        for i, (item, count) in enumerate(d.items()):
            if i > 1:
                joined += sep
            joined += "{} {}".format(intcomma(count), item)
    return joined if joined else empty_extras


@register.filter
def name(value):
    if value and hasattr(value, "name"):
        if callable(value.name):
            return value.name()
        return value.name
    elif value and hasattr(value, "label"):
        if callable(value.label):
            return value.label()
        return value.label
    return value


@register.filter
def verbose_name(instance, field_name=None):
    """
    Returns verbose_name for a model instance or a field.
    """
    if field_name:
        return instance._meta.get_field(field_name).verbose_name
    return instance._meta.verbose_name
