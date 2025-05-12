from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    INTENSITY_CHOICES = [
        ('низька', 'низька'),
        ('середня', 'середня'),
        ('висока', 'висока'),
    ]
    
    TYPE_CHOICES = [
        ('аеробна', 'аеробна'),
        ('силова', 'силова'),
        ('розтяжка', 'розтяжка'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    duration = models.IntegerField()
    intensity = models.CharField(max_length=10, choices=INTENSITY_CHOICES)
    calories_burned = models.IntegerField()
    
    def __str__(self):
        return self.name

class ExerciseItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.IntegerField()
    
    @property
    def calories_burned(self):
        ratio = self.duration / self.exercise.duration
        return int(self.exercise.calories_burned * ratio)
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise.name} on {self.date}"
    
    class Meta:
        ordering = ['-date'] 