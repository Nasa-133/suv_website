from django.db import models

class Testimonial(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="To'liq ism")
    position = models.CharField(max_length=100, blank=True, verbose_name="Lavozim/Kompaniya")
    message = models.TextField(verbose_name="Sharh")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5, verbose_name="Baho")
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name="Rasm")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mijoz sharhi"
        verbose_name_plural = "Mijozlar sharhlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.rating}⭐"