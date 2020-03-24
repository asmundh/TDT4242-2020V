from django.test import TestCase
from django.test import TestCase, Client, RequestFactory
from .views import signup
from .forms import SignUpForm
from user.models import User, Profile
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


def createSignupContent(fieldToTest, valueForField):
    signupFormData = {
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
    'description': 'testDesc',
    }
    
    if (type(fieldToTest) == type([])):
        for i in range(len(fieldToTest)):
            signupFormData[fieldToTest[i]] = valueForField[i]
    elif (type(fieldToTest) == type("")):
        signupFormData[fieldToTest] = valueForField
    return signupFormData


class SignupUsernameTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_username_too_short(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        usernameTestValue = ""
        data = createSignupContent("username", usernameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_username_and_first_name(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        usernameTestValue = ""
        firstNameTestValue = ""
        data = createSignupContent(["username", "first_name"], [usernameTestValue, firstNameTestValue])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_username_minimum_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        usernameTestValue = "a"
        data = createSignupContent("username", usernameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_username_just_above_min_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        usernameTestValue = "a"*2
        data = createSignupContent("username", usernameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_username_legal_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        usernameTestValue = "a"*15
        data = createSignupContent("username", usernameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_username_just_below_max_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        usernameValue = "a"*149
        data = createSignupContent("username", usernameValue)

        request = self.getSignupRequest(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 1)
        User.objects.all().delete()

    def test_signup_username_max_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        usernameTestValue = "a"*150
        data = createSignupContent("username", usernameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_username_too_long(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        usernameTestValue = "a"*151
        data = createSignupContent("username", usernameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()


class SignupFirstnameTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_firstname_too_short(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        firstnameTestValue = ""
        data = createSignupContent("first_name", firstnameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_firstname_minimum_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        firstnameTestValue = "a"
        data = createSignupContent("first_name", firstnameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_firstname_just_above_min_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        firstnameTestValue = "a"*2
        data = createSignupContent("firstname", firstnameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_firstname_legal_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        firstnameTestValue = "a"*15
        data = createSignupContent("first_name", firstnameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_firstname_just_below_max_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        firstnameValue = "a"*29
        data = createSignupContent("firstname", firstnameValue)

        request = self.getSignupRequest(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 1)
        User.objects.all().delete()

    def test_signup_firstname_max_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        firstnameTestValue = "a"*30
        data = createSignupContent("first_name", firstnameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_firstname_too_long(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        firstnameTestValue = "a"*31
        data = createSignupContent("first_name", firstnameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupLastnameTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_lastname_too_short(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        lastnameTestValue = ""
        data = createSignupContent("last_name", lastnameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_lastname_minimum_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        lastnameTestValue = "a"
        data = createSignupContent("lastname", lastnameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_lastname_just_above_min_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        lastnameTestValue = "a"*2
        data = createSignupContent("lastname", lastnameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_lastname_legal_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        lastnameTestValue = "a"*15
        data = createSignupContent("last_name", lastnameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_lastname_just_below_max_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        lastnameValue = "a"*29
        data = createSignupContent("lastname", lastnameValue)

        request = self.getSignupRequest(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 1)
        User.objects.all().delete()

    def test_signup_lastname_max_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        lastnameTestValue = "a"*30
        data = createSignupContent("last_name", lastnameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_lastname_too_long(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        lastnameTestValue = "a"*31
        data = createSignupContent("last_name", lastnameTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupCategoriesTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_categories_legal_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        categoriesTestValue = 1
        data = createSignupContent("categories", categoriesTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_categories_max_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        categoriesTestValue = 1
        data = createSignupContent("categories", categoriesTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_categories_too_long(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        categoriesTestValue = 2
        data = createSignupContent("categories", categoriesTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()


class SignupCompanyTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_company_legal_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        companyTestValue = "a"*15
        data = createSignupContent("company", companyTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_company_max_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        companyTestValue = "a"*30
        data = createSignupContent("company", companyTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_company_too_long(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        companyTestValue = "a"*31
        data = createSignupContent("company", companyTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupPhoneNumberTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_phone_number_too_short(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        phone_numberTestValue = ""
        data = createSignupContent("phone_number", phone_numberTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_phone_number_minimum_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        phone_numberTestValue = "a"
        data = createSignupContent("phone_number", phone_numberTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_phone_number_just_above_min_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        phone_numberTestValue = "a"*2
        data = createSignupContent("phone_number", phone_numberTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_phone_number_legal_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        phone_numberTestValue = "a"*15
        data = createSignupContent("phone_number", phone_numberTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_phone_number_just_below_max_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        phone_numberValue = "a"*49
        data = createSignupContent("phone_number", phone_numberValue)

        request = self.getSignupRequest(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 1)
        User.objects.all().delete()

    def test_signup_phone_number_max_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        phone_numberTestValue = "a"*50
        data = createSignupContent("phone_number", phone_numberTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_phone_number_too_long(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        phone_numberTestValue = "a"*51
        data = createSignupContent("phone_number", phone_numberTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupCountryTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_country_too_short(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        countryTestValue = ""
        data = createSignupContent("country", countryTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_country_minimum_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        countryTestValue = "a"
        data = createSignupContent("country", countryTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_country_just_above_min_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        countryTestValue = "a"*2
        data = createSignupContent("country", countryTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_country_legal_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        countryTestValue = "a"*15
        data = createSignupContent("country", countryTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_country_just_below_max_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        countryValue = "a"*49
        data = createSignupContent("country", countryValue)

        request = self.getSignupRequest(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 1)
        User.objects.all().delete()

    def test_signup_country_max_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        countryTestValue = "a"*50
        data = createSignupContent("country", countryTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_country_too_long(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        countryTestValue = "a"*51
        data = createSignupContent("country", countryTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupStateTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_state_too_short(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        stateTestValue = ""
        data = createSignupContent("state", stateTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_state_legal_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        stateTestValue = "a"*15
        data = createSignupContent("state", stateTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_state_max_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        stateTestValue = "a"*50
        data = createSignupContent("state", stateTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_state_too_long(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        stateTestValue = "a"*51
        data = createSignupContent("state", stateTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()


class SignupCityTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_city_too_short(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        cityTestValue = ""
        data = createSignupContent("city", cityTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_city_minimum_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        cityTestValue = "a"
        data = createSignupContent("city", cityTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_city_just_above_min_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        cityTestValue = "a"*2
        data = createSignupContent("city", cityTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_city_legal_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        cityTestValue = "a"*15
        data = createSignupContent("city", cityTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_city_just_below_max_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        cityValue = "a"*49
        data = createSignupContent("city", cityValue)

        request = self.getSignupRequest(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 1)
        User.objects.all().delete()

    def test_signup_city_max_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        cityTestValue = "a"*50
        data = createSignupContent("city", cityTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_city_too_long(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        cityTestValue = "a"*51
        data = createSignupContent("city", cityTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()


class SignupPostalCodeTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_postal_code_too_short(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        postal_codeTestValue = ""
        data = createSignupContent("postal_code", postal_codeTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_postal_code_minimum_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        postal_codeTestValue = "a"
        data = createSignupContent("postal_code", postal_codeTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_postal_code_just_above_min_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        postal_codeTestValue = "a"*2
        data = createSignupContent("postal_code", postal_codeTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_postal_code_legal_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        postal_codeTestValue = "a"*15
        data = createSignupContent("postal_code", postal_codeTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_postal_code_just_below_max_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        postal_codeValue = "a"*49
        data = createSignupContent("postal_code", postal_codeValue)

        request = self.getSignupRequest(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 1)
        User.objects.all().delete()

    def test_signup_postal_code_max_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        postal_codeTestValue = "a"*50
        data = createSignupContent("postal_code", postal_codeTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_postal_code_too_long(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        postal_codeTestValue = "a"*51
        data = createSignupContent("postal_code", postal_codeTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()


class SignupStreetAddressTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_street_address_too_short(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        street_addressTestValue = ""
        data = createSignupContent("street_address", street_addressTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_street_address_minimum_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        street_addressTestValue = "a"
        data = createSignupContent("street_address", street_addressTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_street_address_just_above_min_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        street_addressTestValue = "a"*2
        data = createSignupContent("street_address", street_addressTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_street_address_legal_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        street_addressTestValue = "a"*15
        data = createSignupContent("street_address", street_addressTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_street_address_just_below_max_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        street_addressValue = "a"*49
        data = createSignupContent("street_address", street_addressValue)

        request = self.getSignupRequest(data)
        
        response = signup(request)
        self.assertEqual(302, response.status_code)
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 1)
        User.objects.all().delete()

    def test_signup_street_address_max_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        street_addressTestValue = "a"*50
        data = createSignupContent("street_address", street_addressTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_street_address_too_long(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        street_addressTestValue = "a"*51
        data = createSignupContent("street_address", street_addressTestValue)
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupPasswordTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_password_too_short(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        passwordTestValue = ""
        data = createSignupContent(["password1", "password2"], [passwordTestValue, passwordTestValue])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_password_minimum_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        passwordTestValue = "Stringtw2"
        data = createSignupContent(["password1", "password2"], [passwordTestValue, passwordTestValue])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_password_just_above_min_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        passwordTestValue = "Stringtw2F"
        data = createSignupContent(["password1", "password2"], [passwordTestValue, passwordTestValue])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_password_legal_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        passwordTestValue = "Bollerrogbrus1_"
        data = createSignupContent(["password1", "password2"], [passwordTestValue, passwordTestValue])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_password_max_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        # len(bollerogbrus) = 14
        passwordTestValue = "Bollerogbruss1_"
        data = createSignupContent(["password1", "password2"], [passwordTestValue, passwordTestValue])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()
    
    @unittest.skip("Should not accept 200 000 long password")
    def test_signup_password_too_long(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        passwordTestValue = "TenChars12"*20000 + "a" # No upperlimit to password length
        data = createSignupContent(["password1", "password2"], [passwordTestValue, passwordTestValue])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

class SignupEmailTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
        request = self.factory.post('/signup', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_signup_email_too_short(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        emailTestValue = ""
        data = createSignupContent(["email", "email_confirmation"], [emailTestValue, emailTestValue])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()

    def test_signup_email_minimum_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        emailTestValue = "a@a.no"
        data = createSignupContent(["email", "email_confirmation"], [emailTestValue, emailTestValue])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_email_legal_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        emailTestValue = "lovlig@hotmail.com"
        data = createSignupContent(["email", "email_confirmation"], [emailTestValue, emailTestValue])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_email_just_below_max_legal_length(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        User.objects.all().delete()
        
        emailTestValue = "a"*241 + "@hotmail.com"
        data = createSignupContent(["email", "email_confirmation"], [emailTestValue, emailTestValue])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_email_max_value(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        
        emailTestValue = "a"*242 + "@hotmail.com"
        data = createSignupContent(["email", "email_confirmation"], [emailTestValue, emailTestValue])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_signup_email_too_long(self):
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)

        emailTestValue = "a"*243 + "@hotmail.com"
        data = createSignupContent(["email", "email_confirmation"], [emailTestValue, emailTestValue])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()

        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()


class TwoWayDomainTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(name="Painting")
    
    def getSignupRequest(self, data):
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
            createdUsers = User.objects.all()
            self.assertEqual(len(createdUsers), 0)
            data = createSignupContent([input_field_1, input_field_2], [first_variable, second_variable])
            request = self.getSignupRequest(data)
            response = signup(request)
            createdUsers = User.objects.all()
            if len(createdUsers) == 0:
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
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        data = createSignupContent([input_field_1, input_field_2], [first_variable, second_variable])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    def test_two_way_domain_special_cases_password_2(self):
        input_field_1 = "password1"
        input_field_2 = "password2"
        first_variable = "WickyWick123"
        second_variable = "WickyWick133" # should fail
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        data = createSignupContent([input_field_1, input_field_2], [first_variable, second_variable])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        self.assertEqual(200, response.status_code)
        User.objects.all().delete()


    def test_two_way_domain_special_cases_email_1(self):
        input_field_1 = "email"
        input_field_2 = "email_confirmation"
        first_variable = "a@mail.com"
        second_variable = "a@mail.com" 
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        data = createSignupContent([input_field_1, input_field_2], [first_variable, second_variable])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 1)
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()

    @unittest.skip("Should not accept different mail in email_confirmation")
    def test_two_way_domain_special_cases_email_2(self):
        input_field_1 = "email"
        input_field_2 = "email_confirmation"
        first_variable = "a@mail.com"
        second_variable = "b@mail.com" # should fail
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0)
        data = createSignupContent([input_field_1, input_field_2], [first_variable, second_variable])
        request = self.getSignupRequest(data)
        response = signup(request)
        createdUsers = User.objects.all()
        self.assertEqual(len(createdUsers), 0) 
        self.assertEqual(302, response.status_code)
        User.objects.all().delete()