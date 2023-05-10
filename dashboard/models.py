from django.db import models
from django.contrib.auth.models import User

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tittle = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.tittle

    class Meta:
        verbose_name = "Notes"
        verbose_name_plural = "Notes"
class Homework(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    tittle = models.CharField(max_length=255)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.description

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title