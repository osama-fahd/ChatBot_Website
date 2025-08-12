from django.db import models

class Exercise(models.Model):
    class WorkoutCategory(models.TextChoices):
        HOME_WORKOUT = 'home', 'Home Workout'
        CLUB_WORKOUT = 'club', 'Club Workout'
        BOTH_WORKOUTS = 'both', 'Home and Club Workouts'
        
    class EquipmentCategory(models.TextChoices):
        NO_EQUIPMENT = 'none', 'No Machine'
        MACHINE = 'machine', 'Machine'
        
    class ExerciseCategory(models.TextChoices):
        STRENGTH = 'strength', 'Strength'
        CARDIO = 'cardio', 'Cardio'
        FLEXIBILITY = 'flexibility', 'Flexibility'
        
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="media/images/exercises/")
    video_link = models.URLField(blank=True)
    video = models.FileField(upload_to="media/videos/", blank=True)
    
    workout_category = models.CharField(
        max_length=30,
        choices=WorkoutCategory.choices
    )
    equipment_category = models.CharField(
        max_length=30,
        choices=EquipmentCategory.choices
    )
    exercise_category = models.CharField(
        max_length=30,
        choices=ExerciseCategory.choices
    )


    def __str__(self):
        return self.name

class Step(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    instruction = models.TextField()
    
    def __str__(self) -> str:
        return f'{self.exercise.name}- step id: {self.id}'
