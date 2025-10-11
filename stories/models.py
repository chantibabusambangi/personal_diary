from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    visibility = models.CharField(max_length=10, choices=[('private', 'Private'), ('public', 'Public')], default='private')
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title