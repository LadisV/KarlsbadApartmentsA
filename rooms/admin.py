from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Room, Reservation, RoomImage
from django.utils.html import format_html


# Inline admin pro nahrávání více obrázků k jednomu pokoji
class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return ""
    image_preview.short_description = "Náhled obrázku"


# Konfigurace adminu pro model Room s podporou překladu
@admin.register(Room)
class RoomAdmin(TranslatableAdmin):
    inlines = [RoomImageInline]
    list_display = ('name', 'capacity')
    search_fields = ('translations__name',)
    list_filter = ('capacity',)


# Konfigurace adminu pro rezervace
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'room', 'check_in_date', 'check_out_date', 'payment_status')
    list_filter = ('payment_status', 'check_in_date', 'check_out_date')
    search_fields = ('customer_name', 'customer_email', 'customer_phone')
