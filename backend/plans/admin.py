from django.contrib import admin
from .models import UserPlan, PlanItem

@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'initial_weight', 'goal_weight',
        'calorie_intake_goal', 'exercise_calorie_goal',
        'start_date', 'end_date', 'is_active'
    )
    list_filter = ('is_active', 'start_date', 'end_date', 'user')
    search_fields = ('user__username',)

@admin.register(PlanItem)
class PlanItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'plan', 'date',
        'calories_consumed', 'calories_burned', 'weight_gained'
    )
    list_filter = ('date', 'plan')
    search_fields = ('plan__user__username',) 