

from rest_framework import serializers
from circles.models import Forum
from contrib.models import Comment
from home.models import Post, PostFiles, Savedpost, Share, Sound, SoundCategory, Update

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'picture', 'Audio_file','Video_file',
            'slug','user'
            ]
        depth = 2

class SavedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Savedpost
        fields = [ 'post','created_at','user' ]
        depth = 2


class PostShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields =[
            'user', 'posts', 'date_posted'
        ]
        extra_kwargs = {
            'user': {"read_only": True,},
            'date_posted': {"read_only": True,},
        }


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'id', 'content_object', 'comment', 'comment_date', 'reply', 'media', 
                  'content_type', 'object_id', 'ip_address')
        extra_kwargs = {
            'user': {"read_only": True,},
            'comment_date': {"read_only": True,},
        }


class SoundCategorySerializer(serializers.ModelSerializer):
    """Serializer for sound category model."""

    class Meta:
        model = SoundCategory
        fields = ('uuid', 'name', 'icon', 'description')


class SoundSerializer(serializers.ModelSerializer):
    """Serializer for sound model."""
    category = SoundCategorySerializer()

    class Meta:
        model = Sound
        fields = (
            'uuid', 'name', 'user', 'sound_file', 'copyright', 'category', 'sound_cover'
        )


class VideoSerializer(serializers.ModelSerializer):
    """Serializer for post model."""
    sound = SoundSerializer()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    shares = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    is_viewed = serializers.SerializerMethodField()

    def get_is_viewed(self, obj):
        request = self.context.get('request')
        if not request:
            return False

    class Meta:
        model = Post
        fields = (
            'uuid', 'profile', 'sound', 'video_file',
            'video_gif', 'description', 'category',
            'likes', 'shares', 'comments', 'views',
            'is_downloadable', 'is_viewed'
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = [
            'id',  'content', 'media', 'slug', 'user', 'comments', 'views','likes'
            ]
        depth = 2

# class ForumSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Forum
#         fields = ('id', 'group_name')


# class SnippetSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only = True)
#     ReactsCount = serializers.SerializerMethodField(method_name = 'ReactsCount')

#     def ReactsCount(self, comment):
#         return comment.reacts_count()

#     class Meta:
#         model = Comment
#         fields = ('user', 'id', 'content_object', 'comment', 'comment_date', 'reply', 'media', 
#                   'content_type', 'object_id', 'ip_address')


# class PostFilesSerializers(serializers.ModelSerializer):

#     class Meta:
#         model = PostFiles
#         fields = ('id', 'content', 'media')

# class SharedPostSerializer(serializers.ModelSerializer):
#     files = PostFilesSerializers(many = True, source = 'post_file' , read_only = True)
#     author = UserSerializer(read_only = True)

#     class Meta:
#         model = Post
#         fields = ('id', 'author', 'forum', 'files', 'content', 'DatePublished')

# class PostSerializer(serializers.ModelSerializer):
#     files = PostFilesSerializers(many = True, source = 'post_file', read_only = True)
#     author = UserSerializer(read_only = True)
#     forum = ForumSerializer(read_only = True)
#     ReactsCounter = serializers.SerializerMethodField(method_name = 'ReactsCount')
#     SharesCounter = serializers.SerializerMethodField(method_name = 'SharesCount')
#     CommentsCounter = serializers.SerializerMethodField(method_name = 'CommentsCount')
#     share = SharedPostSerializer(read_only = True)
#     checking_per = serializers.SerializerMethodField(method_name = 'checking_perm')
#     checking_reactions = serializers.SerializerMethodField(method_name = 'checking_react')
#     checking_shares = serializers.SerializerMethodField(method_name = 'checking_share')
#     DatePublished = serializers.SerializerMethodField(method_name = 'getDate')

#     def getDate(self, post):
#         return post.date()

#     def ReactsCount(self, post):
#         return post.reacts_count()

#     def SharesCount(self, post):
#         return post.shared_post.count()

#     def CommentsCount(self, post):
#         return post.comments.count()

#     def checking_perm(self, post):
#         visitor = self.context['request'].user
#         if visitor == post.author:
#             return True
#         else:
#             return False

#     def checking_react(self, post):
#         visitor = self.context['request'].user
#         if visitor in post.likes.all():
#             return "fas fa-thumbs-up react"

#         elif visitor in post.love.all():
#             return "fas fa-heart react"

#         elif visitor in post.haha.all():
#             return "fas fa-smile react"

#         elif visitor in post.sad.all():
#             return "fas fa-frown react"

#         elif visitor in post.wow.all():
#             return "fas fa-surprise react"

#         elif visitor in post.angry.all():
#             return "fas fa-angry react"

#         else:
#             return "far fa-thumbs-up react"

#     def checking_share(self, post):
#         visitor = self.context['request'].user
#         shared = Post.objects.filter(share=post, author=visitor)
#         if shared:
#             return "fas fa-share"
#         else:
#             return "far fa-share"



#     class Meta:
#         model = Post
#         fields = ('id', 'author', 'share', 'checking_per', 'checking_reactions', 'checking_shares', 'page', 'group', 'files', 'content', 'ReactsCounter', 'SharesCounter', 'CommentsCounter', 'DatePublished')
