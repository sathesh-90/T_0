from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Link task to user
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # no need for null=True with TextField
    due_date = models.DateField()

    STATUS_CHOICES = [
        ('incomplete', 'Incomplete'),
        ('progressing', 'Progressing'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='incomplete')

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    def __str__(self):
        return f"{self.title} ({self.status})"
