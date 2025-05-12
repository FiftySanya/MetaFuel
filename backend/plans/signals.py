from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PlanItem, UserPlan
from foods.models import MealItem
from exercises.models import ExerciseItem


def update_planitem_for(user, date):
    plan = (UserPlan.objects
            .filter(user=user, start_date__lte=date, end_date__gte=date)
            .order_by('-start_date', '-id')
            .first())
    if not plan:
        return

    consumed = sum(item.calories for item in MealItem.objects.filter(meal__user=user, meal__date=date))
    burned = sum(ex.calories_burned for ex in ExerciseItem.objects.filter(user=user, date=date))
    consumed_val = consumed if consumed > 0 else None
    burned_val = burned   if burned   > 0 else None
    defaults = {'calories_consumed': consumed_val, 'calories_burned': burned_val}
    
    PlanItem.objects.update_or_create(plan=plan, date=date, defaults=defaults)


@receiver(post_save, sender=MealItem)
def mealitem_saved(sender, instance, **kwargs):
    date = instance.meal.date
    user = instance.meal.user
    update_planitem_for(user, date)


@receiver(post_delete, sender=MealItem)
def mealitem_deleted(sender, instance, **kwargs):
    date = instance.meal.date
    user = instance.meal.user
    update_planitem_for(user, date)


@receiver(post_save, sender=ExerciseItem)
def exerciseitem_saved(sender, instance, **kwargs):
    update_planitem_for(instance.user, instance.date)


@receiver(post_delete, sender=ExerciseItem)
def exerciseitem_deleted(sender, instance, **kwargs):
    update_planitem_for(instance.user, instance.date) 