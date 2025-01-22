import pytest
from rooms.models import Room, Reservation

@pytest.mark.django_db
def test_room_creation():
    room = Room.objects.create(
        name="Test Room",
        description="Test Description",
        capacity=2
    )
    assert Room.objects.count() == 1
    assert str(room) == "Test Room"

@pytest.mark.django_db
def test_reservation_creation():
    room = Room.objects.create(
        name="Test Room",
        description="Test Description",
        capacity=2
    )
    reservation = Reservation.objects.create(
        room=room,
        customer_name="John Doe",
        customer_email="john@example.com",
        customer_phone="123456789",
        check_in_date="2025-01-01",
        check_out_date="2025-01-05",
        payment_status="Pending"
    )
    assert Reservation.objects.count() == 1
    assert str(reservation) == f"Reservation for {room.name} by John Doe"
