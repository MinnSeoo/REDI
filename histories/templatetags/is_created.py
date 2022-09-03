from django import template
from histories import models
import datetime

register = template.Library()


@register.simple_tag
def is_created(user, day):
    try:
        date = datetime.date(day.year, day.month, day.number)
        models.History.objects.get(date=date, user__pk=user.pk)
        return True
    except models.History.DoesNotExist:
        return False
