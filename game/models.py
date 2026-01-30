from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
class Grid(models.Model):
    grid = models.CharField(max_length=81)
    difficulty = models.CharField(max_length=10, default='easy')
    source = models.CharField(max_length=255, default='Unknown')
    date = models.DateField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='puzzles')
    is_public = models.BooleanField(default=True)

    def __str__(self):
        owner = self.created_by.username if self.created_by else 'Anonymous'
        return f'Sudoku {self.id} from {self.source} date {self.date}'