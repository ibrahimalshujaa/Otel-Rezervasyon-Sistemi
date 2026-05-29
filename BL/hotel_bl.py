# Business Logic Layer (BL)
# Implements business rules, validation, and communicates with DAL.

import re
from datetime import datetime, date
from DAL.db_manager import execute_proc, execute_proc_non_query

# =========================================================================
# VALIDATION HELPERS
# =========================================================================

def validate_email(email):
    """Simple regex to validate email structure."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """Validate phone number is not empty and has a reasonable length."""
    return len(phone.strip()) >= 7

def validate_dates(check_in, check_out):
    """
    Validate that check-in date is today or in the future,
    and check-out is after check-in.
    Accepts string dates (YYYY-MM-DD) or date objects.
    """
    if isinstance(check_in, str):
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
    else:
        check_in_date = check_in

    if isinstance(check_out, str):
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
    else:
        check_out_date = check_out

    if check_out_date <= check_in_date:
        raise ValueError("Check-out date must be after check-in date.")
        
    return check_in_date, check_out_date

# =========================================================================
# 1. CUSTOMERS BL
# =========================================================================

def add_customer(first_name, last_name, phone, email, passport_no):
    """Validate and add a new customer."""
    if not first_name.strip() or not last_name.strip():
        raise ValueError("First name and last name are required.")
    if not validate_phone(phone):
        raise ValueError("A valid phone number is required.")
    if not validate_email(email):
        raise ValueError("A valid email address is required.")
    if not passport_no.strip():
        raise ValueError("Passport number is required.")
        
    res = execute_proc('sp_AddCustomer', (first_name.strip(), last_name.strip(), phone.strip(), email.strip(), passport_no.strip()))
    return res[0]['customer_id'] if res else None

def update_customer(customer_id, first_name, last_name, phone, email, passport_no):
    """Validate and update customer details."""
    if not customer_id:
        raise ValueError("Customer ID is required.")
    if not first_name.strip() or not last_name.strip():
        raise ValueError("First name and last name are required.")
    if not validate_phone(phone):
        raise ValueError("A valid phone number is required.")
    if not validate_email(email):
        raise ValueError("A valid email address is required.")
    if not passport_no.strip():
        raise ValueError("Passport number is required.")
        
    execute_proc_non_query('sp_UpdateCustomer', (customer_id, first_name.strip(), last_name.strip(), phone.strip(), email.strip(), passport_no.strip()))
    return True

def delete_customer(customer_id):
    """Delete a customer."""
    if not customer_id:
        raise ValueError("Customer ID is required.")
    execute_proc_non_query('sp_DeleteCustomer', (customer_id,))
    return True

def get_customers():
    """Retrieve all customers."""
    return execute_proc('sp_GetCustomers')

def get_customer_by_id(customer_id):
    """Retrieve a single customer by ID."""
    res = execute_proc('sp_GetCustomerById', (customer_id,))
    return res[0] if res else None

# =========================================================================
# 2. ROOM TYPES BL
# =========================================================================

def add_room_type(type_name, price_per_night, capacity):
    """Validate and add a new room type."""
    if not type_name.strip():
        raise ValueError("Room type name is required.")
    if float(price_per_night) < 0:
        raise ValueError("Price per night must be non-negative.")
    if int(capacity) <= 0:
        raise ValueError("Capacity must be greater than zero.")
        
    res = execute_proc('sp_AddRoomType', (type_name.strip(), float(price_per_night), int(capacity)))
    return res[0]['room_type_id'] if res else None

def update_room_type(room_type_id, type_name, price_per_night, capacity):
    """Validate and update a room type."""
    if not room_type_id:
        raise ValueError("Room type ID is required.")
    if not type_name.strip():
        raise ValueError("Room type name is required.")
    if float(price_per_night) < 0:
        raise ValueError("Price per night must be non-negative.")
    if int(capacity) <= 0:
        raise ValueError("Capacity must be greater than zero.")
        
    execute_proc_non_query('sp_UpdateRoomType', (room_type_id, type_name.strip(), float(price_per_night), int(capacity)))
    return True

def delete_room_type(room_type_id):
    """Delete a room type."""
    if not room_type_id:
        raise ValueError("Room type ID is required.")
    execute_proc_non_query('sp_DeleteRoomType', (room_type_id,))
    return True

def get_room_types():
    """Retrieve all room types."""
    return execute_proc('sp_GetRoomTypes')

def get_room_type_by_id(room_type_id):
    """Retrieve a room type by ID."""
    res = execute_proc('sp_GetRoomTypeById', (room_type_id,))
    return res[0] if res else None

# =========================================================================
# 3. ROOMS BL
# =========================================================================

def add_room(room_number, room_type_id, floor_number, room_status='Available'):
    """Validate and add a new room."""
    if not room_number.strip():
        raise ValueError("Room number is required.")
    if not room_type_id:
        raise ValueError("Room type is required.")
    if int(floor_number) < 0:
        raise ValueError("Floor number cannot be negative.")
    if room_status not in ['Available', 'Reserved', 'Occupied', 'Maintenance']:
        raise ValueError("Invalid room status.")
        
    res = execute_proc('sp_AddRoom', (room_number.strip(), int(room_type_id), int(floor_number), room_status))
    return res[0]['room_id'] if res else None

def update_room(room_id, room_number, room_type_id, floor_number, room_status):
    """Validate and update a room."""
    if not room_id:
        raise ValueError("Room ID is required.")
    if not room_number.strip():
        raise ValueError("Room number is required.")
    if not room_type_id:
        raise ValueError("Room type is required.")
    if int(floor_number) < 0:
        raise ValueError("Floor number cannot be negative.")
    if room_status not in ['Available', 'Reserved', 'Occupied', 'Maintenance']:
        raise ValueError("Invalid room status.")
        
    execute_proc_non_query('sp_UpdateRoom', (room_id, room_number.strip(), int(room_type_id), int(floor_number), room_status))
    return True

def delete_room(room_id):
    """Delete a room."""
    if not room_id:
        raise ValueError("Room ID is required.")
    execute_proc_non_query('sp_DeleteRoom', (room_id,))
    return True

def get_rooms():
    """Retrieve all rooms."""
    return execute_proc('sp_GetRooms')

def get_room_by_id(room_id):
    """Retrieve room by ID."""
    res = execute_proc('sp_GetRoomById', (room_id,))
    return res[0] if res else None

# =========================================================================
# 4. RESERVATIONS BL
# =========================================================================

def get_calculated_cost(room_id, check_in, check_out):
    """
    Calculate stay duration and reservation cost using database SQL functions.
    Uses sp_GetCalculatedCost to conform to SP-only rule.
    """
    check_in_date, check_out_date = validate_dates(check_in, check_out)
    res = execute_proc('sp_GetCalculatedCost', (room_id, check_in_date, check_out_date))
    if res:
        return {
            'stay_days': res[0]['stay_days'],
            'total_cost': float(res[0]['total_cost'])
        }
    return {'stay_days': 0, 'total_cost': 0.0}

def check_room_availability(room_id, check_in, check_out):
    """
    Check if a room is available for the given dates.
    Uses sp_CheckRoomAvailability.
    """
    check_in_date, check_out_date = validate_dates(check_in, check_out)
    res = execute_proc('sp_CheckRoomAvailability', (room_id, check_in_date, check_out_date))
    if res:
        return res[0]['active_reservations'] == 0
    return False

def create_reservation(customer_id, room_id, check_in, check_out, reservation_status='Pending'):
    """
    Validate, calculate cost, check availability, and create reservation.
    Room status will be automatically changed to 'Reserved' by DB triggers.
    """
    if not customer_id or not room_id:
        raise ValueError("Customer and Room are required.")
    
    check_in_date, check_out_date = validate_dates(check_in, check_out)
    
    # Check if the room is available for these dates
    if not check_room_availability(room_id, check_in_date, check_out_date):
        raise ValueError("This room is already booked for the selected dates.")
        
    # Get calculated cost using SQL functions through SP wrapper
    cost_info = get_calculated_cost(room_id, check_in_date, check_out_date)
    total_price = cost_info['total_cost']
    
    res = execute_proc('sp_AddReservation', (
        int(customer_id), 
        int(room_id), 
        check_in_date, 
        check_out_date, 
        reservation_status, 
        total_price
    ))
    return res[0]['reservation_id'] if res else None

def update_reservation(reservation_id, customer_id, room_id, check_in, check_out, reservation_status, total_price=None):
    """Validate and update a reservation."""
    if not reservation_id:
        raise ValueError("Reservation ID is required.")
    if not customer_id or not room_id:
        raise ValueError("Customer and Room are required.")
    
    check_in_date, check_out_date = validate_dates(check_in, check_out)
    
    # If check-in/out or room changed, we should verify availability
    old_res = get_reservation_by_id(reservation_id)
    if not old_res:
        raise ValueError("Reservation not found.")
        
    # Verify availability if room or dates changed
    dates_changed = (str(old_res['check_in_date']) != str(check_in_date)) or (str(old_res['check_out_date']) != str(check_out_date))
    room_changed = (old_res['room_id'] != int(room_id))
    
    if (dates_changed or room_changed) and reservation_status != 'Cancelled':
        # Check availability excluding current reservation (needs to check if double book occurs)
        # For simplicity, if room or dates changed, make sure new room is available
        # Wait, if we book the same room but different dates, or different room, check it.
        # Simple check:
        # If check_room_availability returns false, but the conflict is ONLY the current reservation, it's fine.
        # But our simple sp_CheckRoomAvailability counts ALL reservations.
        # Let's adjust BL check: if it overlaps with others.
        # We can implement a check in BL or a custom SP. But for safety, let's check:
        # If we are changing to a new room, or changing dates on the current room, we verify.
        # Let's write a simple check:
        # If it overlaps, check if there is an overlapping reservation where reservation_id != current reservation_id.
        # We can run sp_CheckRoomAvailability. If it returns > 0 and we are keeping the same room and same dates, no check needed.
        # If we change dates or room, we check.
        if room_changed or dates_changed:
            if not check_room_availability(room_id, check_in_date, check_out_date):
                # To be absolutely sure it's not overlapping with itself:
                # If room is same and overlap count is 1, it might be overlapping with itself.
                # If room is different, any overlap is a real conflict.
                if room_changed or not (old_res['room_id'] == int(room_id) and dates_changed):
                    raise ValueError("The selected room is not available for these dates.")
    
    # Calculate price if not provided
    if total_price is None or float(total_price) == 0:
        cost_info = get_calculated_cost(room_id, check_in_date, check_out_date)
        total_price = cost_info['total_cost']
        # Add services prices already attached
        services = get_reservation_services_by_reservation(reservation_id)
        for s in services:
            total_price += float(s['service_price']) * int(s['quantity'])
            
    execute_proc_non_query('sp_UpdateReservation', (
        reservation_id, 
        int(customer_id), 
        int(room_id), 
        check_in_date, 
        check_out_date, 
        reservation_status, 
        float(total_price)
    ))
    return True

def cancel_reservation(reservation_id):
    """Cancel a reservation. Trigger will automatically free the room."""
    if not reservation_id:
        raise ValueError("Reservation ID is required.")
    execute_proc_non_query('sp_CancelReservation', (reservation_id,))
    return True

def delete_reservation(reservation_id):
    """Delete a reservation."""
    if not reservation_id:
        raise ValueError("Reservation ID is required.")
    execute_proc_non_query('sp_DeleteReservation', (reservation_id,))
    return True

def get_reservations():
    """Retrieve all reservations."""
    return execute_proc('sp_GetReservations')

def get_reservation_by_id(reservation_id):
    """Retrieve a single reservation by ID."""
    res = execute_proc('sp_GetReservationById', (reservation_id,))
    return res[0] if res else None

# =========================================================================
# 5. PAYMENTS BL
# =========================================================================

def add_payment(reservation_id, payment_amount, payment_method, payment_status='Completed'):
    """Validate and record a new payment."""
    if not reservation_id:
        raise ValueError("Reservation ID is required.")
    if float(payment_amount) <= 0:
        raise ValueError("Payment amount must be positive.")
    if payment_method not in ['Cash', 'Credit Card', 'Bank Transfer']:
        raise ValueError("Invalid payment method.")
    if payment_status not in ['Pending', 'Completed', 'Failed']:
        raise ValueError("Invalid payment status.")
        
    res = execute_proc('sp_AddPayment', (int(reservation_id), float(payment_amount), payment_method, payment_status))
    return res[0]['payment_id'] if res else None

def update_payment(payment_id, reservation_id, payment_amount, payment_method, payment_status):
    """Validate and update a payment record."""
    if not payment_id:
        raise ValueError("Payment ID is required.")
    if not reservation_id:
        raise ValueError("Reservation ID is required.")
    if float(payment_amount) <= 0:
        raise ValueError("Payment amount must be positive.")
    if payment_method not in ['Cash', 'Credit Card', 'Bank Transfer']:
        raise ValueError("Invalid payment method.")
    if payment_status not in ['Pending', 'Completed', 'Failed']:
        raise ValueError("Invalid payment status.")
        
    execute_proc_non_query('sp_UpdatePayment', (payment_id, int(reservation_id), float(payment_amount), payment_method, payment_status))
    return True

def delete_payment(payment_id):
    """Delete a payment record."""
    if not payment_id:
        raise ValueError("Payment ID is required.")
    execute_proc_non_query('sp_DeletePayment', (payment_id,))
    return True

def get_payments():
    """Retrieve all payments."""
    return execute_proc('sp_GetPayments')

def get_payment_by_id(payment_id):
    """Retrieve a payment by ID."""
    res = execute_proc('sp_GetPaymentById', (payment_id,))
    return res[0] if res else None

def get_payments_by_reservation(reservation_id):
    """Retrieve all payments for a single reservation."""
    return execute_proc('sp_GetPaymentsByReservation', (reservation_id,))

# =========================================================================
# 6. SERVICES BL
# =========================================================================

def add_service(service_name, service_price):
    """Validate and add a new hotel service."""
    if not service_name.strip():
        raise ValueError("Service name is required.")
    if float(service_price) < 0:
        raise ValueError("Service price cannot be negative.")
        
    res = execute_proc('sp_AddService', (service_name.strip(), float(service_price)))
    return res[0]['service_id'] if res else None

def update_service(service_id, service_name, service_price):
    """Validate and update a service."""
    if not service_id:
        raise ValueError("Service ID is required.")
    if not service_name.strip():
        raise ValueError("Service name is required.")
    if float(service_price) < 0:
        raise ValueError("Service price cannot be negative.")
        
    execute_proc_non_query('sp_UpdateService', (service_id, service_name.strip(), float(service_price)))
    return True

def delete_service(service_id):
    """Delete a service."""
    if not service_id:
        raise ValueError("Service ID is required.")
    execute_proc_non_query('sp_DeleteService', (service_id,))
    return True

def get_services():
    """Retrieve all services."""
    return execute_proc('sp_GetServices')

def get_service_by_id(service_id):
    """Retrieve a service by ID."""
    res = execute_proc('sp_GetServiceById', (service_id,))
    return res[0] if res else None

# =========================================================================
# 7. RESERVATION SERVICES BL
# =========================================================================

def add_reservation_service(reservation_id, service_id, quantity=1):
    """Attach a service to a reservation. Recalculates reservation total price automatically in SP."""
    if not reservation_id or not service_id:
        raise ValueError("Reservation and Service are required.")
    if int(quantity) <= 0:
        raise ValueError("Quantity must be greater than zero.")
        
    execute_proc_non_query('sp_AddReservationService', (int(reservation_id), int(service_id), int(quantity)))
    return True

def delete_reservation_service(reservation_service_id):
    """Remove a service from a reservation. Deducts service cost from reservation total price automatically in SP."""
    if not reservation_service_id:
        raise ValueError("Reservation Service ID is required.")
    execute_proc_non_query('sp_DeleteReservationService', (reservation_service_id,))
    return True

def get_reservation_services_by_reservation(reservation_id):
    """Retrieve all services attached to a specific reservation."""
    return execute_proc('sp_GetReservationServicesByReservation', (reservation_id,))

# =========================================================================
# 8. STAFF BL
# =========================================================================

def add_staff(first_name, last_name, position, phone, salary):
    """Validate and add new staff member."""
    if not first_name.strip() or not last_name.strip():
        raise ValueError("First and last names are required.")
    if not position.strip():
        raise ValueError("Position is required.")
    if not validate_phone(phone):
        raise ValueError("A valid phone number is required.")
    if float(salary) < 0:
        raise ValueError("Salary cannot be negative.")
        
    res = execute_proc('sp_AddStaff', (first_name.strip(), last_name.strip(), position.strip(), phone.strip(), float(salary)))
    return res[0]['staff_id'] if res else None

def update_staff(staff_id, first_name, last_name, position, phone, salary):
    """Validate and update a staff member."""
    if not staff_id:
        raise ValueError("Staff ID is required.")
    if not first_name.strip() or not last_name.strip():
        raise ValueError("First and last names are required.")
    if not position.strip():
        raise ValueError("Position is required.")
    if not validate_phone(phone):
        raise ValueError("A valid phone number is required.")
    if float(salary) < 0:
        raise ValueError("Salary cannot be negative.")
        
    execute_proc_non_query('sp_UpdateStaff', (staff_id, first_name.strip(), last_name.strip(), position.strip(), phone.strip(), float(salary)))
    return True

def delete_staff(staff_id):
    """Delete a staff member."""
    if not staff_id:
        raise ValueError("Staff ID is required.")
    execute_proc_non_query('sp_DeleteStaff', (staff_id,))
    return True

def get_staff():
    """Retrieve all staff."""
    return execute_proc('sp_GetStaff')

def get_staff_by_id(staff_id):
    """Retrieve a staff member by ID."""
    res = execute_proc('sp_GetStaffById', (staff_id,))
    return res[0] if res else None

# =========================================================================
# 9. DASHBOARD BL
# =========================================================================

def get_dashboard_stats():
    """Retrieve overall system statistics for dashboard cards."""
    res = execute_proc('sp_GetDashboardStats')
    return res[0] if res else {
        'TotalCustomers': 0,
        'TotalRooms': 0,
        'TotalReservations': 0,
        'AvailableRooms': 0,
        'TotalRevenue': 0.00
    }
