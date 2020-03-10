from django.test import TestCase
import unittest
from projects.views import project_view, get_user_task_permissions
from .models import Project, Task, TaskFile, TaskOffer, Delivery, ProjectCategory, Team, TaskFileTeam, directory_path

# Create your tests here.



# if __name__ == '__main__':
#     unittest.main()