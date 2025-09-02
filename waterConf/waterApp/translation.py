from modeltranslation.translator import register, TranslationOptions, translator
from .models import About, HomePage, FAQ, Testimonial, Category, Product, News, SiteConfig


@register(About)
class AboutTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'mission', 'vision')

@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'button_text')

@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')

@register(Testimonial)
class TestimonialTranslationOptions(TranslationOptions):
    fields = ('full_name', 'position', 'message',)

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Category, CategoryTranslationOptions)

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description')

translator.register(Product, ProductTranslationOptions)

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'excerpt',)

@register(SiteConfig)
class SiteConfigTranslationOptions(TranslationOptions):
    fields = ('address',)