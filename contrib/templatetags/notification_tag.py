from django import template
from contrib.models import Notification

register = template.Library()


@register.inclusion_tag("notification/notification.html", takes_context=True)
def notification(context): 
    request_user = context['request'].user
    notifications = Notification.objects.filter(receiver=request_user).exclude(is_seen=True).order_by('-when')
    return {'notifications': notifications}



@register.inclusion_tag("user_admin/includes/admin_notifications.html", takes_context=True)
def admin_notifications(context): 
    request_user = context['request'].user
    notifications = Notification.objects.filter(receiver=request_user).exclude(is_seen=True).order_by('-when')
    return {'notifications': notifications}
