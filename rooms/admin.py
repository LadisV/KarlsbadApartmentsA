from django.contrib import admin
from .models import Room, Reservation, RoomImage

# Inline admin pro nahrávání více obrázků k jednomu pokoji
class RoomImageInline(admin.TabularInline):
    model = RoomImage  # Model pro obrázky
    extra = 1  # Kolik polí pro nové obrázky se má zobrazit

# Konfigurace adminu pro model Room
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline]  # Přidání inline obrázků k pokoji
    list_display = ('name', 'capacity')  # Sloupce v seznamu pokojů
    search_fields = ('name',)  # Hledání podle názvu

# Registrace modelů
admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation)
admin.site.register(RoomImage)
