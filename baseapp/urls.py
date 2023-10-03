from django.urls import path
from .views import TaskList, TaskDeets, CreateTask, TaskUpdate, DeleteTask, LoginPage, RegistrationPage
from django.contrib.auth.views import LogoutView

#as_view method returns a callable view that takes a request and returns a response
urlpatterns = [
    path('', TaskList.as_view(), name = 'home'),
    path('logout/', LogoutView.as_view(next_page = 'loginpage'), name = 'logO'),

    #path('tasks/<int:pk>/', TaskDeets.as_view(), name = 'task'),
    path('add-task/', CreateTask.as_view(), name = 'add-task'),
    path('update-task/<int:pk>/', TaskUpdate.as_view(), name = 'update-task'),
    path('delete/task/<int:pk>/', DeleteTask.as_view(), name = 'delete.task'),
    path('login/', LoginPage.as_view(), name = "loginpage"),
    path('register/', RegistrationPage.as_view(), name = "regist")
    ]

"""
next_page is used to redirect the user to a particular page after logout.
"""

#tasks/1 gives 1st task, tasks/2 gives 2nd task and so on...