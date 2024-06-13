
from circles.models import Circles, Forum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, viewsets, status
from contrib.models import Notification
from rest_framework.decorators import *
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string



class FollowAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, pk, format=None, *args, **kwargs):
        """
        Retrieves a specific circle object based on the provided primary key and updates the following status for the current user. 
        The function returns a dictionary containing the keys 'updated' and 'following' with their corresponding boolean values.
        """
        # Get the circle object based on the primary key
        circle = Circles.objects.get(pk=pk)
        
        updated = False
        following = False
        user = request.user
        
        # Check if the user is authenticated
        if user.is_authenticated:
            # Check if the request user is already following the circle
            if request.user in circle.followers.all():
                following = True
                circle.followers.remove(request.user)
                request.user.circles.following.remove(circle.user)
                
                # Check if the circle user is in the connections of the request user
                if circle.user in request.user.circles.connections.all():
                    request.user.circles.connections.remove(circle.user)
                    circle.user.circles.connections.remove(request.user)
            else:
                following = False
                circle.followers.add(request.user)
                request.user.circles.following.add(circle.user)
                absolute_url = request.user.profile.get_absolute_url
                text_preview = "{0} Started following you".format(request.user.profile.name())
                Notification.objects.create(sender=request.user, text_preview=text_preview, receiver=circle.user, content_object=circle, redirect_url=absolute_url)
                
                # Add notifications for following and connecting
                if circle.user in request.user.circles.followers.all():
                    request.user.circles.connections.add(circle.user)
                    circle.user.circles.connections.add(request.user)
                    text_preview = "You are now connected with {0}".format(request.user.profile.name())
                    Notification.objects.create(sender=request.user, text_preview=text_preview, receiver=circle.user, content_object=circle, redirect_url=absolute_url)
            updated = True
        data = {
            "updated": updated,
            "following": following
        }
        return Response(data)


class ForumFollowAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, pk, format=None, *args, **kwargs):
        """
        Retrieves a specific forum object based on the provided primary key and updates the following status for the current user. 
        The function returns a dictionary containing the keys 'updated' and 'following' with their corresponding boolean values.
        """
        # Initialize flags
        updated = False
        following = False

        # Check if the forum exists, and if not, return a 404 error.
        try:
            forum = Forum.objects.get(pk=pk)
        except Forum.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check if the user is authenticated, and if not, return a 401 error.
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user is already following the forum, and if so, remove them from the followers.
        if request.user in forum.followers.all():
            following = True
            forum.followers.remove(request.user)
        # Otherwise, add the user to the followers.
        else:
            following = False
            forum.followers.add(request.user)

        # Set the updated flag to True
        updated = True

        # Prepare the response data
        data = {
            "updated": updated,
            "following": following
        }
        return Response(data)



class LeaveForumView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

    """
    Delete a forum.
    If the requesting user is the forum admin, the forum is deleted.
    If the requesting user is not the forum admin, the user is removed
    from the forum members.
    Returns:
        204 No Content: The forum was deleted or the user was removed from the forum.
    """
    def delete(self, request, pk, format=None):
        forum = Forum.objects.get(pk=pk)
        if request.user != forum.forum_admin:
            # If the user is not the forum admin, remove them from the forum members.
            forum.forum_members.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # If the user is the forum admin, delete the forum.
            forum.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


# class JoinRequestView(APIView):
#     authentication_classes = (authentication.SessionAuthentication,)
#     permission_classes = (permissions.IsAuthenticated, )
    
#     """
#     Handles join request for a forum.

#     If the user is already in the forum members waiting list, the user is removed from the list.
#     If the user is not in the forum members waiting list, the user is added to the list.
#     Returns:
#         204 No Content: The user was added/removed from the forum members waiting list.
#     """
#     def post(self, request, pk, format=None):
#         forum = Forum.objects.get(pk=pk)
#         # Check if the user is already in the forum members waiting list.
#         if request.user in forum.forum_members_waiting.all():
#             # If the user is already in the list, remove them from the list.
#             forum.forum_members_waiting.remove(request.user)
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             # If the user is not in the list, add them to the list.
#             forum.forum_members_waiting.add(request.user)
#             return Response(status=status.HTTP_204_NO_CONTENT)


class JoinRequestView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, pk, format=None, *args, **kwargs):
        """
        Retrieves a specific forum object based on the provided primary key and updates the following status for the current user. 
        The function returns a dictionary containing the keys 'updated' and 'following' with their corresponding boolean values.
        """
        # Initialize flags
        updated = False
        joined = False

        # Check if the forum exists, and if not, return a 404 error.
        try:
            forum = Forum.objects.get(pk=pk)
        except Forum.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check if the user is authenticated, and if not, return a 401 error.
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user is already following the forum, and if so, remove them from the followers.
        if request.user in forum.forum_members_waiting.all():
            joined = True
            forum.forum_members_waiting.remove(request.user)
        # Otherwise, add the user to the followers.
        else:
            joined = False
            forum.forum_members_waiting.add(request.user)
            absolute_url = "/circles/forum-{0}/members".format(int(pk))
            text_preview = "{0} Requested to join {1}".format(request.user, forum.forum_name)
            Notification.objects.create(sender=request.user, text_preview=text_preview, receiver=forum.forum_admin, content_object=forum, redirect_url=absolute_url)

        # Set the updated flag to True
        updated = True

        # Prepare the response data
        data = {
            "updated": updated,
            "joined": joined
        }
        return Response(data)



class ForumBlockingUser(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

    """
    Unblocks a user from a forum.

    If the user is a forum member, the user is removed from the forum members.
    If the user is a forum sub-admin, the user is removed from the forum sub-admins.
    If the user is a forum member waiting, the user is removed from the forum member waiting.
    If the user is a forum member blocked, the user is removed from the forum member blocked.
    Returns:
        200 OK: The user was unblocked from the forum.
    """
    def post(self, request, forum_id, user_id, format=None):
        # Retrieves the forum and user objects based on the primary keys provided in the URL.
        forum = Forum.objects.get(pk=forum_id)
        user = User.objects.get(pk=user_id)

        # If the user is a forum member, remove them from the forum members.
        if user in forum.forum_members.all():
            forum.forum_members.remove(user)
        # If the user is a forum sub-admin, remove them from the forum sub-admins.
        elif user in forum.forum_sub_admin.all():
            forum.forum_sub_admin.remove(user)
        # If the user is a forum member waiting, remove them from the forum member waiting.
        elif user in forum.forum_members_waiting.all():
            forum.forum_members_waiting.remove(user)
        # If the user is a forum member blocked, remove them from the forum member blocked.
        elif user in forum.forum_members_blocked.all():
            forum.forum_members_blocked.remove(user)

        return Response({'done': True})


class AcceptForumJoinReq(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        """
        Accepts a forum join request by adding the user to the forum members and removing them from the
        forum members waiting list.
        Args:
            request (Request): The request containing the forum and user primary keys.
            format (str): Not used, exists for compatibility with parent method.
        Returns:
            Response:
                success (bool): Whether the action was successful or not.
                status (int):
                    HTTP_200_OK if the action was successful,
                    HTTP_400_BAD_REQUEST if the forum or user primary key could not be found.
        """
        forum_pk = request.data.get('forum')
        # Retrieves the forum object based on the primary key provided in the request.
        forum = Forum.objects.filter(pk=forum_pk)
        # If the forum could not be found, return a 400 Bad Request response.
        if not forum:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
        forum = forum[0]

        user_pk = request.data.get('user')
        # Retrieves the user object based on the primary key provided in the request.
        user = User.objects.filter(pk=user_pk)
        # If the user could not be found, return a 400 Bad Request response.
        if not user:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
        user = user[0]

        # Adds the user to the forum members.
        forum.forum_members.add(user)
        # Removes the user from the forum members waiting list.
        forum.forum_members_waiting.remove(user)

        # Returns a 200 OK response indicating that the action was successful.
        return Response({'success': True}, status=status.HTTP_200_OK)


class DenyForumJoinReq(APIView):
	""" This view is used to deny a forum join request.
		Args:
			request (Request): The request containing the forum and user primary keys.
		Returns:
			Response:
				success (bool): Whether the action was successful or not.
				status (int):
					HTTP_200_OK if the action was successful,
					HTTP_400_BAD_REQUEST if the forum or user primary key could not be found.
	"""
	
	# Only authenticated users are allowed to deny forum join requests.
	authentication_classes = (authentication.SessionAuthentication,)
	# Checks if the user is authenticated and is a member of the forum admin.
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
	
	def post(self, request, format=None):
		# Retrieves the forum primary key from the request.
		forum_pk = request.data.get('forum')
		# Retrieves the forum object based on the primary key provided in the request.
		forum = Forum.objects.filter(pk=forum_pk)
		# If the forum could not be found, return a 400 Bad Request response.
		if not forum:
			return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
		forum = forum[0]
		
		# Retrieves the user primary key from the request.
		user_pk = request.data.get('user')
		# Retrieves the user object based on the primary key provided in the request.
		user = User.objects.filter(pk=user_pk)
		# If the user could not be found, return a 400 Bad Request response.
		if not user:
			return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
		user = user[0]
		
		# Removes the user from the forum members waiting list.
		forum.forum_members_waiting.remove(user)
		
		# Returns a 200 OK response indicating that the action was successful.
		return Response({'success': True}, status=status.HTTP_200_OK)


@login_required
def ForumAssignUserToSubAdmin(forum , user):
	forum.forum_sub_admin.add(user)
	return JsonResponse({'done':True})


@login_required
def ForumAssignToUser(forum , user):
	if user in forum.forum_sub_admin.all():
		forum.forum_sub_admin.remove(user)
		return JsonResponse({'done':True})
	else:
		return JsonResponse({'done': False})

@login_required
def ForumMembersAssigns(request):
	if request.method == 'POST' and request.user == forum.forum_admin:
		user = User.objects.get(pk=request.POST.get('UserPk'))
		forum = Forum.objects.get(pk=request.POST.get('forumPk'))
		assign = request.POST.get('assign')
		if assign == 'subadmin':
			return ForumAssignUserToSubAdmin(forum, user)
		elif assign == 'block':
			return ForumBlockingUser(forum, user)
	else :
		raise PermissionDenied()

@login_required
def InviteMembers(request, pk, slug):
    forum = Forum.objects.get(pk=pk, slug=slug)
    if request.user == forum.forum_admin or request.user in forum.forum_sub_admin.all():
        if request.method == 'POST':
            absolute_url = "/circles/forum/{0}".format(int(slug))
            text_preview = "{0} invited you to join his group {1}".format(request.user(), forum.forum_namee)
            Notification.objects.create(receiver=User.objects.get(pk=request.POST.get('user_pk')), sender=request.user, text_preview=text_preview, content_object=forum, redirect_url=absolute_url)
    else:
        return HttpResponseRedirect((reverse('forum', args=[str(pk),])))	

