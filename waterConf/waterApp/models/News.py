from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Kontent")
    excerpt = models.CharField(max_length=300, verbose_name="Qisqa mazmun")
    image = models.ImageField(upload_to='news/', verbose_name="Rasm")
    is_discount = models.BooleanField(default=False, verbose_name="Chegirma/Aksiya")
    discount_percent = models.PositiveIntegerField(blank=True, null=True, verbose_name="Chegirma foizi")
    valid_until = models.DateTimeField(blank=True, null=True, verbose_name="Amal qilish muddati")
    is_published = models.BooleanField(default=True, verbose_name="Nashr etilgan")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title