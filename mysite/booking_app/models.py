from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField



class Country (models.Model):
    country_image = models.ImageField(upload_to='country_images')
    country_name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.country_name


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(60)], null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    photo = models.ImageField(upload_to='user_images/', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    ROLE_CHOICES = (
    ('client', 'client'),
    ('owner', 'owner'))
    user_role = models.CharField(choices=ROLE_CHOICES, max_length=15, default='client')
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class City(models.Model):
    city_image = models.ImageField(upload_to='city_images')
    city_name = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.country}, {self.city_name}'


class Service(models.Model):
    service_image = models.ImageField(upload_to='service_images')
    service_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.service_name



class Hotel(models.Model):
    hotel_name = models.CharField(max_length=100)
    street = models.CharField(max_length=50)
    postal_code = models.PositiveIntegerField(unique=True, verbose_name='Postal Code')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotels')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    hotel_stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                                   null=True, blank=True)
    hotel_video = models.FileField(upload_to='hotel_videos', null=True, blank=True)
    description = models.TextField()
    service = models.ManyToManyField(Service)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.hotel_name


class HotelImage(models.Model):
    image = models.ImageField(upload_to='hotel_images')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_images')

    def __str__(self):
        return f'{self.hotel}, {self.image}'


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.PositiveIntegerField()
    ROOM_TYPE_CHOICES = (
    ('стандарт', 'стандарт'),
    ('семейный', 'семейный'),
    ('одноместный', 'одноместный'),
    ('люкс', 'люкс'))
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    ROOM_STATUS_CHOICES = (
    ('занят', 'занят'),
    ('забронирован', 'забронирован'),
    ('свободен', 'свободен'))
    room_status = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f'{self.hotel}, {self.room_number}'


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room_images')

    def __str__(self):
        return f'{self.room}, {self.image}'

class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.hotel}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    text = models.TextField()
    created_date = models.DateTimeField()

    def __str__(self):
        return f'{self.user}, {self.hotel}'

