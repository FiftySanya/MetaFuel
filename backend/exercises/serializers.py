from rest_framework import serializers
from .models import Exercise, ExerciseItem

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'type', 'description', 'duration', 'intensity', 'calories_burned']

class ExerciseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'duration', 'calories_burned']

class ExerciseItemSerializer(serializers.ModelSerializer):
    exercise_details = ExerciseSerializer(source='exercise', read_only=True)
    calories_burned = serializers.ReadOnlyField()
    
    class Meta:
        model = ExerciseItem
        fields = ['id', 'exercise_details', 'duration', 'calories_burned']

class ExerciseItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseItem
        fields = ['exercise', 'date', 'duration'] 