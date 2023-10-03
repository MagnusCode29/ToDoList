from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#each class defines a database table

class TodoTasks(models.Model):

    #class attributes define the database fields


    #use foreign key for many-to-one relationships

    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)

    #models.CASCADE signifies that whenever a user is deleted delete all the tasks too

    tasktitle = models.CharField(max_length = 200)
    completed = models.BooleanField(default = False)
    description = models.TextField(null = True, blank = True)
    creation = models.DateTimeField(auto_now_add = True) #add current date and time
    

    #string representation of object created
    def __str__(self):
        return self.tasktitle

    #metadata of class is given using Meta inner class
    class Meta:
        ordering = ['completed'] #order based on completed or not