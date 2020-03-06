from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

class UserReview(models.Model):
    givenRating = models.IntegerField(default=0)
    taskPerformed = models.ForeignKey("projects.Task", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.TextField(max_length=50, blank=True)
    phone_number = models.TextField(max_length=50, blank=True)
    country = models.TextField(max_length=50, blank=True)
    state = models.TextField(max_length=50, blank=True)
    city = models.TextField(max_length=50, blank=True)
    postal_code = models.TextField(max_length=50, blank=True)
    street_address = models.TextField(max_length=50, blank=True)
    categories = models.ManyToManyField('projects.ProjectCategory', related_name='competance_categories')
    user_reviews = models.ManyToManyField(UserReview, related_name='user_reviews')

    @property
    def get_average_rating(self):
        #             project.category =  get_object_or_404(ProjectCategory, id=request.POST.get('category_id'))
        project_ratings = get_object_or_404(Profile, id=request.POST.get('user_reviews'))
        return user_reviews.all().sum()
        # aggregate(average=models.Sum('given_rating'))['total']

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save() # Saves the user profile
