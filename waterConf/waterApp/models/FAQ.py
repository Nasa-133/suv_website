from django.db import models


class FAQ(models.Model):
    question = models.CharField(max_length=300, verbose_name="Savol")
    answer = models.TextField(verbose_name="Javob")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Ko'p so'raladigan savol"
        verbose_name_plural = "Ko'p so'raladigan savollar"

    def __str__(self):
        return self.question