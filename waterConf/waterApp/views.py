from decimal import Decimal

from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
import json

# Model imports
from .models.SiteSettings import SiteConfig
from .models.About import About
from .models.Contact import ContactMessage
from .models.FAQ import FAQ
from .models.HomePage import HomePage
from .models.News import News
from .models.Partner import Partner
from .models.Product import Category, Product
from .models.Testimonial import Testimonial
from .models.Order import Order
from .telegram_bot import TelegramBot


def get_site_config():
    """Barcha sahifalar uchun umumiy sayt sozlamalari"""
    config, created = SiteConfig.objects.get_or_create(pk=1)
    return config


def home_view(request):
    """Bosh sahifa"""
    context = {
        'site_config': get_site_config(),
        'banners': HomePage.objects.filter(is_active=True),
        'about': About.objects.first(),
        'featured_products': Product.objects.filter(is_active=True)[:4],
        'categories': Category.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True)[:6],
        'partners': Partner.objects.all()[:8],
        'latest_news': News.objects.filter(is_published=True)[:3],
        'active_discounts': News.objects.filter(
            is_published=True,
            is_discount=True
        )[:2],
        'page_title': 'Bosh sahifa',
        'meta_description': 'TozaSuv - O\'zbekistondagi eng sifatli ichimlik suvi. Toza, sof va foydali suv mahsulotlari.'
    }
    return render(request, 'home.html', context)


def about_view(request):
    """Biz haqimizda sahifasi"""
    about_obj = About.objects.first()

    context = {
        'site_config': get_site_config(),
        'about': about_obj,
        'testimonials': Testimonial.objects.filter(is_active=True)[:6],
        'partners': Partner.objects.all(),
        'featured_products': Product.objects.filter(is_active=True),
        'page_title': 'Biz haqimizda',
        'meta_description': 'TozaSuv kompaniyasi tarixi, maqsad va vazifalari haqida ma\'lumot.'
    }
    return render(request, 'about.html', context)


def products_view(request):
    """Mahsulotlar katalogi"""
    # Filter parametrlari
    category_id = request.GET.get('category')
    size_filter = request.GET.get('size')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort', 'name')

    # Asosiy queryset
    products_list = Product.objects.filter(is_active=True)

    # Filtrlash
    if category_id:
        products_list = products_list.filter(category_id=category_id)

    if size_filter:
        products_list = products_list.filter(size=size_filter)

    if search_query:
        products_list = products_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )

    # Jami mahsulotlar sonini paginatsiyadan OLDIN olish kerak
    total_products_count = products_list.count()

    # Saralash
    if sort_by == 'price_low':
        products_list = products_list.order_by('price')
    elif sort_by == 'price_high':
        products_list = products_list.order_by('-price')
    elif sort_by == 'newest':
        products_list = products_list.order_by('-created_at')
    else:
        products_list = products_list.order_by('name')

    # Pagination
    paginator = Paginator(products_list, 12)  # Sahifadagi mahsulotlar soni
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'site_config': get_site_config(),
        'products': page_obj,  # Bu shablondagi for loop uchun
        'page_obj': page_obj,  # <<--- MUHIM O'ZGARTIRISH: Bu paginatsiya uchun
        'categories': Category.objects.filter(is_active=True),
        'sizes': Product.VOLUME_CHOICES,
        'current_category': category_id,
        'current_size': size_filter,
        'current_search': search_query,
        'current_sort': sort_by,
        'total_products': total_products_count,  # Paginatsiyadan oldingi hisob
        'featured_products': Product.objects.filter(is_active=True),
        # Buni ham paginatsiya qilish kerak bo'lishi mumkin
        'page_title': 'Mahsulotlar',
        'meta_description': 'TozaSuv mahsulotlari katalogi. Turli hajmdagi toza ichimlik suvlari.'
    }
    return render(request, 'products.html', context)


def product_detail_view(request, product_id):
    """Mahsulot tafsilotlari"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'site_config': get_site_config(),
        'product': product,
        'related_products': related_products,
        'page_title': product.name,
        'featured_products': Product.objects.filter(is_active=True),
        'meta_description': product.short_description
    }
    return render(request, 'product_detail.html', context)


def news_view(request):
    """Yangiliklar va chegirmalar"""
    # Filter
    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'discount':
        news_list = News.objects.filter(is_published=True, is_discount=True)
    elif filter_type == 'news':
        news_list = News.objects.filter(is_published=True, is_discount=False)
    else:
        news_list = News.objects.filter(is_published=True)

    # Pagination
    paginator = Paginator(news_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'site_config': get_site_config(),
        'news': page_obj,
        'page_obj': page_obj,
        'current_filter': filter_type,
        'discount_count': News.objects.filter(is_published=True, is_discount=True).count(),
        'news_count': News.objects.filter(is_published=True, is_discount=False).count(),
        'page_title': 'Yangiliklar va chegirmalar',
        'featured_products': Product.objects.filter(is_active=True),
        'meta_description': 'TozaSuv yangiliklari, aksiyalar va chegirmalar haqida ma\'lumot.'
    }
    return render(request, 'news.html', context)


def news_detail_view(request, news_id):
    """Yangilik tafsilotlari"""
    news = get_object_or_404(News, id=news_id, is_published=True)
    related_news = News.objects.filter(
        is_published=True
    ).exclude(id=news.id)[:3]

    context = {
        'site_config': get_site_config(),
        'news': news,
        'related_news': related_news,
        'page_title': news.title,
        'meta_description': news.excerpt
    }
    return render(request, 'news_detail.html', context)


def contact_view(request):
    """Aloqa sahifasi"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        message = request.POST.get('message')

        if name and phone and message:
            # Contact message yaratish
            contact_msg = ContactMessage.objects.create(
                name=name,
                phone=phone,
                email=email,
                message=message
            )

            # Telegram botga yuborish
            bot = TelegramBot()
            telegram_sent = bot.send_contact_notification(contact_msg)

            if telegram_sent:
                messages.success(request, 'Xabaringiz muvaffaqiyatli yuborildi! Tez orada javob beramiz.')
            else:
                messages.warning(request, 'Xabaringiz saqlandi, ammo xabarnoma yuborilmadi. Tez orada javob beramiz.')

            return redirect('contact')
        else:
            messages.error(request, 'Iltimos, barcha majburiy maydonlarni to\'ldiring.')

    context = {
        'site_config': get_site_config(),
        'faqs': FAQ.objects.filter(is_active=True),
        'page_title': 'Aloqa',
        'meta_description': 'TozaSuv bilan bog\'lanish. Telefon, email, manzil va aloqa formasi.'
    }
    return render(request, 'contact.html', context)


def faq_view(request):
    """Tez-tez so'raladigan savollar"""
    context = {
        'site_config': get_site_config(),
        'faqs': FAQ.objects.filter(is_active=True),
        'page_title': 'Tez-tez so\'raladigan savollar',
        'meta_description': 'TozaSuv mahsulotlari va xizmatlar haqida eng ko\'p so\'raladigan savollar va javoblar.'
    }
    return render(request, 'faq.html', context)


def testimonials_view(request):
    """Mijozlar sharhlari"""
    testimonials_list = Testimonial.objects.filter(is_active=True)

    # Pagination
    paginator = Paginator(testimonials_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'site_config': get_site_config(),
        'testimonials': page_obj,
        'page_title': 'Mijozlar sharhlari',
        'meta_description': 'TozaSuv mijozlarining fikr va tavsiyalari.'
    }
    return render(request, 'testimonials.html', context)


# AJAX Views
@csrf_exempt
def create_order_ajax(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': "Noto'g'ri so'rov."}, status=405)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': "JSON format xatosi."}, status=400)

    # Majburiy maydonlar
    full_name = data.get('full_name', '').strip()
    phone     = data.get('phone', '').strip()
    address   = data.get('address', '').strip()
    product_id = data.get('product_id')
    quantity   = data.get('quantity', 1)

    if not all([full_name, phone, address, product_id]):
        return JsonResponse({
            'success': False,
            'message': "Iltimos, barcha majburiy maydonlarni to'ldiring."
        }, status=400)

    # Mahsulotni topamiz
    product = get_object_or_404(Product, id=product_id, is_active=True)

    # Batafsil manzil maydonlari
    building      = data.get('building', '').strip() or None
    entrance      = data.get('entrance')
    floor         = data.get('floor')

    # Koordinatalar
    latitude  = data.get('latitude')
    longitude = data.get('longitude')

    order_kwargs = {
        'full_name': full_name,
        'phone': phone,
        'address': address,
        'product': product,
        'quantity': int(quantity),
        'total_price': product.price * int(quantity),
        'notes': data.get('notes', '').strip(),
        'status': 'new',
        'telegram_sent': False,
        # batafsil manzil
        'building': building,
        'entrance': int(entrance) if entrance else None,
        'floor': int(floor) if floor else None,
    }

    # Koordinatalarni kiritamiz
    if latitude and longitude:
        try:
            order_kwargs['latitude']  = Decimal(str(latitude))
            order_kwargs['longitude'] = Decimal(str(longitude))
        except (TypeError, ValueError):
            pass

    # Buyurtma yaratish
    order = Order.objects.create(**order_kwargs)

    # Telegram xabarini yuborish
    bot = TelegramBot()
    sent = bot.send_order_notification(order)

    # Telegram statusini yangilash
    order.telegram_sent = sent
    order.save(update_fields=['telegram_sent'])

    # Javob ma'lumotlari
    response_data = {
        'success': True,
        'message': "Buyurtmangiz muvaffaqiyatli qabul qilindi! Tez orada siz bilan bog'lanamiz.",
        'order_id': order.id,
    }

    # Agar koordinata kiritilgan bo'lsa, joylashuv ma'lumotini qo'shamiz
    loc = order.get_location_info()
    if loc.get('has_location'):
        response_data['location'] = loc

    return JsonResponse(response_data)

def search_products_ajax(request):
    """AJAX orqali mahsulot qidirish"""
    query = request.GET.get('q', '')

    if len(query) >= 2:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query),
            is_active=True
        )[:5]

        results = []
        for product in products:
            results.append({
                'id': product.id,
                'name': product.name,
                'size': product.size,
                'price': str(product.price),
                'image': product.image.url if product.image else '',
                'url': f'/products/{product.id}/'
            })

        return JsonResponse({'products': results})

    return JsonResponse({'products': []})


# API Views (ixtiyoriy)
def api_products(request):
    """API - Mahsulotlar ro'yxati"""
    products = Product.objects.filter(is_active=True).values(
        'id', 'name', 'size', 'price', 'short_description'
    )
    return JsonResponse({'products': list(products)})


def api_categories(request):
    """API - Kategoriyalar ro'yxati"""
    categories = Category.objects.filter(is_active=True).values(
        'id', 'name'
    )
    return JsonResponse({'categories': list(categories)})


# Error handlers
def handler404(request, exception):
    """404 sahifa topilmadi"""
    context = {
        'site_config': get_site_config(),
        'page_title': 'Sahifa topilmadi'
    }
    return render(request, '404.html', context, status=404)


def handler500(request):
    """500 server xatosi"""
    context = {
        'site_config': get_site_config(),
        'page_title': 'Server xatosi'
    }
    return render(request, '500.html', context, status=500)


# Context processors (settings.py ga qo'shish kerak)
def site_context(request):
    """Global context - barcha sahifalar uchun"""
    return {
        'site_config': get_site_config(),
        'categories_menu': Category.objects.filter(is_active=True)[:5],
        'cart_count': 0,  # Savat funktsiyasi qo'shilganda
    }