from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.utils import translation
from parler.utils.i18n import get_language

from .models import Room, Reservation
from django.http import HttpResponseRedirect

from django.shortcuts import render
from .models import Room


def home(request):
    # Aktivace jazyka na základě preferencí uživatele
    user_language = translation.get_language()
    translation.activate(user_language)

    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/room_list.html', {'rooms': rooms})


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'rooms/room_detail.html', {'room': room})


def reservation(request):
    if request.method == "POST":
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        room_id = request.POST.get('room_id')

        room = get_object_or_404(Room, pk=room_id)

        reservation = Reservation(
            room=room,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            check_in_date=request.POST.get('check_in_date'),
            check_out_date=request.POST.get('check_out_date'),
            payment_status="Pending"
        )
        reservation.save()

        return HttpResponseRedirect('/reservation_success')  # Příklad přesměrování na stránku úspěchu

    return render(request, 'rooms/reservation.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        send_mail(
            f'Kontakt od {name}',
            message,
            email,
            [settings.CONTACT_EMAIL],
        )
        return render(request, 'contact.html', {'message_sent': True})  # Opravený path k šabloně
    return render(request, 'contact.html')


def reserve_room(request):
    return None

def home_view(request):
    context = {
        'LANGUAGE_CODE': get_language(),
    }
    return render(request, 'home.html', context)


def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)

def custom_server_error(request):
    return render(request, '500.html', status=500)

def custom_permission_denied(request, exception):
    return render(request, '403.html', status=403)

def custom_bad_request(request, exception):
    return render(request, '400.html', status=400)
