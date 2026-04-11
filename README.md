# Sistem Peminjaman Kendaraan

Aplikasi manajemen peminjaman kendaraan berbasis microservices dengan frontend Vue 3.

## Arsitektur

```
                        ┌─────────────────┐
                        │   Browser/Client │
                        └────────┬────────┘
                                 │ :80
                        ┌────────▼────────┐
                        │      Nginx      │  ← Reverse Proxy
                        └──┬──────────┬──┘
                           │          │
               ┌───────────▼──┐  ┌────▼────────┐
               │  API Gateway │  │  Frontend   │  Vue 3 + Vuestic UI
               │   :8000      │  │  :3000      │
               └──┬───────────┘  └─────────────┘
                  │
     ┌────────────┼─────────────┬──────────────┐
     │            │             │              │
┌────▼────┐ ┌────▼────┐ ┌─────▼────┐ ┌───────▼───────┐
│  User   │ │Vehicle  │ │ Booking  │ │  Operational  │
│ Service │ │ Service │ │ Service  │ │    Service    │
│  :8000  │ │  :8000  │ │  :8000   │ │    :8000      │
└────┬────┘ └────┬────┘ └─────┬────┘ └───────┬───────┘
     │            │             │              │
┌────▼────┐ ┌────▼────┐ ┌─────▼────┐ ┌───────▼───────┐
│ user-db │ │vehicle- │ │booking-  │ │operational-   │
│(Postgres│ │   db    │ │   db     │ │     db        │
└─────────┘ └─────────┘ └──────────┘ └───────────────┘
                        Redis (shared)
```

## Layanan & Endpoint

| Layanan              | Prefix                               | Deskripsi                        |
|----------------------|--------------------------------------|----------------------------------|
| User Service         | `/users/`, `/role/`, `/location/`    | Manajemen pengguna & autentikasi |
| Vehicle Service      | `/vehicles/`, `/drivers/`            | Manajemen kendaraan & pengemudi  |
| Booking Service      | `/bookings/`                         | Peminjaman & persetujuan         |
| Operational Service  | `/fuel-logs/`, `/service-schedules/` | Log operasional kendaraan        |

## Cara Menjalankan

### Prasyarat
- Docker Desktop (atau Docker Engine + Docker Compose plugin)
- Port 80 tidak dipakai proses lain

### Langkah

```bash
# 1. Masuk ke direktori project
cd kendaraan-app

# 2. Salin file environment (sudah ada .env default)
cp .env.example .env

# 3. Edit .env jika perlu (ganti JWT_SECRET di production!)
# DB_PASSWORD=airflow
# JWT_SECRET=ganti_dengan_secret_kuat_min_32_karakter

# 4. Jalankan semua services
docker compose up -d --build

# 5. Cek status
docker compose ps
```

### Akses Aplikasi

| URL                          | Keterangan                      |
|------------------------------|---------------------------------|
| http://localhost             | Frontend (Vue 3)                |
| http://localhost/health      | Status semua microservice       |
| http://localhost/users/      | API Users                       |
| http://localhost/vehicles/   | API Kendaraan                   |
| http://localhost/bookings/   | API Peminjaman                  |

### Login

Buat user pertama via API (user service belum ada seeder):

```bash
# Buat role dulu
curl -X POST http://localhost/role/ \
  -H "Content-Type: application/json" \
  -d '{"name": "admin"}'

# Buat user pertama
curl -X POST http://localhost/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Admin", "email": "admin@example.com", "password": "admin123", "role_id": 1}'

# Login
curl -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'
```

## Perintah Berguna

```bash
# Lihat log semua service
docker compose logs -f

# Lihat log service tertentu
docker compose logs -f user-service
docker compose logs -f api-gateway

# Restart satu service
docker compose restart user-service

# Stop semua
docker compose down

# Stop dan hapus volume (reset database)
docker compose down -v

# Rebuild satu service setelah perubahan kode
docker compose up -d --build user-service
```

## Struktur Direktori

```
kendaraan-app/
├── .env                        ← Konfigurasi environment (jangan di-commit)
├── .env.example                ← Template environment
├── docker-compose.yml          ← Orkestrasi semua services
├── nginx/
│   └── nginx.conf              ← Reverse proxy config
├── frontend/                   ← Vue 3 + Vuestic UI
│   ├── Dockerfile
│   ├── src/
│   │   ├── App.vue             ← Root component + routing
│   │   ├── main.js
│   │   ├── services/
│   │   │   └── api.js          ← HTTP client ke backend
│   │   ├── store/
│   │   │   └── auth.js         ← State autentikasi
│   │   └── components/
│   │       ├── LoginForm.vue
│   │       ├── Dashboard.vue
│   │       └── CrudTable.vue   ← Tabel CRUD generik
│   └── ...
└── services/
    ├── api-gateway/            ← FastAPI gateway (port 8000 internal)
    ├── user_service/           ← Auth, User, Role, Location
    ├── vehicle_service/        ← Vehicle, Driver
    ├── booking_service/        ← Booking, Approval
    └── operational_service/    ← FuelLog, ServiceSchedule, ServiceHistory
```

## Troubleshooting

**Service tidak mau start:**
```bash
docker compose logs <nama-service>
```

**Database connection refused:**
```bash
# Pastikan DB sudah healthy sebelum service start
docker compose ps
# Jika perlu, restart service yang gagal
docker compose restart user-service
```

**Port 80 sudah dipakai:**
Ganti di `docker-compose.yml`:
```yaml
nginx:
  ports:
    - "8080:80"   # ganti 8080 dengan port yang tersedia
```
Lalu akses di http://localhost:8080

**Reset ulang semua data:**
```bash
docker compose down -v
docker compose up -d --build
```
