from django.test import TestCase
from django.test import TestCase, Client, RequestFactory
from .views import signup, update_profile
from .forms import SignUpForm
from user.models import User, Profile
from home.views import home
from projects.models import ProjectCategory
from django.contrib.messages.storage.fallback import FallbackStorage
from allpairspy import AllPairs
import xlsxwriter
import unittest




one50Chars = 'a'*150
thirtyChars = 'a'*30
fifteenChars = 'a'*15
fiftyChars = 'a'*50
fiftyOneChars = 'a'*51
twoThousandChars = 'a'*2000
twoThousandOneChars = 'a'*2001
legalPassword = 'Bollerogbrus1_'
legalCategory = 1
legalEmail = 'test@hotmail.com'
legalFiftyCharFieldValue = 'a'*25
legalThirtyCharFieldValue = 'a'*15


def create_signup_content(field_to_test, value_for_field):
    signup_form_data = {
    'username': thirtyChars,
    'first_name': thirtyChars,
    'last_name': thirtyChars,
    'email': legalEmail,
    'email_confirmation': legalEmail,
    'company': legalThirtyCharFieldValue,
    'phone_number': legalFiftyCharFieldValue,
    'country': legalFiftyCharFieldValue,
    'password1': legalPassword,
    'password2': legalPassword,
    'state': legalFiftyCharFieldValue,
    'city': legalFiftyCharFieldValue,
    'postal_code': legalFiftyCharFieldValue,
    'street_address': legalFiftyCharFieldValue,
    'categories': legalCategory,
    'description': "testDesc",
    }
    
    if (type(field_to_test) == type([])):
        for i in range(len(field_to_test)):
            signup_form_data[field_to_test[i]] = value_for_field[i]
    elif (type(field_to_test) == type("")):
        signup_form_data[field_to_test] = value_for_field
    return signup_form_data


class SignupUsernameTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_username_too_short(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        username_test_value = ""
        data = create_signup_content("username", username_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_username_and_first_name(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        username_test_value = ""
        firstname_test_value = ""
        data = create_signup_content(["username", "first_name"], [username_test_value, firstname_test_value])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_username_minimum_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        username_test_value = "a"
        data = create_signup_content("username", username_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_username_just_above_min_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        username_test_value = "a"*2
        data = create_signup_content("username", username_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_username_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        username_test_value = "a"*15
        data = create_signup_content("username", username_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_username_just_below_max_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        username_value = "a"*149
        data = create_signup_content("username", username_value)

        request = self.get_signup_request(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 1)
        User.objects.all().delete()

    def test_signup_username_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        username_test_value = "a"*150
        data = create_signup_content("username", username_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_username_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        username_test_value = "a"*151
        data = create_signup_content("username", username_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()


class SignupFirstnameTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_firstname_too_short(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        firstname_test_value = ""
        data = create_signup_content("first_name", firstname_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_firstname_minimum_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        firstname_test_value = "a"
        data = create_signup_content("first_name", firstname_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_firstname_just_above_min_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        firstname_test_value = "a"*2
        data = create_signup_content("firstname", firstname_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_firstname_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        firstname_test_value = "a"*15
        data = create_signup_content("first_name", firstname_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_firstname_just_below_max_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        firstname_value = "a"*29
        data = create_signup_content("firstname", firstname_value)

        request = self.get_signup_request(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 1)
        User.objects.all().delete()

    def test_signup_firstname_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        firstname_test_value = "a"*30
        data = create_signup_content("first_name", firstname_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_firstname_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        firstname_test_value = "a"*31
        data = create_signup_content("first_name", firstname_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupLastnameTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_lastname_too_short(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        lastname_test_value = ""
        data = create_signup_content("last_name", lastname_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_lastname_minimum_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        lastname_test_value = "a"
        data = create_signup_content("lastname", lastname_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_lastname_just_above_min_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        lastname_test_value = "a"*2
        data = create_signup_content("lastname", lastname_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_lastname_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        lastname_test_value = "a"*15
        data = create_signup_content("last_name", lastname_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_lastname_just_below_max_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        lastname_value = "a"*29
        data = create_signup_content("lastname", lastname_value)

        request = self.get_signup_request(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 1)
        User.objects.all().delete()

    def test_signup_lastname_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        lastname_test_value = "a"*30
        data = create_signup_content("last_name", lastname_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_lastname_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        lastname_test_value = "a"*31
        data = create_signup_content("last_name", lastname_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupCategoriesTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_categories_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        categories_test_value = 1
        data = create_signup_content("categories", categories_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_categories_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        categories_test_value = 1
        data = create_signup_content("categories", categories_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_categories_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        categories_test_value = 2
        data = create_signup_content("categories", categories_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupCompanyTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_company_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        company_test_value = "a"*15
        data = create_signup_content("company", company_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_company_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        company_test_value = "a"*30
        data = create_signup_content("company", company_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_company_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        company_test_value = "a"*31
        data = create_signup_content("company", company_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupPhoneNumberTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_phone_number_too_short(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        phone_number_test_value = ""
        data = create_signup_content("phone_number", phone_number_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_phone_number_minimum_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        phone_number_test_value = "a"
        data = create_signup_content("phone_number", phone_number_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_phone_number_just_above_min_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        phone_number_test_value = "a"*2
        data = create_signup_content("phone_number", phone_number_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_phone_number_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        phone_number_test_value = "a"*15
        data = create_signup_content("phone_number", phone_number_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_phone_number_just_below_max_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        phone_number_value = "a"*49
        data = create_signup_content("phone_number", phone_number_value)

        request = self.get_signup_request(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 1)
        User.objects.all().delete()

    def test_signup_phone_number_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        phone_number_test_value = "a"*50
        data = create_signup_content("phone_number", phone_number_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_phone_number_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        phone_number_test_value = "a"*51
        data = create_signup_content("phone_number", phone_number_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupCountryTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_country_too_short(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        country_test_value = ""
        data = create_signup_content("country", country_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_country_minimum_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        country_test_value = "a"
        data = create_signup_content("country", country_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_country_just_above_min_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        country_test_value = "a"*2
        data = create_signup_content("country", country_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_country_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        country_test_value = "a"*15
        data = create_signup_content("country", country_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_country_just_below_max_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        country_value = "a"*49
        data = create_signup_content("country", country_value)

        request = self.get_signup_request(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 1)
        User.objects.all().delete()

    def test_signup_country_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        country_test_value = "a"*50
        data = create_signup_content("country", country_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_country_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        country_test_value = "a"*51
        data = create_signup_content("country", country_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupStateTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_state_too_short(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        state_test_value = ""
        data = create_signup_content("state", state_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_state_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        state_test_value = "a"*15
        data = create_signup_content("state", state_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_state_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        state_test_value = "a"*50
        data = create_signup_content("state", state_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_state_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        state_test_value = "a"*51
        data = create_signup_content("state", state_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupCityTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_city_too_short(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        city_test_value = ""
        data = create_signup_content("city", city_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_city_minimum_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        city_test_value = "a"
        data = create_signup_content("city", city_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_city_just_above_min_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        city_test_value = "a"*2
        data = create_signup_content("city", city_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_city_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        city_test_value = "a"*15
        data = create_signup_content("city", city_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_city_just_below_max_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        city_value = "a"*49
        data = create_signup_content("city", city_value)

        request = self.get_signup_request(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 1)
        User.objects.all().delete()

    def test_signup_city_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        city_test_value = "a"*50
        data = create_signup_content("city", city_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_city_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        city_test_value = "a"*51
        data = create_signup_content("city", city_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupPostalCodeTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_postal_code_too_short(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        postal_code_test_value = ""
        data = create_signup_content("postal_code", postal_code_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_postal_code_minimum_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        postal_code_test_value = "a"
        data = create_signup_content("postal_code", postal_code_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_postal_code_just_above_min_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        postal_code_test_value = "a"*2
        data = create_signup_content("postal_code", postal_code_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_postal_code_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        postal_code_test_value = "a"*15
        data = create_signup_content("postal_code", postal_code_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_postal_code_just_below_max_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        postal_code_value = "a"*49
        data = create_signup_content("postal_code", postal_code_value)

        request = self.get_signup_request(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 1)
        User.objects.all().delete()

    def test_signup_postal_code_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        postal_code_test_value = "a"*50
        data = create_signup_content("postal_code", postal_code_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_postal_code_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        postal_code_test_value = "a"*51
        data = create_signup_content("postal_code", postal_code_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupStreetAddressTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_street_address_too_short(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        street_address_test_value = ""
        data = create_signup_content("street_address", street_address_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_street_address_minimum_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        street_address_test_value = "a"
        data = create_signup_content("street_address", street_address_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_street_address_just_above_min_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        street_address_test_value = "a"*2
        data = create_signup_content("street_address", street_address_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_street_address_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        street_address_test_value = "a"*15
        data = create_signup_content("street_address", street_address_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_street_address_just_below_max_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        street_address_value = "a"*49
        data = create_signup_content("street_address", street_address_value)

        request = self.get_signup_request(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 1)
        User.objects.all().delete()

    def test_signup_street_address_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        street_address_test_value = "a"*50
        data = create_signup_content("street_address", street_address_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_street_address_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        street_address_test_value = "a"*51
        data = create_signup_content("street_address", street_address_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupPasswordTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_password_too_short(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        password_test_value = ""
        data = create_signup_content(["password1", "password2"], [password_test_value, password_test_value])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_password_minimum_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        password_test_value = "Stringtw2"
        data = create_signup_content(["password1", "password2"], [password_test_value, password_test_value])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_password_just_above_min_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        password_test_value = "Stringtw2F"
        data = create_signup_content(["password1", "password2"], [password_test_value, password_test_value])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_password_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        password_test_value = "Bollerrogbrus1_"
        data = create_signup_content(["password1", "password2"], [password_test_value, password_test_value])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_password_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        password_test_value = "Bollerogbruss1_" # length is 14
        data = create_signup_content(["password1", "password2"], [password_test_value, password_test_value])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()
    
    @unittest.skip("Should not accept 200 000 long password")
    def test_signup_password_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        password_test_value = "TenChars12"*20000 + "a" # No upperlimit to password length
        data = create_signup_content(["password1", "password2"], [password_test_value, password_test_value])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupEmailTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_email_too_short(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        email_test_value = ""
        data = create_signup_content(["email", "email_confirmation"], [email_test_value, email_test_value])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_email_minimum_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        email_test_value = "a@a.no"
        data = create_signup_content(["email", "email_confirmation"], [email_test_value, email_test_value])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_email_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        email_test_value = "lovlig@hotmail.com"
        data = create_signup_content(["email", "email_confirmation"], [email_test_value, email_test_value])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_email_just_below_max_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        email_test_value = "a"*241 + "@hotmail.com"
        data = create_signup_content(["email", "email_confirmation"], [email_test_value, email_test_value])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_email_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        email_test_value = "a"*242 + "@hotmail.com"
        data = create_signup_content(["email", "email_confirmation"], [email_test_value, email_test_value])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_email_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        email_test_value = "a"*243 + "@hotmail.com"
        data = create_signup_content(["email", "email_confirmation"], [email_test_value, email_test_value])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class TwoWayDomainTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    @unittest.skip("Creates excel sheet for manual testing")
    def test_two_way_domain(self):
        """
        This method uses the framework allpairspy (https://pypi.org/project/allpairspy/) which
        "produces a good enough dataset" of 2-way combinations. This drasticly decreases the 
        number of a brute force search of runtime O(n^4) to O(m). 

        This test is however a manual test to discover false positives and false negatives, and
        does not automaticly discover these. The 2-way domain test does not consider boundry test 
        since this is done in a different test. We need to go through the test output to see if there
        are anomalies in the output. To do this, we create an excel file with a negatives sheet
        and a positives sheet. During exercise 2 we found the following:
        False Positives:
            *  Success with email = nonunique@email.com and email_confirmation = unique@email.com.
            Should be the same email and email_confirmation variable.
            *  Success with first_name = ? and last_name = !.
            Should only be allowed to use alphabetic characters in these fields.
            *  Success with phone_number = nonunique@email.com and postal_code = nonunique@email.com.
            Should only be allowed to have numeric characters in these fields.
            *  Success with street_address = nonunique@email.com and city = nonunique@email.com.
            Should only be allowed to use alphabetic characters in these fields.
        False Negatives:
            *  Error with categories = 3 and username = 3.
            This is allowed as category = 3 means Garderning selected and username can be a number
            *  Error with categories = 2 and email_confirmation 
        """
        parameters = [
            [
                "", " ", "!", "?", "@", 
                "unique_variable", 
                'nonunique_variable', 
                'nonunique_variable', 
                'unique@email.com', 
                'nonunique@email.com',
                'nonunique@email.com',
                'nonunique@email.com',
                1, # Cleaning
                2, # Painting
                3, # Gardening
                4, # Carpentry
                "QWErty123"


            ],
            [
                "", " ", "!", "?", "@", 
                "unique_variable", 
                'nonunique_variable', 
                'nonunique_variable', 
                'unique@email.com', 
                'nonunique@email.com', 
                'nonunique@email.com',
                'nonunique@email.com',
                1, # Cleaning
                2, # Painting
                3, # Gardening
                4, # Carpentry
                "QWErty123"

            ],
            [
                'username',
                'first_name', 
                'last_name', 
                'email', 
                'email_confirmation', 
                'company', 
                'phone_number', 
                'country', 
                'password1', 
                'password2', 
                'state', 
                'city', 
                'postal_code', 
                'street_address', 
                'categories', 
                'description' 
            ],
            [
                'username',
                'first_name', 
                'last_name', 
                'email', 
                'email_confirmation', 
                'company', 
                'phone_number', 
                'country', 
                'password1', 
                'password2', 
                'state', 
                'city', 
                'postal_code', 
                'street_address', 
                'categories', 
                'description' 
            ]
        ]
        parameters = AllPairs(parameters)
        j = 1
        i = 1
        
        # Write to excel sheet
        workbook = xlsxwriter.Workbook("2-way-domain.xlsx")
        negatives = workbook.add_worksheet()
        negatives.write('C1', "first variable")
        negatives.write('D1', "second variable")
        negatives.write('A1', "first input field")
        negatives.write('B1', "second input field")

        positives = workbook.add_worksheet()
        positives.write('C1', "first variable")
        positives.write('D1', "second variable")
        positives.write('A1', "first input field")
        positives.write('B1', "second input field")
        
        for first_variable, second_variable, input_field_1, input_field_2 in parameters:   
            created_users = User.objects.all()
            self.assertEqual(len(created_users), 0)
            data = create_signup_content([input_field_1, input_field_2], [first_variable, second_variable])
            request = self.get_signup_request(data)
            response = signup(request)
            created_users = User.objects.all()
            if len(created_users) == 0:
                i += 1
                negatives.write('C'+str(i), first_variable)
                negatives.write('D'+str(i), second_variable)
                negatives.write('A'+str(i), input_field_1)
                negatives.write('B'+str(i), input_field_2)
                
            else:
                j += 1
                positives.write('C'+str(j), first_variable)
                positives.write('D'+str(j), second_variable)
                positives.write('A'+str(j), input_field_1)
                positives.write('B'+str(j), input_field_2)
            User.objects.all().delete()
        print(f'{j+i-2} number of possible combinations')
        print(f'There were {i-1} number of invalid cases')
        workbook.close()
    
    def test_two_way_domain_special_cases_password_1(self):
        input_field_1 = "password1"
        input_field_2 = "password2"
        first_variable = "WickyWick123"
        second_variable = "WickyWick123"
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        data = create_signup_content([input_field_1, input_field_2], [first_variable, second_variable])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_two_way_domain_special_cases_password_2(self):
        input_field_1 = "password1"
        input_field_2 = "password2"
        first_variable = "WickyWick123"
        second_variable = "WickyWick133" # should fail
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        data = create_signup_content([input_field_1, input_field_2], [first_variable, second_variable])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()


    def test_two_way_domain_special_cases_email_1(self):
        input_field_1 = "email"
        input_field_2 = "email_confirmation"
        first_variable = "a@mail.com"
        second_variable = "a@mail.com" 
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        data = create_signup_content([input_field_1, input_field_2], [first_variable, second_variable])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    @unittest.skip("Should not accept different mail in email_confirmation")
    def test_two_way_domain_special_cases_email_2(self):
        input_field_1 = "email"
        input_field_2 = "email_confirmation"
        first_variable = "a@mail.com"
        second_variable = "b@mail.com" # should fail
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        data = create_signup_content([input_field_1, input_field_2], [first_variable, second_variable])
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0) 
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

class SignupDescriptionTestSuite(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.category = ProjectCategory.objects.create(name="Painting")

    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_description_minimum_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        description_test_value = ""
        data = create_signup_content("description", description_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_description_just_above_min_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        description_test_value = "a"*1
        data = create_signup_content("description", description_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_description_legal_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        User.objects.all().delete()
        
        description_test_value = "a"*600
        data = create_signup_content("description", description_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

    def test_signup_description_just_below_max_legal_length(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        description_value = "a"*1999
        data = create_signup_content("description", description_value)

        request = self.get_signup_request(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 1)
        User.objects.all().delete()

    def test_signup_description_max_value(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)
        
        description_test_value = "a"*2000
        data = create_signup_content("description", description_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

    def test_signup_description_too_long(self):
        created_users = User.objects.all()
        self.assertEqual(len(created_users), 0)

        description_test_value = "a"*2001
        data = create_signup_content("description", description_test_value)
        request = self.get_signup_request(data)
        response = signup(request)
        created_users = User.objects.all()

        self.assertEqual(len(created_users), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class DescriptionBannerShowingCorrectlyTestSuite(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.category = ProjectCategory.objects.create(name="Painting")

    
    def get_signup_request(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def getHomeRequest(self, user):
        request = self.factory.get('/home')
        request.user = user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_banner_should_not_show_when_description_is_set(self):
        existing_users = User.objects.all()
        self.assertEqual(len(existing_users), 0)
        
        description_value = "This is not an empty description"
        data = create_signup_content("description", description_value)
        request = self.get_signup_request(data)
        response = signup(request)

        created_users = Profile.objects.all()
        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        self.assertEqual(created_users.first().description, description_value)

        self.client.login(username=thirtyChars, password=legalPassword)
        resp = self.getHomeRequest(created_users.first().user)
        home_screen_response = home(resp)
        alert_showing = "alert" in home_screen_response.content.decode("utf-8")
        self.assertFalse(alert_showing)

    def test_banner_should_show_when_description_is_not_set(self):
        existing_users = User.objects.all()
        self.assertEqual(len(existing_users), 0)
        
        description_value = ""
        data = create_signup_content("description", description_value)
        request = self.get_signup_request(data)
        response = signup(request)

        created_users = Profile.objects.all()
        self.assertEqual(len(created_users), 1)
        self.assertEqual(302, response.status_code)
        self.assertEqual(created_users.first().description, description_value)

        self.client.login(username=thirtyChars, password=legalPassword)
        resp = self.getHomeRequest(created_users.first().user)
        home_screen_response = home(resp)
        alert_showing = "alert" in home_screen_response.content.decode("utf-8")
        self.assertTrue(alert_showing)

class EditDescriptionTestSuite(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
    
    def getUpdateProfileRequest(self, data, user):
        request = self.factory.post('/user/'+str(self.user.username), data)
        request.user = user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        return request

    def test_description_should_update(self):
        description_before = "This is not an empty description"
        description_after = "This is an entirely new description"
        self.user = User.objects.create_user(
            username='chrsitopher',
            first_name='Christopher',
            last_name='Columbus',
            email='criscol@atlanticocean.com',
        )
        self.user_profile = Profile.objects.get(user=self.user)
        self.user_profile.description = description_before
        data = {
            "description": description_after,
            "email_notifications": True,
        }
        request = self.getUpdateProfileRequest(data, self.user)
        self.assertEqual(self.user_profile.description, description_before)
        response = update_profile(request)
        self.assertEqual(response.status_code, 302)
        profile_after = Profile.objects.all().first()
        self.assertEqual(profile_after.description, description_after)

class EditEmailNotificationPreferencesTestSuite(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='chrsitopher',
            first_name='Christopher',
            last_name='Columbus',
            email='criscol@atlanticocean.com',
        )
        self.user_profile = Profile.objects.get(user=self.user)
        self.user_profile.description = "This is not an empty description"
    
    def getUpdateProfileRequest(self, data, user):
        request = self.factory.post('/user/'+str(self.user.username), data)
        request.user = user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        return request

    def test_email_preferences_should_update(self):
        self.assertTrue(self.user_profile.email_notifications)

        data = {
            "description": "This is not an empty description",
            "email_notifications": False,
        }
        request = self.getUpdateProfileRequest(data, self.user)

        response = update_profile(request)
        profile_after = Profile.objects.all().first()

        self.assertEqual(response.status_code, 302)
        self.assertFalse(profile_after.email_notifications)

        data = {
            "description": "This is not an empty description",
            "email_notifications": True,
        }
        request = self.getUpdateProfileRequest(data, self.user)

        response = update_profile(request)
        profile_after = Profile.objects.all().first()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(profile_after.email_notifications)
