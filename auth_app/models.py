from django.db import models

# Create your models here.
# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    Extended user profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    # profile_picture = models.ImageField(
    #     upload_to='profile_pics/', 
    #     null=True, 
    #     blank=True, 
    #     default='default_profile.png'
    # )
    
    # # Social media links (optional)
    # linkedin_url = models.URLField(blank=True, null=True)
    # github_url = models.URLField(blank=True, null=True)
    
    # # Account settings
    # is_email_verified = models.BooleanField(default=False)
    # receives_newsletter = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a profile when a new user is created
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Automatically save the profile when the user is saved
    """
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
