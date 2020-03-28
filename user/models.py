from django.contrib.auth.models import User
from django.db import models
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    company = models.TextField(max_length=50, blank=True)
    phone_number = models.TextField(max_length=50, blank=True)
    country = models.TextField(max_length=50, blank=True)
    state = models.TextField(max_length=50, blank=True)
    city = models.TextField(max_length=50, blank=True)
    postal_code = models.TextField(max_length=50, blank=True)
    street_address = models.TextField(max_length=50, blank=True)
    categories = models.ManyToManyField(
        'projects.ProjectCategory', related_name='competance_categories')
    description = models.TextField(max_length=2000, blank=True)
    email_notifications = models.BooleanField(default=True)

    @property
    def get_average_rating(self):
        queried_deliveries = apps.get_model(
            'projects.delivery').objects.filter(delivery_user=self)
        sum_of_ratings = 0
        if (queried_deliveries.count() > 0):
            for delivery in queried_deliveries:
                sum_of_ratings += delivery.delivery_rating
            return round(sum_of_ratings/queried_deliveries.count(), 1)
        else:
            return 0

    @property
    def get_rating_count(self):
        queried_deliveries = apps.get_model(
            'projects.delivery').objects.filter(delivery_user=self)
        return queried_deliveries.count()

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()  # Saves the user profile
