# mastertheorem/models.py

from django.db import models
from django.core.validators import MinValueValidator

class Algorithm(models.Model):
    name = models.CharField(max_length=255)
    a = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    b = models.IntegerField(default=2, validators=[MinValueValidator(2)])
    k = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    p = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    description = models.TextField()
    python_code = models.TextField()
    case = models.CharField(max_length=255, blank=True, null=True)
    time_complexity = models.CharField(max_length=255, blank=True, null=True)
    complexity_analysis = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
