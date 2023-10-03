from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import TodoTasks
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy 
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm #used for creating a new user to use my web application
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

#logout functionality direct in urls.py
#reverse_lazy accepts view and returns an URL. Used for redirecting once form is submitted

# Create your views here.

class LoginPage(LoginView):
    template_name = 'baseapp/loginpage.html'
    fields = '__all__'
    redirect_authenticated_user = True #if already logged in, don't come here

    def get_success_url(self):
        return reverse_lazy('home')

class RegistrationPage(FormView):
    #formView is used to display and verify a Django form
    template_name = 'baseapp/registrationPage.html'
    form_class = UserCreationForm

    #redirect to home once user is signed up
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()

        #user successfully created
        if user is not None:
            login(self.request, user)
        return super(RegistrationPage, self).form_valid(form)

    #this is used if user is already logged in, registration page is not accessible and he/she/they are redirected to home

    def get(self, *args, **kwargs):

        #is_authenticated is attribute of User
        if self.request.user.is_authenticated:
            return redirect('home')

        #if user is not authenticated call super() implementation
        return super(RegistrationPage, self).get(*args, **kwargs)

#class-based view
class TaskList(LoginRequiredMixin, ListView):  #loginrequiredmixin restricts guests users. Should login

    """
    ListView is a generic class based view used to display a page representing a list of objects.
    self.object_list contains list of objects  that the view is operating upon
    By default listview looks for a template with "{model name}_list.html". Configure this in templates/baseapp

    """

    model = TodoTasks
    
    #used to change default object_list to name of our choice
    context_object_name = 'tasks'

    template_name = 'baseapp/listDemo.html'


    """
    to add extra content to our existing context, we need to
    override this method. Default implementation of this method adds the
    object being displayed to the template.
    """

    def get_context_data(self, **kwargs):
        #call base implementation to get context
        context = super().get_context_data(**kwargs)

        #to ensure each user sees his/her own tasks
        context['tasks'] = context['tasks'].filter(user=self.request.user)

        #to show how many incomplete tasks are present
        context['incompletetasks'] = context['tasks'].filter(completed = False).count()

        #for search functionality

        #get word from the searchbar
        search_items = self.request.GET.get('searchbar') or ''

        #if search input exists, filter accordingly
        if search_items:
            context['tasks'] = context['tasks'].filter(tasktitle__icontains = search_items)
        
        context['searchitems'] = search_items
        return context
"""
DetailView returns information about a simple item(single model instance)
"""
class TaskDeets(LoginRequiredMixin, DetailView):

    #this view looks for {model_name}_detail.html in templates.
    model = TodoTasks

    context_object_name = 'task'

    #to override default template names like {}_detail and {}_list
    template_name = 'baseapp/detailDemo.html'


#createview is used for forms and need to do a database insertion of submission of form

class CreateTask(LoginRequiredMixin, CreateView):

    #looks for template with {{model}}_form.html
    model = TodoTasks

    #__all__ includes all fields under model class.

    fields = ['tasktitle', 'completed', 'description']

    #redirect
    success_url = reverse_lazy('home') #check url.py


    def form_valid(self, form):

        #user is the logged in user
        
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)



#redisplays form if it has validation errors
#and save changes of the object to the database
"""
whenever we click on update it prepopulates the existing 
task data in 
the form

"""
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = TodoTasks
    fields = '__all__'
    success_url = reverse_lazy('home')


"""
If request method is GET, view will display confirmation page or else
if it is POST, view will delete the object
"""

class DeleteTask(LoginRequiredMixin, DeleteView):
    model = TodoTasks
    context_object_name = 'thetask'
    success_url = reverse_lazy('home')
    template_name = 'baseapp/deleteDemo.html'