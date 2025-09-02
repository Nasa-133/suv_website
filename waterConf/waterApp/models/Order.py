from django.db import models

from .Product import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('processing', 'Jarayonda'),
        ('delivered', 'Yetkazildi'),
        ('cancelled', 'Bekor qilindi'),
    ]

    # Kontakt va asosiy ma'lumotlar
    full_name = models.CharField(max_length=100, verbose_name="To'liq ism")
    phone = models.CharField(max_length=20, verbose_name="Telefon")

    # Manzil (asosiy)
    address = models.TextField(verbose_name="Manzil")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitude")

    # Manzil (batafsil)
    building = models.CharField(max_length=50, null=True, blank=True, verbose_name="Uy/Bino (№)")
    entrance = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Podezd")
    floor = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Qavat")

    # Buyurtma tarkibi
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miqdor")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Umumiy narx")

    # Xizmat holati
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Status")
    notes = models.TextField(blank=True, verbose_name="Izohlar")
    telegram_sent = models.BooleanField(default=False, verbose_name="Telegramga yuborildi")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.product.name}"

    def get_map_link(self):
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        return None

    def get_location_info(self):
        if self.latitude and self.longitude:
            return {
                'has_location': True,
                'latitude': float(self.latitude),
                'longitude': float(self.longitude),
                'map_link': self.get_map_link()
            }
        return {'has_location': False}

    @property
    def full_address(self):
        extra = []
        if self.building: extra.append(f"Uy/Bino: {self.building}")
        if self.entrance: extra.append(f"Podezd: {self.entrance}")
        if self.floor: extra.append(f"Qavat: {self.floor}")
        tail = (", ".join(extra)) if extra else ""
        return f"{self.address}{(' (' + tail + ')') if tail else ''}"