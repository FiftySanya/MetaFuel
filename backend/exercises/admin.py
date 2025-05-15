from django.contrib import admin
from .models import Exercise, ExerciseItem

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'intensity', 'duration', 'calories_burned')
    list_filter = ('type', 'intensity')
    search_fields = ('name',)

@admin.register(ExerciseItem)
class ExerciseItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'exercise', 'date', 'duration', 'calories_burned')
    list_filter = ('date', 'exercise')
    search_fields = ('user__username', 'exercise__name') 