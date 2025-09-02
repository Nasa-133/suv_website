from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin

from .models import (
    SiteConfig, Product, Category, Order, News,
    Testimonial, FAQ, Partner, ContactMessage, HomePage, About
)

# --- 1. SiteConfig Admin ---
@admin.register(SiteConfig)
class SiteConfigAdmin(TranslationAdmin):
    list_display = ('site_name', 'phone', 'email')
    search_fields = ('site_name', 'phone', 'email')
    fieldsets = (
        ("Asosiy sozlamalar", {
            'fields': ('site_name', 'logo', 'phone', 'email')
        }),
        ("Manzil va xarita", {
            'fields': ('address', 'google_maps_embed')
        }),
        ("Ijtimoiy tarmoqlar", {
            'fields': ('facebook', 'instagram', 'telegram')
        }),
        ("Telegram bot sozlamalari", {
            'fields': ('telegram_bot_token', 'telegram_chat_id')
        }),
    )
    ordering = ['-id']


# --- 2. Category Admin ---
@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    prepopulated_fields = {'name': ('name',)}


# --- 3. Product Admin ---
@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('name', 'category', 'size', 'price', 'stock_quantity', 'is_active')
    list_filter = ('category', 'size', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'name': ('name',)}
    readonly_fields = ('get_discount_percent',)
    fieldsets = (
        ("Mahsulot ma'lumotlari", {
            'fields': ('name', 'category', 'size', 'description', 'short_description')
        }),
        ("Narx va chegirma", {
            'fields': ('price', 'old_price', 'get_discount_percent')
        }),
        ("Ombor", {
            'fields': ('stock_quantity', 'is_active')
        }),
        ("Rasm", {
            'fields': ('image',)
        }),
    )

    def get_discount_percent(self, obj):
        return f"{obj.get_discount_percent()}%"
    get_discount_percent.short_description = "Chegirma foizi"


# --- 4. Order Admin ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'product', 'quantity', 'total_price',
                    'status', 'has_location', 'telegram_sent', 'created_at')
    list_filter = ('status', 'telegram_sent', 'created_at', 'product')
    search_fields = ('full_name', 'phone', 'address')
    readonly_fields = ('created_at', 'updated_at', 'map_link_display')

    fieldsets = (
        ('Mijoz ma\'lumotlari', {
            'fields': ('full_name', 'phone', 'address')
        }),
        ('Joylashuv', {
            'fields': ('latitude', 'longitude', 'map_link_display'),
            'classes': ('collapse',)
        }),
        ('Buyurtma ma\'lumotlari', {
            'fields': ('product', 'quantity', 'total_price', 'notes')
        }),
        ('Status', {
            'fields': ('status', 'telegram_sent')
        }),
        ('Vaqt ma\'lumotlari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def has_location(self, obj):
        """Joylashuv mavjudligini ko'rsatish"""
        if obj.latitude and obj.longitude:
            return format_html(
                '<span style="color: green;"><i class="fas fa-check"></i> Mavjud</span>'
            )
        return format_html(
            '<span style="color: red;"><i class="fas fa-times"></i> Yo\'q</span>'
        )

    has_location.short_description = 'Xarita'

    def map_link_display(self, obj):
        """Xarita linkini ko'rsatish"""
        if obj.latitude and obj.longitude:
            map_link = obj.get_map_link()
            return format_html(
                '<a href="{}" target="_blank" class="btn btn-primary btn-sm">'
                '<i class="fas fa-map-marker-alt"></i> Xaritada ko\'rish</a>',
                map_link
            )
        return "Joylashuv ma'lumoti yo'q"

    map_link_display.short_description = 'Xarita linki'


# --- 5. News Admin ---
@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('title', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'title': ('title',)}
    fieldsets = (
        ("Asosiy", {
            'fields': ('title', 'excerpt', 'image', 'is_published')
        }),
        ("Kontent", {
            'fields': ('content',)
        }),
        ("Chegirma", {
            'fields': ('is_discount', 'discount_percent', 'valid_until')
        }),
    )


# --- 6. Testimonial Admin ---
@admin.register(Testimonial)
class TestimonialAdmin(TranslationAdmin):
    list_display = ('full_name', 'position', 'rating', 'is_active', 'created_at')
    list_filter = ('rating', 'is_active')
    search_fields = ('full_name', 'message')
    readonly_fields = ('created_at',)


# --- 7. FAQ Admin ---
@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ('question', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')


# --- 8. Partner Admin ---
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# --- 9. ContactMessage Admin ---
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'message')
    readonly_fields = ('created_at', 'is_read')
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "O'qilgan deb belgilash"


# --- 10. HomePage Banner Admin ---
@admin.register(HomePage)
class HomePageAdmin(TranslationAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)
    prepopulated_fields = {'title': ('title',)}
    fieldsets = (
        ("Banner", {
            'fields': ('title', 'subtitle', 'button_text', 'link', 'is_active')
        }),
        ("Rasm", {
            'fields': ('image',)
        }),
    )
# --- 11. About Page Admin ---
@admin.register(About)
class AboutAdmin(TranslationAdmin):
    list_display = ('title', 'vision')
    search_fields = ('title',)
    prepopulated_fields = {'title': ('title',)}
    fieldsets = (
        ("About Page", {
            'fields': ('title', 'content', 'mission', 'vision', 'image')
        }),
    )