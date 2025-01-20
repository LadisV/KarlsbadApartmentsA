from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.IntegerField()
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.room.name}"


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')])
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Reservation for {self.room.name} by {self.customer_name}"

