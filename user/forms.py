from django import forms
from django.contrib.auth.models import User
from projects.models import ProjectCategory
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    company = forms.CharField(
        max_length=30, required=False, help_text='Here you can add your company.')

    email = forms.EmailField(
        max_length=254, help_text='Inform a valid email address.')
    email_confirmation = forms.EmailField(
        max_length=254, help_text='Enter the same email as before, for verification.')

    phone_number = forms.CharField(max_length=50)

    country = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    postal_code = forms.CharField(max_length=50)
    street_address = forms.CharField(max_length=50)
    description = forms.CharField(max_length=2000, required=False)
    categories = forms.ModelMultipleChoiceField(queryset=ProjectCategory.objects.all(
    ), help_text='Hold down "Control", or "Command" on a Mac, to select more than one.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'categories', 'company', 'email', 'email_confirmation',
                  'password1', 'password2', 'phone_number', 'country', 'state', 'city', 'postal_code', 'street_address', 'description')

# COPY PASTA


class UpdateProfile(forms.ModelForm):
    description = forms.CharField(max_length=2000, required=False)
    email_notifications = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('description', 'email_notifications')
