from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    VOLUME_CHOICES = [
        ('0.5L', '0.5 Litr'),
        ('1L', '1 Litr'),
        ('1.5L', '1.5 Litr'),
        ('5L', '5 Litr'),
        ('19L', '19 Litr'),
    ]

    name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(verbose_name="Tavsif")
    short_description = models.CharField(max_length=300, verbose_name="Qisqa tavsif")
    size = models.CharField(max_length=10, choices=VOLUME_CHOICES, verbose_name="Hajm")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narx")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Eski narx")
    image = models.ImageField(upload_to='products/', verbose_name="Asosiy rasm")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Omborda mavjud")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']

    def get_discount_percent(self):
        if self.old_price:
            return round(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    def __str__(self):
        return f"{self.name} - {self.size}"
