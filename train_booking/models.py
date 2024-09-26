from django.db import models

class Seat(models.Model):
    seat_number = models.IntegerField(unique=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} - {'Booked' if self.is_booked else 'Available'}"
