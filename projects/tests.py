from django.test import TestCase, Client, RequestFactory
import unittest
from projects.views import project_view, get_user_task_permissions
from .models import Project, Task, TaskFile, TaskOffer, Delivery, ProjectCategory, Team, TaskFileTeam, directory_path
from user.models import User, Profile

# Create your tests here.


class ProjectViewTestSuite(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        projectCategory = ProjectCategory.objects.create(pk=1, name="Gardening")

        self.user_owner = User.objects.create_user(
            pk = 1,
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
            pk =1,
            user = self.user_owner_profile,
            title = 'Test Project',
            description = 'This is nothing more than a test. Stay calm.',
            category = projectCategory,
            status = "o"
        )

        self.task_1 = Task.objects.create(
            pk = 1,
            project = self.test_project,
            title = 'This task is purely for testing. I will not pay',
            description = '^Same as above',
            budget = 150000000
        )

        self.task_1_offer = TaskOffer.objects.create(
            pk = 1,
            task = self.task_1, 
            title = 'This offer is purely for testing. I will not actually complete the task',
            description = 'Same as above',
            price = 150000000,
            offerer = self.user_bidder.profile
        )

        


    def test_project_view(self):
        request = self.factory.get('/project/'+str(self.user_owner.id))
        request.user = self.user_owner
        response = project_view(request, self.test_project.id)
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



if __name__ == '__main__':
    unittest.main()
3