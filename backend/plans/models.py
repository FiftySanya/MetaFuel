from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta, date

User = get_user_model()

class UserPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    initial_weight = models.DecimalField(max_digits=5, decimal_places=2)
    goal_weight = models.DecimalField(max_digits=5, decimal_places=2)
    calorie_intake_goal = models.PositiveIntegerField()
    exercise_calorie_goal = models.PositiveIntegerField()

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.start_date = date.today()
            self.end_date = self.start_date + timedelta(days=30)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"UserPlan {self.id} for {self.user.username}"

class PlanItem(models.Model):
    plan = models.ForeignKey(UserPlan, on_delete=models.CASCADE, related_name='days')
    date = models.DateField()
    calories_consumed = models.PositiveIntegerField(null=True, blank=True)
    calories_burned = models.PositiveIntegerField(null=True, blank=True)
    weight_gained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('plan', 'date')

    def __str__(self):
        return f"PlanItem {self.date} of plan {self.plan.id}"
