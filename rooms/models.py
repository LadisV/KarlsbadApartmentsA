from django.db import models
from parler.models import TranslatableModel, TranslatedFields

# Model pro pokoje s podporou překladu
class Room(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name="Název pokoje"),  # Přeložitelný název pokoje
        description=models.TextField(verbose_name="Popis pokoje"),  # Přeložitelný popis pokoje
    )
    capacity = models.IntegerField(verbose_name="Kapacita")  # Kapacita pokoje
    image = models.ImageField(upload_to='room_images/', blank=True, null=True, verbose_name="Obrázek pokoje")  # Obrázek pokoje

    def __str__(self):
        # Vrátí překlad názvu pokoje nebo název v libovolném dostupném jazyce
        return self.safe_translation_getter('name', any_language=True)


# Model pro více obrázků k jednotlivým pokojům
class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images', verbose_name="Pokoj")  # Vztah k modelu Room
    image = models.ImageField(upload_to='room_images/', blank=True, null=True, verbose_name="Obrázek")  # Obrázek pokoje
    description = models.CharField(max_length=255, blank=True, verbose_name="Popis obrázku")  # Popis obrázku (volitelné pole)

    def __str__(self):
        # Vrátí informaci o obrázku a k jakému pokoji patří
        return f"Image for {self.room.safe_translation_getter('name', any_language=True)}"


# Model pro rezervace pokojů
class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Pokoj")  # Vztah k modelu Room
    customer_name = models.CharField(max_length=100, verbose_name="Jméno zákazníka")  # Jméno zákazníka
    customer_email = models.EmailField(verbose_name="Email zákazníka")  # Email zákazníka
    customer_phone = models.CharField(max_length=15, verbose_name="Telefon zákazníka")  # Telefon zákazníka
    check_in_date = models.DateField(verbose_name="Datum příjezdu")  # Datum příjezdu
    check_out_date = models.DateField(verbose_name="Datum odjezdu")  # Datum odjezdu
    payment_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Paid', 'Paid')],
        verbose_name="Stav platby"  # Stav platby
    )
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID platby Stripe")  # ID platby (volitelné)

    def __str__(self):
        # Vrátí informace o rezervaci včetně pokoje a jména zákazníka
        return f"Reservation for {self.room.safe_translation_getter('name', any_language=True)} by {self.customer_name}"
