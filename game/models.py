from django.db import models
from django.utils import timezone

# Create your models here.
class Grid(models.Model):

    grid = models.CharField(max_length=81)
    difficulty = models.CharField(max_length=10, default='easy')
    source = models.CharField(max_length=255, default='Unknown')
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'Sudoku {self.id} from {self.source} date {self.date}'