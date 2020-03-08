from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
import unittest
from projects.views import project_view, get_user_task_permissions
from .models import Project, Task, TaskFile, TaskOffer, Delivery, ProjectCategory, Team, TaskFileTeam, directory_path
from user.models import User, Profile
from django.urls import reverse


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


class ProjectViewTests(TestCase):

    def setUp(self):
        self.owner_user = User.objects.create_user(
            username='elizabeth',
            first_name='Elizabeth',
            last_name='Bennet',
            email='eliben@pride.com',
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
        self.project_manager = User.objects.create_user(
            username='sherlock',
            first_name='Sherlock',
            last_name='Holmes',
            email='shehol@mystery.com'
        )
        self.project_manager.save()
        self.owner_task = Task.objects.create(
            project=self.owner_project,
            title='Task name',
            description='Task description'
        )
        self.offer = TaskOffer.objects.create(
            task=self.owner_task,
            offerer=self.project_manager.profile,
            title="Offer title",
            price=1,
            description="Offer description",
            status=TaskOffer.ACCEPTED
        )
        self.offer.save()

        self.owner_task.save()

    def test_project_view_not_logged_in(self):
        task_id = self.owner_task.id
        project_id = self.owner_task.project_id
        response = self.client.get(
            reverse('task_view', kwargs={'task_id': task_id, 'project_id': project_id}))
        self.assertEqual(response.status_code, 302)

    def test_task_view_logged_in(self):
        self.client.force_login(user=self.owner_user)
        task_id = self.owner_task.id
        project_id = self.owner_task.project_id
        response = self.client.get(
            reverse('task_view', kwargs={'task_id': task_id, 'project_id': project_id}))
        self.assertEqual(response.status_code, 200)


class ProjectViewTests(TestCase):

    def setUp(self):
        self.owner_user = User.objects.create_user(
            username='john5',
            first_name='john5',
            last_name='johnson5',
            email='jlennon5@beatles.com',
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
        self.project_manager = User.objects.create_user(
            username='john3',
            first_name='john3',
            last_name='johnson3',
            email='jlennon3@beatles.com'
        )
        self.project_manager.save()
        self.owner_task = Task.objects.create(
            project=self.owner_project,
            title='Task name',
            description='Task description'
        )
        self.offer = TaskOffer.objects.create(
            task=self.owner_task,
            offerer=self.project_manager.profile,
            title="Offer title",
            price=1,
            description="Offer description",
            status=TaskOffer.ACCEPTED
        )
        self.offer.save()

        self.owner_task.save()

    def test_project_view_not_logged_in(self):
        task_id = self.owner_task.id
        project_id = self.owner_task.project_id
        response = self.client.get(
            reverse('project_view', kwargs={'project_id': project_id}))
        self.assertEqual(response.status_code, 200)

    def test_project_view_logged_in(self):
        self.client.force_login(user=self.owner_user)
        task_id = self.owner_task.id
        project_id = self.owner_task.project_id
        response = self.client.get(
            reverse('project_view', kwargs={'project_id': project_id}))
        self.assertEqual(response.status_code, 200)


class ProjectViewTestSuite(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        projectCategory = ProjectCategory.objects.create(
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
            category=projectCategory,
            status="o"
        )

        self.task_1 = Task.objects.create(
            pk=1,
            project=self.test_project,
            title='This task is purely for testing. I will not pay',
            description='^Same as above',
            budget=150000000
        )

        self.task_1_offer = TaskOffer.objects.create(
            pk=1,
            task=self.task_1,
            title='This offer is purely for testing. I will not actually complete the task',
            description='Same as above',
            price=150000000,
            offerer=self.user_bidder.profile
        )

    def test_project_view(self):
        request = self.factory.get('/project/'+str(self.user_owner.id))
        request.user = self.user_owner
        response = project_view(request, self.test_project.id)
        self.assertEqual(200, response.status_code)

        post = self.factory.post(
            '/project'+str(self.user_owner.id),
            {
                'offer_response': '',
                'status': 'a'
            }
        )

        post.user = self.user_bidder
        response = project_view(post, self.test_project.id)
        self.assertEqual(200, response.status_code)

        post = self.factory.post(
            '/project/'+str(self.user_owner.id),
            {
                'status_change': '',
                'status': 'i'
            }
        )
        post.user = self.user_owner
        response = project_view(post, self.test_project.id)
        self.assertEqual(response.status_code, 200)

        post = self.factory.post(
            '/project/'+str(self.user_bidder.id),
            {
                'offer_submit': '',
                'title': 'This is purely a test offer. I have not actually done anything.',
                'description': 'Same as above.',
                'price': 1500000,
                'taskvalue': self.task_1.id
            }
        )
        post.user = self.user_bidder
        response = project_view(post, self.test_project.id)
        self.assertEqual(200, response.status_code)

        post = self.factory.post(
            '/project'+str(self.user_owner.id),
            {
                'taskofferid': self.task_1_offer.id,
                'offer_response': '',
                'feedback': 'This is purely test feedback, I do not actually accept',
                'status': 'a'
            }
        )

        post.user = self.user_bidder
        response = project_view(post, self.test_project.id)
        self.assertEqual(200, response.status_code)
