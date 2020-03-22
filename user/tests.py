from django.test import TestCase
from django.test import TestCase, Client, RequestFactory
from .views import signup
from .forms import SignUpForm
from user.models import User, Profile
from projects.models import ProjectCategory
from django.contrib.messages.storage.fallback import FallbackStorage



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

    # def test_signup_password_max_value(self):
    #     createdUsers = User.objects.all()
    #     self.assertEqual(len(createdUsers), 0)
    #     # len(bollerogbrus) = 14
    #     passwordTestValue = "Bollerogbruss1_"
    #     data = createSignupContent(["password1", "password2"], [passwordTestValue, passwordTestValue])
    #     request = self.getSignupRequest(data)
    #     response = signup(request)
    #     createdUsers = User.objects.all()

    #     self.assertEqual(len(createdUsers), 1)
    #     self.assertEqual(302, response.status_code)
    #     User.objects.all().delete()

    # def test_signup_password_too_long(self):
    #     createdUsers = User.objects.all()
    #     self.assertEqual(len(createdUsers), 0)

    #     passwordTestValue = "TenChars12"*2000 + "a"
    #     data = createSignupContent(["password1", "password2"], [passwordTestValue, passwordTestValue])
    #     request = self.getSignupRequest(data)
    #     response = signup(request)
    #     createdUsers = User.objects.all()

    #     self.assertEqual(len(createdUsers), 0)
    #     self.assertEqual(200, response.status_code)
    #     User.objects.all().delete()


# # 
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
