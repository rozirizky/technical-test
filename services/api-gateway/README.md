# API Gateway — Peminjaman Kendaraan

Reverse proxy ringan berbasis FastAPI. Meneruskan request dari satu base URL ke masing-masing service.

## Struktur folder

```
./
├── run_all.py           ← jalankan SEMUA service sekaligus dari sini
├── api-gateway/
│   ├── main.py
│   └── requirements.txt
├── user-service/
├── booking-service/
└── operational-service/
```

## Cara pakai

### 1. Install dependencies gateway
```bash
cd api-gateway
pip install -r requirements.txt
```

### 2. Jalankan semua sekaligus (dari folder root)
```bash
python run_all.py
```

### 3. Atau jalankan manual satu per satu
```bash
# Terminal 1
cd user-service && uvicorn app.main:app --port 8001 --reload

# Terminal 2
cd booking-service && uvicorn app.main:app --port 8002 --reload

# Terminal 3
cd operational-service && uvicorn app.main:app --port 8003 --reload

# Terminal 4 (gateway)
cd api-gateway && uvicorn main:app --port 8000 --reload
```

## Routing

| Prefix                  | Service              | Port |
|-------------------------|----------------------|------|
| `/users`                | user-service         | 8001 |
| `/role`                 | user-service         | 8001 |
| `/location`             | user-service         | 8001 |
| `/bookings`             | booking-service      | 8002 |
| `/fuel-logs`            | operational-service  | 8003 |
| `/service-schedules`    | operational-service  | 8003 |
| `/service-histories`    | operational-service  | 8003 |
| `/usage-logs`           | operational-service  | 8003 |

## Endpoints khusus gateway

| Endpoint          | Keterangan                              |
|-------------------|-----------------------------------------|
| `GET /`           | Info gateway + daftar prefix terdaftar  |
| `GET /health`     | Cek status semua service (up/down)      |

## Contoh request via gateway

```bash
# Semua request cukup ke port 8000
curl http://localhost:8000/users/
curl http://localhost:8000/bookings/
curl http://localhost:8000/fuel-logs/

# Health check
curl http://localhost:8000/health
```

## Menambah service baru

Edit `SERVICES` di `api-gateway/main.py`:

```python
SERVICES: dict[str, str] = {
    ...
    "/vehicles": "http://localhost:8004",   # tambah baris ini
}
```

Lalu tambahkan juga di `run_all.py`:

```python
SERVICES = [
    ...
    {
        "name":   "vehicle-service",
        "dir":    "vehicle-service",
        "module": "app.main:app",
        "port":   8004,
    },
]
```
