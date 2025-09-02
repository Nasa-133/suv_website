from django.db import models


class HomePage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Qo'shimcha matn")
    image = models.ImageField(upload_to='banners/', verbose_name="Rasm")
    video = models.FileField(upload_to='banners/videos/', blank=True, null=True, verbose_name="Video")
    link = models.CharField(max_length=255, blank=True, verbose_name="Havola")
    button_text = models.CharField(max_length=50, blank=True, verbose_name="Tugma matni")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Bannerlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title