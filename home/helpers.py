
import os
import pipes
import random
import time

from django.core.files import File
from contrib.models import PostLocation

from home.models import Post, PostView, Sound

from contrib.exceptions import CustomAPIException
from contrib.utils import (
    TagCentral,
    get_ip_address,
    get_ip_details
)


class PostUploader:
    """Handle post upload."""

    @staticmethod
    def handle_location(request):
        """Handle location from where post was uploaded."""
        ip_address = get_ip_address(request)
        if ip_address or ip_address == '127.0.0.1':
            location = get_ip_details(ip_address)
            try:
                loc = PostLocation.objects.create(
                    ip_address=ip_address,
                    state=location.region,
                    country=location.country_name,
                    latitude=location.latitude,
                    longitude=location.longitude,
                    postal_code=location.postal,
                    city=location.city
                )
                return loc
            except BaseException:
                return

    def upload(self, user, file, details, request):
        """Upload a post in model."""
        try:
            if details.get('share_post_uuid', None):
                original_post = Post.objects.get(
                    uuid=details.get('share_post_uuid')
                )
            sound = None
            if details.get('sound_uuid', None):
                sound = Sound.objects.get(
                    uuid=details.get('sound_uuid', None)
                )
            location = self.handle_location(request)
            is_location_added = True if location else False
            post = Post.objects.create(
                user=user,
                video_file=file['video_file'],
                video_gif=file['video_gif'],
                content=details.get('content', None),
                sound=sound,
                share_pointer=original_post,
                is_pornographic=details.get('is_pornographic', False),
                is_downloadable=details.get('is_downloadable', False),
                uploaded_location=location
            )
            is_tags_added = TagCentral().handle_tag_cycle(post)
            return {
                'message': ('Post successfully Uploaded, '
                            'hashtags added {},'
                            'location added {}').format(
                    is_tags_added,
                    is_location_added
                )
            }
        except BaseException as e:
            return {'message': 'Error Occured: {}'.format(e)}


class PostUploadException(CustomAPIException):
    """Raise when post upload flow fails."""

    default_code = 'post_upload_failure'
    default_detail = 'Post Upload Failed.'


def is_post_viewed(user, post):
    """Return if post is marked favorite."""
    return PostView.objects.filter(
        post=post,
        user=user
    ).exists()

class AudioConverter:
    """Convert to audio."""

    def __init__(self):
        """Declare all class variables."""
        self.file_name = ''

    @staticmethod
    def audio_extractor(file_name):
        try:
            file, file_extension = os.path.splitext(file_name)
            file = pipes.quote(file)
            output_file = '{}_{}'.format(
                file,
                random.randint(0, 999999)
            )
            video_to_wav = 'ffmpeg -i {}{} {}.wav'.format(
                file,
                file_extension,
                output_file
            )
            final_audio = 'lame {}.wav {}.mp3'.format(
                output_file,
                output_file
            )
            os.system(video_to_wav)
            os.system(final_audio)
            return '{}.mp3'.format(output_file)
        except OSError as err:
            print(str(err))

    def _add_to_sound(self, file_name, post):
        """Store audio to Sound model."""
        with open(file_name, 'rb') as fi:
            sound = Sound.objects.create(
                user=post.user,
                sound_file=File(fi, name=os.path.basename(fi.name)),
                is_extracted_audio=True
            )
            post.sound = sound
            post.save()

    def extract(self, post_uuid):
        """Extract audio from one post."""
        post = Post.objects.get(uuid=post_uuid)
        file_name = post.video_file.path
        audio_file_path = self.audio_extractor(file_name)
        time.sleep(1 * 60)
        self._add_to_sound(
            audio_file_path,
            post
        )


class SoundUploader:
    """Handle sound upload."""

    @staticmethod
    def upload(user, file, details):
        """Upload a sound in model."""
        try:
            Sound.objects.create(
                name=details.get('name', None),
                user=user,
                sound_file=file['sound_file'],
                sound_cover=file.get('sound_cover', None),
                category__name=details.get('category', None)
            )
            return {'message': 'Succesfully Uploaded'}
        except BaseException as e:
            return {'message': 'Error Occured: {}'.format(e)}
