from rest_framework import serializers
from .models import UserPlan, PlanItem

class UserPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlan
        fields = ['id', 'initial_weight', 'goal_weight', 'calorie_intake_goal', 'exercise_calorie_goal', 'start_date', 'end_date']
        read_only_fields = ['id', 'start_date', 'end_date']

class PlanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanItem
        fields = ['id', 'plan', 'date', 'calories_consumed', 'calories_burned', 'weight_gained']
        read_only_fields = ['id']
        extra_kwargs = {
            'calories_consumed': {'allow_null': True, 'required': False},
            'calories_burned':   {'allow_null': True, 'required': False},
        }