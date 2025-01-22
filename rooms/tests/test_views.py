import pytest
import tempfile
from django.urls import reverse
from django.test import Client
from rooms.models import Room, Reservation
from django.utils.translation import activate
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def room(db):
    temp_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
    uploaded_image = SimpleUploadedFile(
        name=temp_image,
        content=b"test_image_content",
        content_type="image/jpeg"
    )
    return Room.objects.create(
        name="Test Room",
        description="Test Description",
        capacity=2,
        image=uploaded_image,
    )

@pytest.mark.django_db
def test_home_view(client, room):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert room.name in str(response.content)

@pytest.mark.django_db
def test_home_view(client, room):
    activate('en')  # Nastavení jazyka na angličtinu
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_room_detail_view(client, room):
    url = reverse('room_detail', args=[room.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert room.description in str(response.content)

@pytest.mark.django_db
def test_reservation_creation(client, room):
    url = reverse('reservation')
    data = {
        'customer_name': 'John Doe',
        'customer_email': 'john@example.com',
        'customer_phone': '123456789',
        'room_id': room.id,
        'check_in_date': '2025-01-01',
        'check_out_date': '2025-01-05',
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Přesměrování na stránku úspěchu
    assert Reservation.objects.count() == 1
