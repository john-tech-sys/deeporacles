from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from affiliate.models import AffiliateLink
from home.models import Post


class Message(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    user_input = models.TextField()  # User input
    message = models.TextField()  # Thread of messages
    in_app_responses = models.ManyToManyField(Post, blank=True, related_name="in_app_response")  # Messages based on the posts within the app, max 4
    affiliate_links = models.ManyToManyField(AffiliateLink,  blank=True, related_name="affiliates")
    
@receiver(post_save, sender=Message)
def create_conversation_on_message_creation(sender, instance, created, **kwargs):
    if created:
        Conversation.objects.create(user=instance.user, title=instance.user_input[:50])


class Conversation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    messages = models.ManyToManyField(Message, blank=True, related_name="messages")  # Thread of messages
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # Add other fields as needed
    
    def save(self, *args, **kwargs):
        if not self.title:
            first_message = self.messages.order_by('id').first()  # Get the first message based on the id
            if first_message:
                try:
                    # Shorten the first response from AI to a maximum of 50 words
                    short_response = ' '.join(first_message.ai_response.split()[:50])

                    # Set the title based on the short response
                    self.title = short_response

                    # Generate slug from title
                    self.slug = slugify(self.title)

                except Exception as e:
                    # Handle errors during title generation or slug creation
                    print(f"Error: {e}")
                    self.title = "Untitled Conversation"
                    self.slug = ""

            else:
                # Handle case where no messages are available
                self.title = "No Messages"
                self.slug = ""
                
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title[:50]  # Return the first 50 characters of the title

