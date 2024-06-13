
from django.contrib import messages
from accounts.models import User
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from deeporacles.settings import MAX_VIDEO_SIZE, VIDEO_EXTENSIONS
from contrib.permissions import IsAuthenticatedOrViewOnly
from home.api.serializers import PostSerializer, SavedPostSerializer, UpdateSerializer
from home.models import Post, Savedpost, Update
from settings.models import Area, City, Country, Region
from .serializers import AddressSerializer, AreaSerializer, CitySerializer, ProfileSerializer, RegionSerializer
from rest_framework.decorators import *
from profiles.models import AddressBook, Profile
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from settings.utils import add_notification


class ProfileViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = ProfileSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrViewOnly]

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = Profile.objects.filter(is_active=True) | Profile.objects.filter(id=profile.id)
        return queryset.distinct()

    def create(self, request, *args, **kwargs):
        """
            adds operation success boolean for client
        """
        response = super(ProfileViewSet, self).create(request, *args, **kwargs)
        return Response({'success': True, 'profile': response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        adds operation success boolean for client
        """
        response = super(ProfileViewSet, self).update(request, *args, **kwargs)
        return Response({'success': True, 'profile': response.data}, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        profile = serializer.save()
        content = f'hey friend {profile.first_name} your account information is updated'
        notification = {'type': 'accounts',
                        'content': content}
        add_notification(notification, profile.user)

    def retrieve(self, request, *args, **kwargs):
        """
        adds operation success boolean for client
        """
        response = super(ProfileViewSet, self).retrieve(request, *args, **kwargs)
        return Response({'success': True, "profile": response.data}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """
        adds operation success boolean for client
        """
        response = super(ProfileViewSet, self).list(request, *args, **kwargs)
        return Response({'success': True, 'profiles': response.data}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated,])
class AddressBookDetails(APIView):
	def get(self, request, id, format=None):
		address = AddressBook.objects.get(id = id)
		address_serializers = AddressSerializer(address, many=False)
		regions = RegionSerializer(Region.objects.filter(country=address.country), many=True)
		cities = CitySerializer(City.objects.filter(region=address.region), many=True)
		areas = AreaSerializer(Area.objects.filter(city=address.city), many=True)
		context = {
			'address' : address_serializers.data,
			'regions': regions.data,
			'cities': cities.data,
			'areas': areas.data,
		}
		return Response(context)


@authentication_classes(authentication.SessionAuthentication)
@permission_classes(permissions.IsAuthenticated)
@api_view(['GET',])
def my_posts (request, *args, **kwargs):
    user = request.user
    posts = Post.objects.filter(user=user, active=True)
    serializer = PostSerializer(instance=posts, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@authentication_classes(authentication.SessionAuthentication)
@api_view(['GET',])
def user_posts (request, pk, *args, **kwargs):
    user = User.objects.get(pk=pk)
    posts = Post.objects.filter(user=user, active=True)
    serializer = PostSerializer(instance=posts, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@authentication_classes(authentication.SessionAuthentication)
@permission_classes(permissions.IsAuthenticated)
@api_view(['GET',])
def saved_posts (request, *args, **kwargs):
    user = request.user
    saved_posts = Savedpost.objects.filter(user=user)
    serializer = SavedPostSerializer(instance=saved_posts, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


	# def post(self, request, format=None):
	#     if Profile.objects.get(user = request.user):
	#         pro = Profile.objects.get(user = request.user)
	#         pro.phone = request.data['phone']
	#         pro.address = request.data['address']
	#         pro.city = request.data['city']
	#         pro.country = request.data['country']
	#         pro.save()
	#         pro_ser = ProfileSerializer(pro, many=False)
	#         return Response(pro_ser.data)
	#     pro = Profile.objects.create(
	#         user = request.user,
	#         phone = request.data['phone'],
	#         address = request.data['address'],
	#         city = request.data['city'],
	#         country = request.data['country']
	#     )
	#     pro_ser = ProfileSerializer(pro, many=False)
	#     return Response(pro_ser.data)
 
 
 
@api_view(['POST',])
def create_status_view (request):
    updates = Update(user=request.user)

    if request.method =="POST":
        serializer = UpdateSerializer(updates, data=request.data)
        if 'Video_file' in request.FILES:
            video_file = request.FILES['Video_file']
            video = str(video_file).split('.')
            if video[1] in VIDEO_EXTENSIONS:
                if video_file.size > MAX_VIDEO_SIZE:
                    messages.error(request, 'Video file should not exceed 100 MB')
            else:
                messages.error(request,
                                'the file extension does not match the requirements. Only Video can be uploaded')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes(authentication.SessionAuthentication)
@permission_classes(permissions.IsAuthenticated)
@api_view(['GET',])
def updates(request, *args, **kwargs):
    # Create an empty list to store the user IDs of connections and following users
    my_connections = []

    # Step 1: Include the current user in the connections list
    my_connections.append(request.user)

    # Step 2: Include user IDs of staff users in the connections list (if the current user is staff)
    staff_users = User.objects.filter(is_staff=True)
    staff_users = list(staff_users)
    my_connections.extend(staff_users)

    # Step 3: Include user IDs of connections in the connections list
    connections = request.user.circles.connections.all()
    connections = list(connections)
    my_connections.extend(connections)

    # Step 4: Include user IDs of following users in the connections list
    following = request.user.circles.following.all()
    following = list(following)
    my_connections.extend(following)

    # Filter updates by users in the connections list
    updates = Update.objects.filter(
        active=True,
        user__in=my_connections,
    )

    # Serialize the updates and return the response
    serializer = UpdateSerializer(instance=updates, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

