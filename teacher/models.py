from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=30)
    room_number = models.CharField(max_length=5)
    profile_image = models.ImageField(upload_to='teacher_profile_images', blank=True)
    subjects_taught = models.ManyToManyField(Subject, related_name='teachers')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
