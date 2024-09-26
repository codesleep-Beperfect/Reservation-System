from django.shortcuts import render
from django.http import JsonResponse
from .models import Seat

def seat_status(request):
    # Retrieve all seats and pass them to the template
    seats = Seat.objects.all().order_by('seat_number')
    return render(request, 'booking/seat_status.html', {'seats': seats})

def book_seats(request):
    if request.method == 'POST':
        
        num_seats = int(request.POST.get('num_seats'))
        available_seats = Seat.objects.filter(is_booked=False)[:num_seats]
    
        if available_seats.count() < num_seats:
            return JsonResponse({"message": "Not enough seats available"}, status=400)

        # Book the seats
        seat_numbers = []
        for seat in available_seats:
            seat.is_booked = True
            seat.save()
            seat_numbers.append(seat.seat_number)
        # Update session with newly booked seats
        booked_seats = request.session.get('booked_seats', [])
        booked_seats.extend(seat_numbers)
        request.session['booked_seats'] = booked_seats

        return JsonResponse({"message": "Seats booked successfully", "seats": seat_numbers})
    
    booked_seats = request.session.get('booked_seats', [])

    valid_booked_seats = Seat.objects.filter(seat_number__in=booked_seats, is_booked=True).values_list('seat_number', flat=True)
    valid_booked_seats = list(valid_booked_seats)  # Convert to list

    # If the session contains seats that are no longer booked, update the session
    if set(booked_seats) != set(valid_booked_seats):
        request.session['booked_seats'] = valid_booked_seats
    # Fetch all seats to render in the template
    all_seats = Seat.objects.all()
    return JsonResponse({"booked_seats": valid_booked_seats, "all_seats": list(all_seats.values())})
