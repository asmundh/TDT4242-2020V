from django.test import TestCase

from .views import get_user_task_permissions
from .models import Task, Project, ProjectCategory, TaskOffer, Team
from user.models import Profile
from django.contrib.auth.models import User
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


class TaskViewTests(TestCase):

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

    def test_task_view_not_logged_in(self):
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
