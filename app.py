# Presentation Layer (UI Routes)
# Entry point of the Hotel Reservation Management System.
# Communicates exclusively with the Business Logic Layer (BL).

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import BL.hotel_bl as bl

app = Flask(__name__)
app.secret_key = "hotel_reservation_secret_key_extremely_secure"
app.config['JSON_AS_ASCII'] = False
app.json.ensure_ascii = False

# Inject some common variables/helpers into templates
@app.context_processor
def inject_now():
    return {'active_page': None}

# =========================================================================
# DASHBOARD ROUTE
# =========================================================================
@app.route('/')
def dashboard():
    try:
        stats = bl.get_dashboard_stats()
        recent_reservations = bl.get_reservations()
        room_types = bl.get_room_types()
        return render_template('dashboard.html', 
                               stats=stats, 
                               recent_reservations=recent_reservations, 
                               room_types=room_types,
                               active_page='dashboard')
    except Exception as e:
        flash(f"Dashboard verileri yüklenirken hata oluştu: {str(e)}", "error")
        return render_template('dashboard.html', 
                               stats={'TotalCustomers':0, 'TotalRooms':0, 'TotalReservations':0, 'AvailableRooms':0, 'TotalRevenue':0.0},
                               recent_reservations=[],
                               room_types=[],
                               active_page='dashboard')

# =========================================================================
# CUSTOMERS ROUTES
# =========================================================================
@app.route('/customers')
def customers_list():
    try:
        customers = bl.get_customers()
        return render_template('customers.html', customers=customers, active_page='customers')
    except Exception as e:
        flash(f"Müşteri listesi yüklenemedi: {str(e)}", "error")
        return render_template('customers.html', customers=[], active_page='customers')

@app.route('/customers/add', methods=['POST'])
def customer_add():
    try:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        passport_no = request.form.get('passport_no')
        
        bl.add_customer(first_name, last_name, phone, email, passport_no)
        flash("Müşteri başarıyla eklendi.", "success")
    except Exception as e:
        flash(f"Müşteri eklenirken hata: {str(e)}", "error")
    return redirect(url_for('customers_list'))

@app.route('/customers/update', methods=['POST'])
def customer_update():
    try:
        customer_id = request.form.get('customer_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        passport_no = request.form.get('passport_no')
        
        bl.update_customer(customer_id, first_name, last_name, phone, email, passport_no)
        flash("Müşteri bilgileri başarıyla güncellendi.", "success")
    except Exception as e:
        flash(f"Müşteri güncellenirken hata: {str(e)}", "error")
    return redirect(url_for('customers_list'))

@app.route('/customers/delete', methods=['POST'])
def customer_delete():
    try:
        customer_id = request.form.get('customer_id')
        bl.delete_customer(customer_id)
        flash("Müşteri kaydı başarıyla silindi.", "success")
    except Exception as e:
        flash(f"Müşteri silinirken hata (aktif rezervasyonları olabilir): {str(e)}", "error")
    return redirect(url_for('customers_list'))

# =========================================================================
# ROOMS & ROOM TYPES ROUTES
# =========================================================================
@app.route('/rooms')
def rooms_list():
    try:
        rooms = bl.get_rooms()
        room_types = bl.get_room_types()
        return render_template('rooms.html', rooms=rooms, room_types=room_types, active_page='rooms')
    except Exception as e:
        flash(f"Oda listesi yüklenemedi: {str(e)}", "error")
        return render_template('rooms.html', rooms=[], room_types=[], active_page='rooms')

@app.route('/rooms/add', methods=['POST'])
def room_add():
    try:
        room_number = request.form.get('room_number')
        room_type_id = request.form.get('room_type_id')
        floor_number = request.form.get('floor_number')
        room_status = request.form.get('room_status')
        
        bl.add_room(room_number, room_type_id, floor_number, room_status)
        flash("Oda başarıyla eklendi.", "success")
    except Exception as e:
        flash(f"Oda eklenirken hata: {str(e)}", "error")
    return redirect(url_for('rooms_list'))

@app.route('/rooms/update', methods=['POST'])
def room_update():
    try:
        room_id = request.form.get('room_id')
        room_number = request.form.get('room_number')
        room_type_id = request.form.get('room_type_id')
        floor_number = request.form.get('floor_number')
        room_status = request.form.get('room_status')
        
        bl.update_room(room_id, room_number, room_type_id, floor_number, room_status)
        flash("Oda bilgileri güncellendi.", "success")
    except Exception as e:
        flash(f"Oda güncellenirken hata: {str(e)}", "error")
    return redirect(url_for('rooms_list'))

@app.route('/rooms/delete', methods=['POST'])
def room_delete():
    try:
        room_id = request.form.get('room_id')
        bl.delete_room(room_id)
        flash("Oda başarıyla silindi.", "success")
    except Exception as e:
        flash(f"Oda silinemedi (rezervasyonlarda kayıtlı olabilir): {str(e)}", "error")
    return redirect(url_for('rooms_list'))

# Room Types Subroutes
@app.route('/room_types/add', methods=['POST'])
def room_type_add():
    try:
        type_name = request.form.get('type_name')
        price_per_night = request.form.get('price_per_night')
        capacity = request.form.get('capacity')
        
        bl.add_room_type(type_name, price_per_night, capacity)
        flash("Oda tipi başarıyla eklendi.", "success")
    except Exception as e:
        flash(f"Oda tipi eklenirken hata: {str(e)}", "error")
    return redirect(url_for('rooms_list'))

@app.route('/room_types/update', methods=['POST'])
def room_type_update():
    try:
        room_type_id = request.form.get('room_type_id')
        type_name = request.form.get('type_name')
        price_per_night = request.form.get('price_per_night')
        capacity = request.form.get('capacity')
        
        bl.update_room_type(room_type_id, type_name, price_per_night, capacity)
        flash("Oda tipi güncellendi.", "success")
    except Exception as e:
        flash(f"Oda tipi güncellenirken hata: {str(e)}", "error")
    return redirect(url_for('rooms_list'))

@app.route('/room_types/delete', methods=['POST'])
def room_type_delete():
    try:
        room_type_id = request.form.get('room_type_id')
        bl.delete_room_type(room_type_id)
        flash("Oda tipi başarıyla silindi.", "success")
    except Exception as e:
        flash(f"Oda tipi silinemedi (bu tipe bağlı odalar olabilir): {str(e)}", "error")
    return redirect(url_for('rooms_list'))

# =========================================================================
# RESERVATIONS ROUTES
# =========================================================================
@app.route('/reservations')
def reservations_list():
    try:
        reservations = bl.get_reservations()
        return render_template('reservations.html', reservations=reservations, active_page='reservations')
    except Exception as e:
        flash(f"Rezervasyonlar yüklenemedi: {str(e)}", "error")
        return render_template('reservations.html', reservations=[], active_page='reservations')

@app.route('/reservations/create', methods=['GET'])
def reservation_create_page():
    try:
        customers = bl.get_customers()
        rooms = bl.get_rooms()
        return render_template('reservation_create.html', customers=customers, rooms=rooms, active_page='reservations')
    except Exception as e:
        flash(f"Rezervasyon oluşturma formu yüklenirken hata: {str(e)}", "error")
        return redirect(url_for('reservations_list'))

@app.route('/reservations/create', methods=['POST'])
def reservation_create():
    try:
        customer_id = request.form.get('customer_id')
        room_id = request.form.get('room_id')
        check_in = request.form.get('check_in_date')
        check_out = request.form.get('check_out_date')
        status = request.form.get('reservation_status')
        
        res_id = bl.create_reservation(customer_id, room_id, check_in, check_out, status)
        flash(f"Rezervasyon başarıyla oluşturuldu. (ID: #{res_id})", "success")
        return redirect(url_for('reservation_detail_page', reservation_id=res_id))
    except Exception as e:
        flash(f"Rezervasyon oluşturulamadı: {str(e)}", "error")
        return redirect(url_for('reservation_create_page'))

@app.route('/reservations/<int:reservation_id>')
def reservation_detail_page(reservation_id):
    try:
        res = bl.get_reservation_by_id(reservation_id)
        if not res:
            flash("Rezervasyon bulunamadı.", "error")
            return redirect(url_for('reservations_list'))
            
        attached_services = bl.get_reservation_services_by_reservation(reservation_id)
        payments = bl.get_payments_by_reservation(reservation_id)
        services = bl.get_services()
        rooms = bl.get_rooms() # for edit room modal
        
        return render_template('reservation_detail.html', 
                               res=res, 
                               attached_services=attached_services, 
                               payments=payments, 
                               services=services,
                               rooms=rooms,
                               active_page='reservations')
    except Exception as e:
        flash(f"Rezervasyon detayları yüklenemedi: {str(e)}", "error")
        return redirect(url_for('reservations_list'))

@app.route('/reservations/update', methods=['POST'])
def reservation_update():
    reservation_id = request.form.get('reservation_id')
    try:
        customer_id = request.form.get('customer_id')
        room_id = request.form.get('room_id')
        check_in = request.form.get('check_in_date')
        check_out = request.form.get('check_out_date')
        status = request.form.get('reservation_status')
        total_price = request.form.get('total_price')
        
        bl.update_reservation(reservation_id, customer_id, room_id, check_in, check_out, status, total_price)
        flash("Rezervasyon başarıyla güncellendi.", "success")
    except Exception as e:
        flash(f"Rezervasyon güncellenirken hata: {str(e)}", "error")
    return redirect(url_for('reservation_detail_page', reservation_id=reservation_id))

@app.route('/reservations/cancel', methods=['POST'])
def reservation_cancel():
    reservation_id = request.form.get('reservation_id')
    redirect_to = request.form.get('redirect_to', 'list')
    try:
        bl.cancel_reservation(reservation_id)
        flash("Rezervasyon başarıyla iptal edildi. Oda kullanıma açıldı.", "success")
    except Exception as e:
        flash(f"Rezervasyon iptal edilirken hata: {str(e)}", "error")
        
    if redirect_to == 'detail':
        return redirect(url_for('reservation_detail_page', reservation_id=reservation_id))
    return redirect(url_for('reservations_list'))

@app.route('/reservations/delete', methods=['POST'])
def reservation_delete():
    try:
        reservation_id = request.form.get('reservation_id')
        bl.delete_reservation(reservation_id)
        flash("Rezervasyon kaydı başarıyla silindi. Oda serbest bırakıldı.", "success")
    except Exception as e:
        flash(f"Rezervasyon kaydı silinirken hata: {str(e)}", "error")
    return redirect(url_for('reservations_list'))

# Dynamic Cost Calculation AJAX Endpoint using SQL functions through BL
@app.route('/api/reservations/calculate-cost')
def reservation_calculate_cost_api():
    room_id = request.args.get('room_id')
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    
    if not room_id or not check_in or not check_out:
        return jsonify({'success': False, 'message': 'Eksik parametreler.'}), 400
        
    try:
        cost_info = bl.get_calculated_cost(room_id, check_in, check_out)
        return jsonify({
            'success': True,
            'stay_days': cost_info['stay_days'],
            'total_cost': cost_info['total_cost']
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# Attach Extra Service to Reservation
@app.route('/reservations/services/add', methods=['POST'])
def reservation_attach_service():
    reservation_id = request.form.get('reservation_id')
    try:
        service_id = request.form.get('service_id')
        quantity = request.form.get('quantity', 1)
        
        bl.add_reservation_service(reservation_id, service_id, quantity)
        flash("Ek hizmet rezervasyona eklendi ve fiyata yansıtıldı.", "success")
    except Exception as e:
        flash(f"Hizmet eklenirken hata: {str(e)}", "error")
    return redirect(url_for('reservation_detail_page', reservation_id=reservation_id))

# Remove Extra Service from Reservation
@app.route('/reservations/services/delete', methods=['POST'])
def reservation_remove_service():
    reservation_id = request.form.get('reservation_id')
    try:
        reservation_service_id = request.form.get('reservation_service_id')
        
        bl.delete_reservation_service(reservation_service_id)
        flash("Hizmet rezervasyondan kaldırıldı ve toplam tutardan düşüldü.", "success")
    except Exception as e:
        flash(f"Hizmet kaldırılırken hata: {str(e)}", "error")
    return redirect(url_for('reservation_detail_page', reservation_id=reservation_id))

# =========================================================================
# PAYMENTS ROUTES
# =========================================================================
@app.route('/payments')
def payments_list():
    try:
        payments = bl.get_payments()
        reservations = bl.get_reservations()
        return render_template('payments.html', payments=payments, reservations=reservations, active_page='payments')
    except Exception as e:
        flash(f"Ödemeler yüklenemedi: {str(e)}", "error")
        return render_template('payments.html', payments=[], reservations=[], active_page='payments')

@app.route('/payments/add', methods=['POST'])
def payment_add():
    reservation_id = request.form.get('reservation_id')
    redirect_to = request.form.get('redirect_to', 'list')
    try:
        amount = request.form.get('payment_amount')
        method = request.form.get('payment_method')
        status = request.form.get('payment_status')
        
        bl.add_payment(reservation_id, amount, method, status)
        flash("Ödeme kaydı başarıyla eklendi.", "success")
    except Exception as e:
        flash(f"Ödeme kaydedilirken hata: {str(e)}", "error")
        
    if redirect_to == 'detail':
        return redirect(url_for('reservation_detail_page', reservation_id=reservation_id))
    return redirect(url_for('payments_list'))

@app.route('/payments/update', methods=['POST'])
def payment_update():
    payment_id = request.form.get('payment_id')
    reservation_id = request.form.get('reservation_id')
    redirect_to = request.form.get('redirect_to', 'list')
    try:
        amount = request.form.get('payment_amount')
        method = request.form.get('payment_method')
        status = request.form.get('payment_status')
        
        bl.update_payment(payment_id, reservation_id, amount, method, status)
        flash("Ödeme kaydı başarıyla güncellendi.", "success")
    except Exception as e:
        flash(f"Ödeme güncellenirken hata: {str(e)}", "error")
        
    if redirect_to == 'detail':
        return redirect(url_for('reservation_detail_page', reservation_id=reservation_id))
    return redirect(url_for('payments_list'))

@app.route('/payments/delete', methods=['POST'])
def payment_delete():
    try:
        payment_id = request.form.get('payment_id')
        bl.delete_payment(payment_id)
        flash("Ödeme kaydı başarıyla silindi.", "success")
    except Exception as e:
        flash(f"Ödeme kaydı silinirken hata: {str(e)}", "error")
    return redirect(url_for('payments_list'))

# =========================================================================
# SERVICES ROUTES
# =========================================================================
@app.route('/services')
def services_list():
    try:
        services = bl.get_services()
        return render_template('services.html', services=services, active_page='services')
    except Exception as e:
        flash(f"Hizmet listesi yüklenemedi: {str(e)}", "error")
        return render_template('services.html', services=[], active_page='services')

@app.route('/services/add', methods=['POST'])
def service_add():
    try:
        service_name = request.form.get('service_name')
        service_price = request.form.get('service_price')
        
        bl.add_service(service_name, service_price)
        flash("Yeni ek hizmet tanımlandı.", "success")
    except Exception as e:
        flash(f"Hizmet tanımlanırken hata: {str(e)}", "error")
    return redirect(url_for('services_list'))

@app.route('/services/update', methods=['POST'])
def service_update():
    try:
        service_id = request.form.get('service_id')
        service_name = request.form.get('service_name')
        service_price = request.form.get('service_price')
        
        bl.update_service(service_id, service_name, service_price)
        flash("Hizmet bilgileri güncellendi.", "success")
    except Exception as e:
        flash(f"Hizmet güncellenirken hata: {str(e)}", "error")
    return redirect(url_for('services_list'))

@app.route('/services/delete', methods=['POST'])
def service_delete():
    try:
        service_id = request.form.get('service_id')
        bl.delete_service(service_id)
        flash("Hizmet tanımı sistemden kaldırıldı.", "success")
    except Exception as e:
        flash(f"Hizmet silinemedi (bu hizmeti alan rezervasyonlar olabilir): {str(e)}", "error")
    return redirect(url_for('services_list'))

# =========================================================================
# STAFF ROUTES
# =========================================================================
@app.route('/staff')
def staff_list():
    try:
        staff = bl.get_staff()
        return render_template('staff.html', staff=staff, active_page='staff')
    except Exception as e:
        flash(f"Personel listesi yüklenemedi: {str(e)}", "error")
        return render_template('staff.html', staff=[], active_page='staff')

@app.route('/staff/add', methods=['POST'])
def staff_add():
    try:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        position = request.form.get('position')
        phone = request.form.get('phone')
        salary = request.form.get('salary')
        
        bl.add_staff(first_name, last_name, position, phone, salary)
        flash("Personel başarıyla kaydedildi.", "success")
    except Exception as e:
        flash(f"Personel kaydedilirken hata: {str(e)}", "error")
    return redirect(url_for('staff_list'))

@app.route('/staff/update', methods=['POST'])
def staff_update():
    try:
        staff_id = request.form.get('staff_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        position = request.form.get('position')
        phone = request.form.get('phone')
        salary = request.form.get('salary')
        
        bl.update_staff(staff_id, first_name, last_name, position, phone, salary)
        flash("Personel bilgileri güncellendi.", "success")
    except Exception as e:
        flash(f"Personel güncellenirken hata: {str(e)}", "error")
    return redirect(url_for('staff_list'))

@app.route('/staff/delete', methods=['POST'])
def staff_delete():
    try:
        staff_id = request.form.get('staff_id')
        bl.delete_staff(staff_id)
        flash("Personel kaydı silindi.", "success")
    except Exception as e:
        flash(f"Personel silinirken hata: {str(e)}", "error")
    return redirect(url_for('staff_list'))

# =========================================================================
# RUN APPLICATION
# =========================================================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
