
import random
from django.http import HttpRequest
from django.utils import timezone
from django.db.models import Min, Max,Avg,Q,Count
from django.contrib.auth.decorators import login_required
from circles.models import Circles
from contrib.models import Message, Notification, Tag
from deeporacles import settings
from noticeboard.models import Faq, Info, SafetyTips
from settings.models import Confsettings, SiteConfiguration
from home.models import *
from deepinfo.models import DeepOracles


def deeporacles(request):
    context = {
        'conf_set': Confsettings.objects.all().first(),
        'site_config': SiteConfiguration.objects.all().first(),
        'deeporacles': DeepOracles.objects.all(),
        'current_year': timezone.now().year,
        'safetytips': SafetyTips.objects.all(),
        'tags': Tag.objects.all(),
        'faq': Faq.objects.all(),
        'infos': Info.objects.all(),
        'site_name': settings.SITE_NAME, 
        'meta_keywords': settings.META_KEYWORDS, 
        'meta_description': settings.META_DESCRIPTION, 
        'request': request,
    }
    return context


def deepchats(request):
    if request.user.is_authenticated:
        notifies = Notification.objects.filter(receiver = request.user)
        messages = [Message.objects.filter((Q(sender=request.user, receiver=user)| Q(receiver = request.user, sender=user))).last() for user in request.user.profile.chatted_with.all()]
        for m in messages:
            if not m:
                messages.remove(m)
        return {
        'notifies': notifies,
        'navmessages': messages if messages else None,
        # 'forum': Forum.objects.filter(forum_admin=request.user)
        }
    else:
        return {
        'message': "sb7",
        'shipping': False
        }

def general_context(request):
    context = {
        'spaces': Space.objects.filter(enable=True),
        'forums': Forum.objects.filter(active=True),
    }
    return context



def users_list(request: HttpRequest) -> dict:
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # Return an empty context if the user is not authenticated
        return {'users': [], 'connections': [], 'rec_connections': []}
    
    # Get the current user
    current_user = request.user
    # Get the list of users excluding the current user
    users = list(Circles.objects.exclude(user=current_user))
    # Get the list of connections for the current user
    my_connections = list(current_user.circles.connections.all())
    # Get the list of users that the current user is following
    following = list(current_user.circles.following.all())

    # Initialize lists
    connections = [user for user in my_connections if user != current_user]
    # Get the list of users that are not in connections or following
    rec_connections = [user for user in users if user not in my_connections + following]
    # Remove the current user from connections
    connections = [user for user in connections if user != current_user]
    # Remove users in connections from rec_connections
    rec_connections = [user for user in rec_connections if user not in connections]
    # Get a random sample of 20 users from rec_connections
    random_list = random.sample(rec_connections, min(len(rec_connections), 20))
    # Remove users in random_list from connections
    connections = [user for user in connections if user not in random_list]

    # Create the context dictionary
    context = {
        # 'users': connections,
        'connections': my_connections,
        'rec_connections': random_list
    }
    
    return context
