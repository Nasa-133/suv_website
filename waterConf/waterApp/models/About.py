from django.db import models

class About(models.Model):
    title = models.CharField(max_length=200, default="Biz haqimizda")
    content = models.TextField()
    mission = models.TextField(help_text="Kompaniya maqsadi")
    vision = models.TextField(help_text="Kompaniya istiqboli")
    image = models.ImageField(upload_to='about/', blank=True, null=True)

    class Meta:
        verbose_name = "Biz haqimizda"
        verbose_name_plural = "Biz haqimizda"

    def __str__(self):
        return self.title