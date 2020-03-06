from django.test import TestCase
import unittest
from projects.views import project_view, get_user_task_permissions
from .models import Project, Task, TaskFile, TaskOffer, Delivery, ProjectCategory, Team, TaskFileTeam, directory_path

# Create your tests here.


class testProjectViewSuite(TestCase):
    def testUpper(self):
        self.assertEqual(2, 5)

    def testCenter(self):
        self.assertEqual(4, 4)

    def testLower(self):
        self.assertEqual(2, 2)

class test_project_view(TestCase):
    def setup(self):
        project = Project.n


# if __name__ == '__main__':
#     unittest.main()