from django.core.serializers.python import Serializer
from django.contrib.humanize.templatetags.humanize import naturaltime
from contrib.models import Tag
import ipinfo
from django.conf import settings


def get_ip_address(request):
    """Get IP address from request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_ip_details(ip_address=None):
    """Get location based information from IP Address."""
    ip_info_token = getattr(settings, "IPINFO_TOKEN", None)
    ip_info_settings = getattr(settings, "IPINFO_SETTINGS", {})
    ip_data = ipinfo.getHandler(
        ip_info_token,
        **ip_info_settings
    ).getDetails(ip_address)
    return ip_data


class LazyNotificationEncoder(Serializer):
	"""
	Serialize a Notification into JSON. 
	There are 3 types
		1. ConnectionRequest
		2. FriendList
		3. UnreadChatRoomMessage
	"""
	def get_dump_object(self, obj):
		dump_object = {}
		if obj.get_content_object_type() == "ConnectionRequest":
			dump_object.update({'notification_type': obj.get_content_object_type()})
			dump_object.update({'notification_id': str(obj.pk)})
			dump_object.update({'verb': obj.verb})
			dump_object.update({'is_active': str(obj.content_object.is_active)})
			dump_object.update({'is_read': str(obj.is_seen)})
			dump_object.update({'natural_timestamp': str(naturaltime(obj.when))})
			dump_object.update({'timestamp': str(obj.when)})
			dump_object.update({
				'actions': {
					'redirect_url': str(obj.redirect_url),
				},
				"from": {
					"title": str(obj.sender.profile.name),
					"image_url": str(obj.sender.profile.picture.url)
				}
			})
		if obj.get_content_object_type() == "Circles":
			dump_object.update({'notification_type': obj.get_content_object_type()})
			dump_object.update({'notification_id': str(obj.pk)})
			dump_object.update({'verb': obj.verb})
			dump_object.update({'natural_timestamp': str(naturaltime(obj.when))})
			dump_object.update({'is_read': str(obj.is_seen)})
			dump_object.update({'timestamp': str(obj.when)})
			dump_object.update({
				'actions': {
					'redirect_url': str(obj.redirect_url),
				},
				"from": {
					"title": str(obj.sender.profile.name),
					"image_url": str(obj.sender.profile.picture.url)
				}
			})
		if obj.get_content_object_type() == "UnreadChatRoomMessages":
			dump_object.update({'notification_type': obj.get_content_object_type()})
			dump_object.update({'notification_id': str(obj.pk)})
			dump_object.update({'verb': obj.verb})
			dump_object.update({'natural_timestamp': str(naturaltime(obj.when))})
			dump_object.update({'timestamp': str(obj.when)})
			dump_object.update({
				'actions': {
					'redirect_url': str(obj.redirect_url),
				},
				"from": {
					"title": str(obj.content_object.get_other_user.profile.name),
					"image_url": str(obj.content_object.get_other_user.profile.picture.url)
				}
			})

		return dump_object



class TagCentral:
    """Handle all tag functions."""

    @staticmethod
    def extract_tags(post_content):
        """Extract all tag."""
        return set(
            part[1:] for part in post_content.split() if part.startswith('#')
        )

    @staticmethod
    def increment_tag_count(tag_obj):
        """Increment count of tag."""
        tag_obj.views += 1
        tag_obj.save()

    @staticmethod
    def store_tag(tag):
        """Store all tags present in post description."""
        try:
            Tag.objects.create(
                title=tag
            )
        except BaseException:
            return

    def link_all_tags_to_post(self, tag, post):
        """Link one tag to a post."""
        tag_obj = Tag.objects.get(title=tag)
        Tag.objects.create(content_object=post)
        self.increment_tag_count(tag_obj)

    def handle_tag_cycle(self, post):
        """Handle all tags."""
        try:
            tags = self.extract_tags(post.content)
            for tag in tags:
                self.store_tag(tag)
                self.link_all_tags_to_post(tag, post)
            return True
        except BaseException as e:
            return False
