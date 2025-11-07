# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django import template

register = template.Library()  # 必须要有这行


@register.simple_tag
def user_space(size):
    if size >= 1024 * 1024 * 1024:
        return "%.2f GB" % (size / (1024 * 1024 * 1024),)
    elif size >= 1024 * 1024:
        return "%.2f MB" % (size / (1024 * 1024),)
    elif size >= 1024:
        return "%.2f KB" % (size / 1024,)
    else:
        return "%d B" % size