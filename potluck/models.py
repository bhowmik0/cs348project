from django.db import models
from django.contrib.auth.models import User

class PotluckEvent(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        indexes = [
            models.Index(fields=['date']),
        ]
    def __str__(self):
        return self.title

class DishSignup(models.Model):
    CATEGORY_CHOICES = [
        ('Main', 'Main'),
        ('Dessert', 'Dessert'),
        ('Drink', 'Drink'),
        ('Side', 'Side'),
    ]

    event = models.ForeignKey(PotluckEvent, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    class Meta:
        indexes = [
            models.Index(fields=['category']),
        ]
    def __str__(self):
        return f"{self.dish_name} by {self.participant.username}"

class RSVP(models.Model):
    STATUS_CHOICES = [
        ('yes', 'Yes'),
        ('maybe', 'Maybe'),
        ('no', 'No'),
    ]

    event = models.ForeignKey(PotluckEvent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.user.username}: {self.status}"
