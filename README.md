# Otel Rezervasyon Sistemi (Hotel Reservation Management System)

Bu proje, veritabanı yönetim sistemleri dersi final projesi kapsamında geliştirilmiş, **N-Katmanlı Mimari (N-Tier Architecture)** prensiplerine ve **Stored Procedure (Saklı Yordam) Kısıtlamalarına** sahip eksiksiz bir otel rezervasyon yönetim sistemidir.

---

## 🛠️ Teknolojik Altyapı ve Katmanlı Mimari

Proje, temiz kod ve modülerlik ilkelerine bağlı olarak **3 Katmanlı (N-Tier) Mimari** mimarisinde yapılandırılmıştır:

1. **Sunum Katmanı (Presentation Layer - UI)**
   - **Teknolojiler:** HTML5, CSS3 (Modern Özel Tasarım), Bootstrap 5, FontAwesome 6, JavaScript (Ajax / Fetch API).
   - **Görevi:** Kullanıcı arayüzünü sunar ve verileri dinamik olarak görselleştirir. Kullanıcıdan alınan form verilerini doğrudan veritabanına göndermek yerine İş Mantığı Katmanı'na (BL) iletir.

2. **İş Mantığı Katmanı (Business Layer - BL)**
   - **Dosya Konumu:** `BL/hotel_bl.py`
   - **Görevi:** Giriş parametrelerinin geçerlilik kontrolünü (Email formatı, telefon uzunluğu, tarih kısıtlamaları) yapar. Rezervasyon tarihlerinin çakışıp çakışmadığını (Çift rezervasyon kontrolü) denetler. SQL Fonksiyonlarını dolaylı olarak çağırarak oda maliyeti hesaplaması yapar.

3. **Veri Erişim Katmanı (Data Access Layer - DAL)**
   - **Dosya Konumu:** `DAL/db_manager.py`
   - **Görevi:** Veritabanı bağlantılarını yönetir. **KRİTİK KURAL:** Uygulama içerisinde hiçbir yerde ham SQL komutu (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) çalıştırılmaz. Tüm veri erişimleri `cursor.callproc()` metodu ile sadece stored procedure'ler üzerinden gerçekleştirilir.

---

## 📊 Entity Relationship (ER) Diyagramı

Aşağıdaki Mermaid diyagramı veritabanındaki tabloları, birincil (PK) ve yabancı anahtarları (FK) ve ilişkisel kardinaliteleri göstermektedir:

```mermaid
erDiagram
    Customers ||--o{ Reservations : "yapar"
    RoomTypes ||--o{ Rooms : "tanımlar"
    Rooms ||--o{ Reservations : "tahsis_edilir"
    Reservations ||--o{ Payments : "odemesidir"
    Reservations ||--o{ ReservationServices : "icerir"
    Services ||--o{ ReservationServices : "saglanir"

    Customers {
        int customer_id PK
        string first_name
        string last_name
        string phone UNIQUE
        string email UNIQUE
        string passport_no UNIQUE
        datetime registration_date
    }

    RoomTypes {
        int room_type_id PK
        string type_name UNIQUE
        decimal price_per_night
        int capacity
    }

    Rooms {
        int room_id PK
        string room_number UNIQUE
        int room_type_id FK
        int floor_number
        string room_status
    }

    Reservations {
        int reservation_id PK
        int customer_id FK
        int room_id FK
        date check_in_date
        date check_out_date
        string reservation_status
        decimal total_price
    }

    Payments {
        int payment_id PK
        int reservation_id FK
        datetime payment_date
        decimal payment_amount
        string payment_method
        string payment_status
    }

    Services {
        int service_id PK
        string service_name UNIQUE
        decimal service_price
    }

    ReservationServices {
        int reservation_service_id PK
        int reservation_id FK
        int service_id FK
        int quantity
    }

    Staff {
        int staff_id PK
        string first_name
        string last_name
        string position
        string phone UNIQUE
        decimal salary
    }
```

---

## 💾 Veritabanı Mimarisi & SQL Nesneleri

Veritabanı ilişkileri ve kısıtlamaları `database/init.sql` dosyasında tanımlanmıştır.

### 1. SQL Fonksiyonları
*   `fn_CalculateStayDays(check_in, check_out)`: İki tarih arasındaki toplam gün sayısını (`DATEDIFF`) hesaplar.
*   `fn_CalculateReservationCost(room_id, check_in, check_out)`: Belirtilen odanın gecelik fiyatı ile konaklama süresini çarparak toplam oda tutarını döndürür.

### 2. SQL Tetikleyicileri (Triggers)
*   `trg_AfterReservationInsert`: Yeni bir rezervasyon eklendiğinde, ilgili odanın durumunu otomatik olarak `'Reserved'` (Rezerve) yapar.
*   `trg_AfterReservationUpdate`: Rezervasyon durumu `'Cancelled'` (İptal) olarak güncellendiğinde, odanın durumunu otomatik olarak `'Available'` (Boş) durumuna çeker.

### 3. Stored Procedure Listesi (Saklı Yordamlar)
*   **Customers:** `sp_AddCustomer`, `sp_UpdateCustomer`, `sp_DeleteCustomer`, `sp_GetCustomers`, `sp_GetCustomerById`
*   **Rooms:** `sp_AddRoom`, `sp_UpdateRoom`, `sp_DeleteRoom`, `sp_GetRooms`, `sp_GetRoomById`
*   **RoomTypes:** `sp_AddRoomType`, `sp_UpdateRoomType`, `sp_DeleteRoomType`, `sp_GetRoomTypes`, `sp_GetRoomTypeById`
*   **Reservations:** `sp_AddReservation`, `sp_UpdateReservation`, `sp_DeleteReservation`, `sp_GetReservations`, `sp_GetReservationById`, `sp_CancelReservation`, `sp_CheckRoomAvailability`, `sp_GetCalculatedCost`
*   **Payments:** `sp_AddPayment`, `sp_UpdatePayment`, `sp_DeletePayment`, `sp_GetPayments`, `sp_GetPaymentById`, `sp_GetPaymentsByReservation`
*   **Services:** `sp_AddService`, `sp_UpdateService`, `sp_DeleteService`, `sp_GetServices`, `sp_GetServiceById`
*   **ReservationServices:** `sp_AddReservationService`, `sp_UpdateReservationService`, `sp_DeleteReservationService`, `sp_GetReservationServices`, `sp_GetReservationServicesByReservation`
*   **Staff:** `sp_AddStaff`, `sp_UpdateStaff`, `sp_DeleteStaff`, `sp_GetStaff`, `sp_GetStaffById`
*   **Dashboard Stats:** `sp_GetDashboardStats`

---

## 🚀 Projeyi Çalıştırma Adımları

### Gereksinimler
*   Python 3.8 veya üzeri
*   MySQL Server (XAMPP önerilir)

### Adım 1: Bağımlılıkları Yükleyin
Terminalde proje klasöründeyken aşağıdaki paketi yükleyin:
```bash
pip install mysql-connector-python flask
```

### Adım 2: Veritabanını Kurun
MySQL sunucunuzu başlatın (XAMPP Control Panel -> MySQL Start).
Aşağıdaki komutu çalıştırarak veritabanını, tabloları, seed verileri, tetikleyicileri ve stored procedure'leri kurun:
```powershell
# Windows PowerShell ile:
Get-Content database/init.sql | C:/xampp/mysql/bin/mysql.exe -u root
```
*(Eğer mysql.exe farklı bir dizindeyse kendi yolunuza göre güncelleyebilirsiniz).*

### Adım 3: Uygulamayı Başlatın
Aşağıdaki komutla Flask uygulamasını lokal sunucuda başlatın:
```bash
python app.py
```
Açılan lokal sunucu adresine tarayıcıdan gidin: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🖥️ Arayüz Özellikleri
*   **İnteraktif Dashboard:** Toplam kazanç, oda doluluğu ve müşteri sayılarını dinamik kartlarla özetler.
*   **Dinamik Rezervasyon Ekranı:** Giriş-çıkış tarihleri ve oda seçildiğinde, sayfa yenilenmeden veritabanı fonksiyonu (`fn_CalculateReservationCost`) tetiklenerek anlık konaklama bedeli yansıtılır.
*   **Rezervasyon Detay Sayfası:** Tek bir panelden müşteriye ek hizmet ekleme (Airport transfer, kahvaltı vb.) ve ödeme alma işlemleri yapılabilir. Hizmet eklendiğinde veya silindiğinde toplam fiyat otomatik güncellenir.
