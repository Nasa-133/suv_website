from django.db import models

class Partner(models.Model):
    name = models.CharField("Hamkor nomi", max_length=255)
    logo = models.ImageField("Logo", upload_to='partners/')

    def __str__(self):
        return self.name