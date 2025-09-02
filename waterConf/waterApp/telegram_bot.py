import requests
from django.conf import settings
from .models.SiteSettings import SiteConfig

class TelegramBot:
    def __init__(self):
        config = SiteConfig.objects.first()
        self.bot_token = config.telegram_bot_token if config else None
        self.chat_id = config.telegram_chat_id if config else None
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """Oddiy matn xabarini yuborish"""
        try:
            resp = requests.post(
                f"{self.base_url}/sendMessage",
                data={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": parse_mode,
                    "disable_web_page_preview": True
                },
                timeout=10,
            )
            return resp.status_code == 200
        except requests.RequestException:
            return False

    def send_order_notification(self, order) -> bool:
        if not self.bot_token or not self.chat_id:
            return False

        # 1️.  Manzil bo‘yicha batafsil satr
        address_details = []
        if order.building:
            address_details.append(f"<b>🏠 Uy/Bino:</b> {order.building}")
        if order.entrance:
            address_details.append(f"<b>🚪 Podezd:</b> {order.entrance}")
        if order.floor:
            address_details.append(f"<b>🔢 Qavat:</b> {order.floor}")


        # 3️.  Xabar matnini yig‘ish
        message_parts = [
            "🛒 <b>Yangi buyurtma!</b>",
            "",
            f"👤 <b>Mijoz:</b> {order.full_name}",
            f"📞 <b>Telefon:</b> {order.phone}",
            f"📍 <b>Manzil:</b> {order.address}",
        ]

        if address_details:
            message_parts.append("\n".join(address_details))

        message_parts.extend([
            "",
            f"🏷️ <b>Mahsulot:</b> {order.product.name}",
            f"📦 <b>Miqdor:</b> {order.quantity} ta",
            f"💰 <b>Umumiy narx:</b> {order.total_price:,.0f} so'm",
        ])

        message_parts.extend([
            "",
            f"📝 <b>Izoh:</b> {order.notes or '—'}",
            "",
            f"⏰ <b>Vaqt:</b> {order.created_at.strftime('%d.%m.%Y %H:%M')}",
        ])

        # Koordinata bo‘lsa, link
        if order.latitude and order.longitude:
            map_link = order.get_map_link()
            message_parts.append(f"\n🗺️ <b>Xarita:</b> <a href=\"{map_link}\">Google Maps</a>")

        full_message = "\n".join(message_parts)

        # 4️.  Xabar yuborish
        sent = self.send_message(full_message)

        # 5️.  Geo yuborish (muvaffaqiyatli xabardan so‘ng)
        if sent and order.latitude and order.longitude:
            self.send_location(order.latitude, order.longitude,
                               f"{order.full_name} · {order.product.name}")

        return sent

    def send_location(self, latitude, longitude, title="Buyurtma manzili"):
        """Telegram botga joylashuvni yuborish"""
        try:
            response = requests.post(
                f"{self.base_url}/sendLocation",
                data={
                    'chat_id': self.chat_id,
                    'latitude': float(latitude),
                    'longitude': float(longitude),
                    'title': title
                },
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def send_contact_notification(self, contact):
        """Aloqa xabari haqida Telegramga yuborish"""
        if not self.bot_token or not self.chat_id:
            return False

        message = f"""
📧 <b>Yangi aloqa xabari!</b>

👤 <b>Ism:</b> {contact.name}
📞 <b>Telefon:</b> {contact.phone}
📧 <b>Email:</b> {contact.email or 'Korsatilmagan'}

💬 <b>Xabar:</b>
{contact.message}

⏰ <b>Vaqt:</b> {contact.created_at.strftime('%d.%m.%Y %H:%M')}
        """

        try:
            response = requests.post(
                f"{self.base_url}/sendMessage",
                data={
                    'chat_id': self.chat_id,
                    'text': message.strip(),
                    'parse_mode': 'HTML'
                },
                timeout=10
            )
            return response.status_code == 200
        except:
            return False