from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
import unittest
from projects.views import project_view, get_user_task_permissions
from .models import Project, Task, TaskFile, TaskOffer, Delivery, ProjectCategory, Team, TaskFileTeam, directory_path
from user.models import User, Profile
from django.urls import reverse
from .views import task_view
from .templatetags.project_extras import get_accepted_task_offer, check_taskoffers, get_project_participants, get_project_participants_string
from django.contrib.messages.storage.fallback import FallbackStorage

def create_make_offer_content(field_to_test, value_for_field):
    task_offer_form_data = {
    "title": "Legal title",
    "description": "Legal description",
    "price": "2000",
    "taskvalue": "1",
    "offer_submit": True,
    }
    task_offer_form_data[field_to_test] = value_for_field
    return task_offer_form_data


class GetUserTaskPermissionsTest(TestCase):
    def setUp(self):
        self.owner_user = User.objects.create_user(
            username='chrsitopher',
            first_name='Christopher',
            last_name='Columbus',
            email='criscol@atlanticocean.com'
        )
        self.owner_user.save()
        self.category = ProjectCategory.objects.create(name="Painting")
        self.category.save()
        self.owner_project = Project.objects.create(
            user=self.owner_user.profile,
            title='Test project',
            description='Description',
            category=self.category
        )
        self.owner_project.save()
        self.owner_task = Task.objects.create(
            project=self.owner_project,
            title='Task name',
            description='Task description'
        )
        self.owner_task.save()

    def test_get_user_task_permissions_owner(self):
        task_permissions = get_user_task_permissions(
            self.owner_user, self.owner_task)
        self.assertIs(task_permissions['write'], True)
        self.assertIs(task_permissions['read'], True)
        self.assertIs(task_permissions['modify'], True)
        self.assertIs(task_permissions['owner'], True)
        self.assertIs(task_permissions['upload'], True)

    def test_get_user_task_permissions_user_not_in_task(self):
        random_user = User.objects.create_user(
            username='tom',
            first_name='Tom',
            last_name='Sawyer',
            email='tomsaw@twain.com'
        )
        random_user.save()
        task_permissions = get_user_task_permissions(
            random_user, self.owner_task)
        self.assertIs(task_permissions['write'], False)
        self.assertIs(task_permissions['read'], False)
        self.assertIs(task_permissions['modify'], False)
        self.assertIs(task_permissions['owner'], False)
        self.assertIs(task_permissions['upload'], False)
        self.assertIs(task_permissions['view_task'], False)

    def test_get_user_task_permissions_project_manager(self):
        project_manager = User.objects.create_user(
            username='Jane',
            first_name='Jane',
            last_name='Doe',
            email='jandoe@anonymous.com'
        )
        project_manager.save()
        offer = TaskOffer.objects.create(
            task=self.owner_task,
            offerer=project_manager.profile,
            title="Offer title",
            price=1,
            description="Offer description",
            status=TaskOffer.ACCEPTED
        )
        offer.save()
        task_permissions = get_user_task_permissions(
            project_manager, self.owner_task)
        self.assertIs(task_permissions['write'], True)
        self.assertIs(task_permissions['read'], True)
        self.assertIs(task_permissions['modify'], True)
        self.assertIs(task_permissions['owner'], False)
        self.assertIs(task_permissions['upload'], True)

    def test_get_user_task_permissions_participant_with_write_permissions(self):
        project_manager = User.objects.create_user(
            username='sherlock',
            first_name='Sherlock',
            last_name='Holmes',
            email='shehol@mystery.com'
        )
        project_manager.save()
        offer = TaskOffer.objects.create(
            task=self.owner_task,
            offerer=project_manager.profile,
            title="Offer title",
            price=1,
            description="Offer description",
            status=TaskOffer.ACCEPTED
        )
        offer.save()
        project_participant = User.objects.create_user(
            username='gandalf',
            first_name='Gandalf',
            last_name='deGrey',
            email='gandeg@middleearth.com'
        )
        project_participant.save()
        self.owner_task.write.add(project_participant.profile)
        self.owner_project.save()
        task_permissions = get_user_task_permissions(
            project_participant, self.owner_task)
        self.assertIs(task_permissions['write'], True)
        self.assertIs(task_permissions['read'], False)
        self.assertIs(task_permissions['modify'], False)
        self.assertIs(task_permissions['owner'], False)
        self.assertIs(task_permissions['upload'], False)
        self.assertIs(task_permissions['view_task'], False)

    def test_get_user_task_permissions_participant_with_read_permissions(self):
        project_manager = User.objects.create_user(
            username='sherlock',
            first_name='Sherlock',
            last_name='Holmes',
            email='shehol@mystery.com'
        )
        project_manager.save()
        offer = TaskOffer.objects.create(
            task=self.owner_task,
            offerer=project_manager.profile,
            title="Offer title",
            price=1,
            description="Offer description",
            status=TaskOffer.ACCEPTED
        )
        offer.save()
        project_participant = User.objects.create_user(
            username='gandalf',
            first_name='Gandalf',
            last_name='deGrey',
            email='gandeg@middleearth.com'
        )
        project_participant.save()
        self.owner_task.read.add(project_participant.profile)
        self.owner_project.save()
        task_permissions = get_user_task_permissions(
            project_participant, self.owner_task)
        self.assertIs(task_permissions['write'], False)
        self.assertIs(task_permissions['read'], True)
        self.assertIs(task_permissions['modify'], False)
        self.assertIs(task_permissions['owner'], False)
        self.assertIs(task_permissions['upload'], False)
        self.assertIs(task_permissions['view_task'], False)

    def test_get_user_task_permissions_participant_with_modify_permissions(self):
        project_manager = User.objects.create_user(
            username='sherlock',
            first_name='Sherlock',
            last_name='Holmes',
            email='shehol@mystery.com'
        )
        project_manager.save()
        offer = TaskOffer.objects.create(
            task=self.owner_task,
            offerer=project_manager.profile,
            title="Offer title",
            price=1,
            description="Offer description",
            status=TaskOffer.ACCEPTED
        )
        offer.save()
        project_participant = User.objects.create_user(
            username='gandalf',
            first_name='Gandalf',
            last_name='deGrey',
            email='gandeg@middleearth.com'
        )
        project_participant.save()
        self.owner_task.modify.add(project_participant.profile)
        self.owner_project.save()
        task_permissions = get_user_task_permissions(
            project_participant, self.owner_task)
        self.assertIs(task_permissions['write'], False)
        self.assertIs(task_permissions['read'], False)
        self.assertIs(task_permissions['modify'], True)
        self.assertIs(task_permissions['owner'], False)
        self.assertIs(task_permissions['upload'], False)
        self.assertIs(task_permissions['view_task'], False)

    def test_get_user_task_permissions_participant_with_upload_permissions(self):
        project_manager = User.objects.create_user(
            username='sherlock',
            first_name='Sherlock',
            last_name='Holmes',
            email='shehol@mystery.com'
        )
        project_manager.save()
        offer = TaskOffer.objects.create(
            task=self.owner_task,
            offerer=project_manager.profile,
            title="Offer title",
            price=1,
            description="Offer description",
            status=TaskOffer.ACCEPTED
        )
        offer.save()
        project_participant = User.objects.create_user(
            username='gandalf',
            first_name='Gandalf',
            last_name='deGrey',
            email='gandeg@middleearth.com'
        )
        project_participant.save()
        team = Team.objects.create(
            name='Team',
            task=self.owner_task,
            write=True
        )
        team.members.add(project_participant.profile)
        team.save()
        task_permissions = get_user_task_permissions(
            project_participant, self.owner_task)
        self.assertIs(task_permissions['write'], False)
        self.assertIs(task_permissions['read'], False)
        self.assertIs(task_permissions['modify'], False)
        self.assertIs(task_permissions['owner'], False)
        self.assertIs(task_permissions['upload'], True)
        self.assertIs(task_permissions['view_task'], True)

    def test_get_user_task_permissions_participant_with_view_task_permissions(self):
        project_manager = User.objects.create_user(
            username='sherlock',
            first_name='Sherlock',
            last_name='Holmes',
            email='shehol@mystery.com'
        )
        project_manager.save()
        offer = TaskOffer.objects.create(
            task=self.owner_task,
            offerer=project_manager.profile,
            title="Offer title",
            price=1,
            description="Offer description",
            status=TaskOffer.ACCEPTED
        )
        offer.save()
        project_participant = User.objects.create_user(
            username='gandalf',
            first_name='Gandalf',
            last_name='deGrey',
            email='gandeg@middleearth.com'
        )
        project_participant.save()
        team = Team.objects.create(
            name='Team',
            task=self.owner_task,
            write=False
        )
        team.members.add(project_participant.profile)
        team.save()
        task_permissions = get_user_task_permissions(
            project_participant, self.owner_task)
        self.assertIs(task_permissions['write'], False)
        self.assertIs(task_permissions['read'], False)
        self.assertIs(task_permissions['modify'], False)
        self.assertIs(task_permissions['owner'], False)
        self.assertIs(task_permissions['upload'], False)
        self.assertIs(task_permissions['view_task'], True)

class ProjectViewTestSuite(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        project_category = ProjectCategory.objects.create(
            pk=1, name="Gardening")

        self.user_owner = User.objects.create_user(
            pk=1,
            username='Project_owner',
            email='proj_owner@gmail.com',
            password='HemmeligWooo213'
        )

        self.user_owner_profile = Profile.objects.get(user=self.user_owner)

        self.user_bidder = User.objects.create_user(
            username='Project_bidder',
            email='proj_bidder@gmail.com',
            password='HemmeligWooo213'
        )

        self.test_project = Project.objects.create(
            pk=1,
            user=self.user_owner_profile,
            title='Test Project',
            description='This is nothing more than a test. Stay calm.',
            category=project_category,
            status="o"
        )

        self.task_1 = Task.objects.create(
            pk=1,
            project=self.test_project,
            title='This task is purely for testing. I will not pay',
            description='^Same as above',
            budget=20
        )

    def test_project_view_offer_response(self):
        task_offer = TaskOffer.objects.create(
            pk=1,
            task=self.task_1,
            title='This offer is purely for testing. I will not actually complete the task',
            description='Same as above',
            price=20,
            offerer=self.user_bidder.profile
        )
        task_offer_id = task_offer.id

        self.client.login(username='Project_owner', password='HemmeligWooo213')
        response = self.client.post(f'/projects/{task_offer_id}/',
            {
                'status': 'a',
                'offer_response': True,
                'taskofferid': task_offer_id,
                'feedback': 'Bra saker'
            }
        )
        self.assertEqual(200, response.status_code)

    def test_project_view_status_change(self):
        request = self.factory.get('/projects/'+str(self.user_owner.id))
        request.user = self.user_owner
        response = project_view(request, self.test_project.id)
        self.assertEqual(200, response.status_code)

        post = self.factory.post(
            '/projects/'+str(self.user_owner.id),
            {
                'status_change': '',
                'status': 'i'
            }
        )
        post.user = self.user_owner
        response = project_view(post, self.test_project.id)
        self.assertEqual(response.status_code, 200)

    def test_project_view_offer_submit(self):
        offers = TaskOffer.objects.all()
        self.assertEqual(len(offers), 0)
        data = {
                'offer_submit': True,
                'title': 'This is purely a test offer. I have not actually done anything.',
                'description': 'Same as above.',
                'price': 20,
                'taskvalue': self.task_1.id
            }
        post = self.factory.post('/project/'+str(self.user_bidder.id), data)
        setattr(post, 'session', 'session')
        messages = FallbackStorage(post)
        setattr(post, '_messages', messages)
        post.user = self.user_bidder
        response = project_view(post, self.test_project.id)
        offers = TaskOffer.objects.all()
        self.assertEqual(len(offers), 1)
        self.assertEqual(200, response.status_code)
        TaskOffer.objects.all().delete()

class OutputCoverageTestSuite(TestCase):
    '''
    This test case will test all possible outputs related to sending a task offer. This encompasses:
    * TaskOffer response with status code "Pending", "Declined" and "Accepted".

    This means that we have 3 possible scenarios where we will first check the status of the project when 
    we have a pending task offer then we check the status after we accept the offer, and finally we check 
    the status after we decline an offer.

    Possible statuses in Task model:
    *  AWAITING_DELIVERY = 'ad'
    *  PENDING_ACCEPTANCE = 'pa'
    *  PENDING_PAYMENT = 'pp'
    *  PAYMENT_SENT = 'ps'
    *  DECLINED_DELIVERY = 'dd'

    Possible statuses in TaskOffer model:
    *  ACCEPTED = 'a'
    *  PENDING = 'p'
    *  DECLINED = 'd'
    '''
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Make the owner of the project
        self.owner_user = User.objects.create_user(
            username='luke',
            first_name='Luke',
            last_name='Skywalker',
            email='luksky@starwars.com',
        )
        self.owner_user.save()

        # Make a project and add the owner to it 
        # Be sure to add a category to it as well
        self.category = ProjectCategory.objects.create(name="Painting")
        self.category.save()
        self.owner_project = Project.objects.create(
            user=self.owner_user.profile,
            title='Test project',
            description='Description',
            category=self.category
        )
        self.owner_project.save()

        # create freelancer to give offer
        self.freelancer = User.objects.create_user(
            username='indiana',
            first_name='Indiana',
            last_name='Jones',
            email='indjon@dynamite.com'
        )
        self.freelancer.save()

        # lets create 3 tasks for the project
        self.project_task_1 = Task.objects.create(
            project=self.owner_project,
            title='Task 1 name',
            description='Task 1 description'
        )
        self.project_task_1.save()

        self.project_task_2 = Task.objects.create(
            project=self.owner_project,
            title='Task 2 name',
            description='Task 2 description'
        )
        self.project_task_2.save()

        self.project_task_3 = Task.objects.create(
            project=self.owner_project,
            title='Task 3 name',
            description='Task 3 description'
        )
        self.project_task_3.save()


        # Then we create 3 task offers from the freelanceer. Do note that initial status is pending
        self.task_offer_1 = TaskOffer.objects.create(
            task=self.project_task_1,
            offerer=self.freelancer.profile,
            title="Offer 1 title",
            price=1,
            description="Offer 1 description",
            status=TaskOffer.PENDING
        )
        self.task_offer_1.save()

        self.task_offer_2 = TaskOffer.objects.create(
            task=self.project_task_2,
            offerer=self.freelancer.profile,
            title="Offer 2 title",
            price=1,
            description="Offer 2 description",
            status=TaskOffer.PENDING
        )
        self.task_offer_2.save()

        self.task_offer_3 = TaskOffer.objects.create(
            task=self.project_task_2,
            offerer=self.freelancer.profile,
            title="Offer 3 title",
            price=1,
            description="Offer 3 description",
            status=TaskOffer.PENDING
        )
        self.task_offer_3.save()

    def test_task_view_not_logged_in(self):
        task_id = self.project_task_1.id
        project_id = self.project_task_1.project_id
        response = self.client.get(reverse('task_view', kwargs={'task_id': task_id, 'project_id': project_id}))
        self.assertEqual(response.status_code, 302)

    def test_task_view_logged_in(self):
        self.client.force_login(user=self.owner_user)
        task_id = self.project_task_1.id
        project_id = self.project_task_1.project_id
        response = self.client.get(reverse('task_view', kwargs={'task_id': task_id, 'project_id': project_id}))
        self.assertEqual(response.status_code, 200)
    
    def test_task_view_offer_submit(self):
        data = {
                'offer_submit': True,
                'title': 'This is purely a test offer. I have not actually done anything.',
                'description': 'Same as above.',
                'price': 20,
                'taskvalue': self.project_task_1.id
            }
        post = self.factory.post('/projects/'+str(self.owner_project.id), data)
        setattr(post, 'session', 'session')
        messages = FallbackStorage(post)
        setattr(post, '_messages', messages)
        post.user = self.freelancer
        response = project_view(post, self.owner_project.id)
        self.assertEqual(200, response.status_code)

    '''
    Possible statuses in Task model:
    *  AWAITING_DELIVERY = 'ad'
    *  PENDING_ACCEPTANCE = 'pa'
    *  PENDING_PAYMENT = 'pp'
    *  PAYMENT_SENT = 'ps'
    *  DECLINED_DELIVERY = 'dd'

    Possible statuses in TaskOffer model:
    *  ACCEPTED = 'a'
    *  PENDING = 'p'
    *  DECLINED = 'd'
    '''


    def test_task_view_offer_submit_logic(self):
        # should be awaiting delivery (no one has delivered anything)
        self.assertEqual('ad', self.project_task_2.status)

        # should be pending since owner has not accepted or declined
        self.assertEqual('p', self.task_offer_2.status)

        # check that the task has no accepted offers
        self.assertIsNone(Task.accepted_task_offer(self.project_task_2))
        

        # change status from pending to accepted
        self.task_offer_2.status = TaskOffer.ACCEPTED
        self.task_offer_2.save()
        self.assertEqual('a', self.task_offer_2.status)

        # should now be in query set for accepted offers
        self.assertEqual(self.task_offer_2, Task.accepted_task_offer(self.project_task_2))
        
        # change status from accepted to declined
        self.task_offer_2.status = TaskOffer.DECLINED
        self.task_offer_2.save()
        self.assertEqual('d', self.task_offer_2.status)

        # check that the task has no accepted offers
        self.assertIsNone(Task.accepted_task_offer(self.project_task_2))

        # change status from accepted to accepted
        self.task_offer_2.status = TaskOffer.ACCEPTED
        self.task_offer_2.save()
        self.assertEqual('a', self.task_offer_2.status)
    
    # TODO: do the same as below just for accept and delcine
    # Check pending in client
    def test_task_view_offer_pending(self):
        task_offer_id = self.task_offer_2.id
        response = self.client.post('/projects/' + str(self.owner_project.pk) + "/", {
            'status': 'p',
            'feedback': 'Still pending unfortunely',
            'taskofferid': task_offer_id,
            'offer_response': True
        })
        self.assertTrue(self.freelancer not in get_project_participants(self.owner_project))
        self.assertIsNone(get_accepted_task_offer(self.project_task_2))
        self.assertEqual('p', self.task_offer_2.status)
        self.assertEqual(response.context['project'], self.owner_project)
        self.assertEqual(check_taskoffers(self.project_task_2, self.freelancer)[0].status, 'p')

    def test_task_view_offer_declined(self):
        task_offer_id = self.task_offer_2.id
        # POST OFFER
        post = self.factory.post(
            '/projects/'+str(self.owner_project.id),
            {
                'offer_submit': True,
                'title': 'This is purely a test offer. I have not actually done anything.',
                # 'description': 'Same as above.',
                'price': 20,
                'taskvalue': self.project_task_1.id
            }
        )
        post.user = self.freelancer
        response = project_view(post, self.owner_project.id)
        # OFFER RESPONSE
        post = self.factory.post(
            '/projects/'+str(self.owner_project.id),
            {
                'status': 'd',
                'feedback': 'declined.',
                'taskofferid': task_offer_id,
                'offer_response': True
            }
        )
        post.user = self.owner_user
        response = project_view(post, self.owner_project.id)
        self.assertEqual(200, response.status_code)

        query = self.owner_project.participants.all()
        participants = set()
        for participant in query:
            participants.add(participant.user.username)
        
        self.assertTrue(self.freelancer.username not in participants)
        self.assertIsNone(get_accepted_task_offer(self.project_task_2))

        # check client context
        response = self.client.post('/projects/' + str(self.owner_project.pk) + "/", {
            'status': 'd',
            'feedback': 'declined.',
            'taskofferid': task_offer_id,
            'offer_response': True
        })
        self.assertEqual(response.context['project'], self.owner_project)
        self.assertEqual(check_taskoffers(self.project_task_2, self.freelancer)[0].status, 'd')

    def test_task_view_offer_accepted(self):
        task_offer_id = self.task_offer_2.id
        # POST OFFER
        post = self.factory.post(
            '/projects/'+str(self.owner_project.id),
            {
                'offer_submit': True,
                'title': 'This is purely a test offer. I have not actually done anything.',
                # 'description': 'Same as above.',
                'price': 20,
                'taskvalue': self.project_task_1.id
            }
        )
        post.user = self.freelancer
        response = project_view(post, self.owner_project.id)
        # OFFER RESPONSE
        post = self.factory.post(
            '/projects/'+str(self.owner_project.id),
            {
                'status': 'a',
                'feedback': 'accepted.',
                'taskofferid': task_offer_id,
                'offer_response': True
            }
        )
        post.user = self.owner_user
        response = project_view(post, self.owner_project.id)
        self.assertEqual(200, response.status_code)

        query = self.owner_project.participants.all()
        participants = set()
        for participant in query:
            participants.add(participant.user.username)
        
        self.assertTrue(self.freelancer.username in participants)
        self.assertIsNotNone(get_accepted_task_offer(self.project_task_2))

        # check client context
        response = self.client.post('/projects/' + str(self.owner_project.pk) + "/", {
            'status': 'a',
            'feedback': 'accepted.',
            'taskofferid': task_offer_id,
            'offer_response': True
        })
        self.assertEqual(response.context['project'], self.owner_project)
        self.assertEqual(check_taskoffers(self.project_task_2, self.freelancer)[0].status, 'a')

class MakeOfferTitleTestSuite(TestCase):
    def setUp(self):
        self.project_owner_user = User.objects.create_user(
            username='elizabeth',
            first_name='Elizabeth',
            last_name='Bennet',
            email='eliben@pride.com',
        )
        self.project_owner_user.save()
        self.category = ProjectCategory.objects.create(name="Painting")
        self.category.save()
        self.project_to_make_offer_to = Project.objects.create(
            user=self.project_owner_user.profile,
            title='Test project',
            description='Description',
            category=self.category
        )
        self.project_to_make_offer_to.save()
        self.user_making_offer = User.objects.create_user(
            username='sherlock',
            first_name='Sherlock',
            last_name='Holmes',
            email='shehol@mystery.com'
        )
        self.user_making_offer.save()
        self.owner_task = Task.objects.create(
            project=self.project_to_make_offer_to,
            title='Task name',
            description='Task description'
        )
        self.owner_task.save()
        self.factory = RequestFactory()

    def get_make_offer_request(self, data):
        request = self.factory.post('/project/1', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_make_offer_title_too_short(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)
        title_value = ""
        data = create_make_offer_content("title", title_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 0)
        TaskOffer.objects.all().delete()

    def test_make_offer_title_legal_min_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        title_value = "a"
        data = create_make_offer_content("title", title_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    def test_make_offer_title_just_above_min_legal_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        title_value = "a"*2
        data = create_make_offer_content("title", title_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    def test_make_offer_title_legal_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        title_value = "a"*15
        data = create_make_offer_content("title", title_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    def test_make_offer_title_just_below_max_legal_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        title_value = "a"*199
        data = create_make_offer_content("title", title_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    def test_make_offer_title_legal_max_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        title_value = "a"*200
        data = create_make_offer_content("title", title_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    def test_make_offer_title_legal_too_long(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        title_value = "a"*201
        data = create_make_offer_content("title", title_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 0)
        TaskOffer.objects.all().delete()

class MakeOfferDescriptionTestSuite(TestCase):
    def setUp(self):
        self.project_owner_user = User.objects.create_user(
            username='elizabeth',
            first_name='Elizabeth',
            last_name='Bennet',
            email='eliben@pride.com',
        )
        self.project_owner_user.save()
        self.category = ProjectCategory.objects.create(name="Painting")
        self.category.save()
        self.project_to_make_offer_to = Project.objects.create(
            user=self.project_owner_user.profile,
            title='Test project',
            description='Description',
            category=self.category
        )
        self.project_to_make_offer_to.save()
        self.user_making_offer = User.objects.create_user(
            username='sherlock',
            first_name='Sherlock',
            last_name='Holmes',
            email='shehol@mystery.com'
        )
        self.user_making_offer.save()
        self.owner_task = Task.objects.create(
            project=self.project_to_make_offer_to,
            title='Task name',
            description='Task description'
        )
        self.owner_task.save()
        self.factory = RequestFactory()

    def get_make_offer_request(self, data):
        request = self.factory.post('/project/1', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    def test_make_offer_description_too_short(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)
        description_value = ""
        data = create_make_offer_content("description", description_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 0)
        TaskOffer.objects.all().delete()

    def test_make_offer_description_legal_min_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        description_value = "a"
        data = create_make_offer_content("description", description_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    def test_make_offer_description_just_above_min_legal_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        description_value = "a"*2
        data = create_make_offer_content("description", description_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    def test_make_offer_description_legal_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        description_value = "a"*100
        data = create_make_offer_content("description", description_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    def test_make_offer_description_legal_max_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        description_value = "a"*500
        data = create_make_offer_content("description", description_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    def test_make_offer_description_just_below_max_legal_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        description_value = "a"*499
        data = create_make_offer_content("description", description_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    def test_make_offer_description_legal_too_long(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        description_value = "a"*501
        data = create_make_offer_content("description", description_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 0)
        TaskOffer.objects.all().delete()

class MakeOfferPriceTestSuite(TestCase):
    def setUp(self):
        self.project_owner_user = User.objects.create_user(
            username='elizabeth',
            first_name='Elizabeth',
            last_name='Bennet',
            email='eliben@pride.com',
        )
        self.project_owner_user.save()
        self.category = ProjectCategory.objects.create(name="Painting")
        self.category.save()
        self.project_to_make_offer_to = Project.objects.create(
            user=self.project_owner_user.profile,
            title='Test project',
            description='Description',
            category=self.category
        )
        self.project_to_make_offer_to.save()
        self.user_making_offer = User.objects.create_user(
            username='sherlock',
            first_name='Sherlock',
            last_name='Holmes',
            email='shehol@mystery.com'
        )
        self.user_making_offer.save()
        self.owner_task = Task.objects.create(
            project=self.project_to_make_offer_to,
            title='Task name',
            description='Task description'
        )
        self.owner_task.save()
        self.factory = RequestFactory()

    def get_make_offer_request(self, data):
        request = self.factory.post('/project/1', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request

    @unittest.skip("Should not accept negative values here")
    def test_make_offer_price_too_short(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)
        price_value = -1000
        data = create_make_offer_content("price", price_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 0)
        TaskOffer.objects.all().delete()

    def test_make_offer_price_legal_min_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        price_value = 0
        data = create_make_offer_content("price", price_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    def test_make_offer_price_just_above_min_legal_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        price_value = 1
        data = create_make_offer_content("price", price_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    def test_make_offer_price_legal_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        price_value = 25000
        data = create_make_offer_content("price", price_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()
    
    def test_make_offer_price_just_below_max_legal_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        price_value = pow(2,63) - 2
        data = create_make_offer_content("price", price_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    def test_make_offer_price_legal_max_length(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        price_value = pow(2, 63) - 1
        data = create_make_offer_content("price", price_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 1)
        TaskOffer.objects.all().delete()

    @unittest.skip("Overflow integer")
    def test_make_offer_price_legal_too_long(self):
        task_offers_before = TaskOffer.objects.all()
        self.assertEqual(len(task_offers_before), 0)

        price_value = pow(2, 63)
        data = create_make_offer_content("price", price_value)

        request = self.get_make_offer_request(data)
        
        request.user = self.user_making_offer
        response = project_view(request, self.project_to_make_offer_to.id)
        self.assertEqual(200, response.status_code)
        new_project_offers = TaskOffer.objects.all()
        self.assertEqual(len(new_project_offers), 0)
        TaskOffer.objects.all().delete()

class EmailOnNewOfferTestSuite(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(pk=1, name="Gardening")

        self.project_owner_user = User.objects.create_user(
            pk=1,
            username='Project_owner',
            email='proj_owner@gmail.com',
            password='HemmeligWooo213'
        )
        self.project_owner_user_profile = Profile.objects.get(user=self.project_owner_user)
        self.project_bidder_user = User.objects.create_user(
            username='Project_bidder',
            email='proj_bidder@gmail.com',
            password='HemmeligWooo213'
        )
        self.test_project = Project.objects.create(
            pk=1,
            user=self.project_owner_user_profile,
            title='Test Project',
            description='This is nothing more than a test. Stay calm.',
            category=self.category,
            status="o"
        )
        self.task_1 = Task.objects.create(
            pk=1,
            project=self.test_project,
            title='This task is purely for testing. I will not pay',
            description='^Same as above',
            budget=20
        )

    def test_email_sent_if_notifications_true(self):
        self.assertTrue(self.project_owner_user_profile.email_notifications)

        offers = TaskOffer.objects.all()
        self.assertEqual(len(offers), 0)
        data = {
                'offer_submit': True,
                'title': 'This is purely a test offer. I have not actually done anything.',
                'description': 'Same as above.',
                'price': 20,
                'taskvalue': self.task_1.id
            }
        post = self.factory.post('/project/'+str(self.project_bidder_user.id), data)
        setattr(post, 'session', 'session')
        messages = FallbackStorage(post)
        setattr(post, '_messages', messages)
        post.user = self.project_bidder_user

        response = project_view(post, self.test_project.id)
        offers = TaskOffer.objects.all()
        self.assertEqual(len(offers), 1)
        self.assertEqual(200, response.status_code)
        TaskOffer.objects.all().delete()
        # print("alert" in response.content.decode("utf-8"))
        alert_showing = "alert" in response.content.decode("utf-8")
        self.assertTrue(alert_showing)

    def test_email_not_sent_if_notifications_false(self):
        self.project_owner_user_profile.email_notifications = False
        self.project_owner_user_profile.save()

        self.assertFalse(self.project_owner_user_profile.email_notifications)

        offers = TaskOffer.objects.all()
        self.assertEqual(len(offers), 0)
        data = {
                'offer_submit': True,
                'title': 'This is purely a test offer. I have not actually done anything.',
                'description': 'Same as above.',
                'price': 20,
                'taskvalue': self.task_1.id
            }
        post = self.factory.post('/project/'+str(self.project_bidder_user.id), data)
        setattr(post, 'session', 'session')
        messages = FallbackStorage(post)
        setattr(post, '_messages', messages)
        post.user = self.project_bidder_user

        response = project_view(post, self.test_project.id)
        offers = TaskOffer.objects.all()
        self.assertEqual(len(offers), 1)
        self.assertEqual(200, response.status_code)
        TaskOffer.objects.all().delete()
        # print("alert" in response.content.decode("utf-8"))
        alert_showing = "alert" in response.content.decode("utf-8")
        self.assertFalse(alert_showing)


class GetAverageRatingTestSuite(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = ProjectCategory.objects.create(pk=1, name="Gardening")

        self.project_owner_user = User.objects.create_user(
            pk=1,
            username='Project_owner',
            email='proj_owner@gmail.com',
            password='HemmeligWooo213'
        )
        self.project_owner_user_profile = Profile.objects.get(user=self.project_owner_user)
        self.project_bidder_user = User.objects.create_user(
            username='Project_bidder',
            email='proj_bidder@gmail.com',
            password='HemmeligWooo213'
        )
        self.project_bidder_user_profile = Profile.objects.get(user=self.project_bidder_user)
        self.test_project1 = Project.objects.create(
            pk=1,
            user=self.project_owner_user_profile,
            title='Test Project',
            description='This is nothing more than a test. Stay calm.',
            category=self.category,
            status="o"
        )
        self.test_project2 = Project.objects.create(
            pk=2,
            user=self.project_owner_user_profile,
            title='Test Project',
            description='This is nothing more than a test. Stay calm.',
            category=self.category,
            status="o"
        )
        self.task_1 = Task.objects.create(
            pk=1,
            project=self.test_project1,
            title='This task is purely for testing. I will not pay',
            description='^Same as above',
            budget=20
        )
        self.task_2 = Task.objects.create(
            pk=2,
            project=self.test_project2,
            title='This task is purely for testing. I will not pay',
            description='^Same as above',
            budget=20
        )
        self.task_1_offer = TaskOffer.objects.create(
            task = self.task_1,
            title = "Task1 Offer",
            description = "Task1 description",
            price = 1000,
            offerer = self.project_bidder_user_profile,
            status = 'a' 
        )
        self.task_2_offer = TaskOffer.objects.create(
            task = self.task_2,
            title = "Task1 Offer",
            description = "Task1 description",
            price = 1000,
            offerer = self.project_bidder_user_profile,
            status = 'a' 
        )

        self.delivery_1 = Delivery.objects.create(
            pk = 1,
            task = self.task_1,
            comment = "test",
            delivery_user = self.project_bidder_user_profile
        )

        self.delivery_2 = Delivery.objects.create(
            pk = 2,
            task = self.task_2,
            comment = "test",
            delivery_user = self.project_bidder_user_profile
        )


    def make_delivery_response(self, project, task, user, data):
        request = self.factory.post('/project/'+str(project.id) + "/" + str(task.id) + "/", data)
        request.user = user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        return request


    def test_average_rating_should_be_zero_if_no_ratings(self):
        self.assertEqual(self.project_owner_user_profile.get_average_rating, 0)
    
    def make_data(self, value_to_change, value):
        data = {
            "status": 'a',
            "feedback": "Looking good", 
            "rating": 4,
            "delivery-id": self.delivery_1.id,
            "delivery-response": True
        }
    
        if (type(value_to_change) == type([])):
            for i in range(len(value_to_change)):
                data[value_to_change[i]] = value[i]
        elif (type(value_to_change) == type("")):
            data[value_to_change] = value
        return data

    def test_average_rating(self):
        rating1, rating2 = 5, 2
        data1 = self.make_data(["rating", "delivery-id"], [rating1, self.delivery_1.id])
        request = self.make_delivery_response(self.test_project1, self.task_1, self.project_owner_user, data1)
        response = task_view(request, self.test_project1.id, self.task_1.id)

        data2 = self.make_data(["rating", "delivery-id"], [rating2, self.delivery_2.id])
        request = self.make_delivery_response(self.test_project2, self.task_2, self.project_owner_user, data2)
        response = task_view(request, self.test_project2.id, self.task_2.id)

        profile = Profile.objects.get(user=self.project_bidder_user)
        self.assertEqual(profile.get_average_rating, (rating1 + rating2) / 2)
        self.assertEqual(profile.get_rating_count, 2)
        self.assertEqual(response.status_code, 200)
