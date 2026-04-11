<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../services/api.js'
import { auth } from '../store/auth.js'

const stats = ref({ vehicles: 0, drivers: 0, bookings: 0, users: 0 })
const health = ref({})
const loading = ref(true)

const emit = defineEmits(['logout'])

async function loadStats() {
  try {
    const [vehicles, drivers, bookings, users] = await Promise.allSettled([
      api.getVehicles(auth.token),
      api.getDrivers(auth.token),
      api.getBookings(auth.token),
      api.getUsers(auth.token),
    ])
    stats.value = {
      vehicles: vehicles.value?.length ?? '—',
      drivers:  drivers.value?.length  ?? '—',
      bookings: bookings.value?.length ?? '—',
      users:    users.value?.length    ?? '—',
    }
    health.value = await api.getHealth().catch(() => ({}))
  } finally {
    loading.value = false
  }
}

function handleLogout() {
  auth.logout()
  emit('logout')
}

onMounted(loadStats)
</script>

<template>
  <div>
    <VaNavbar color="primary" class="mb-6">
      <template #left>
        <VaIcon name="directions_car" size="1.75rem" />
        <span class="nav-title">Peminjaman Kendaraan</span>
      </template>
      <template #right>
        <span class="nav-user">{{ auth.user?.email }}</span>
        <VaButton flat color="textInverted" @click="handleLogout">Keluar</VaButton>
      </template>
    </VaNavbar>

    <div class="dashboard-body">
      <h2 class="section-title">Dashboard</h2>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <VaCard v-for="item in [
          { label: 'Kendaraan', value: stats.vehicles, icon: 'directions_car', color: '#1565c0' },
          { label: 'Pengemudi', value: stats.drivers,  icon: 'person',         color: '#2e7d32' },
          { label: 'Peminjaman', value: stats.bookings, icon: 'assignment',    color: '#e65100' },
          { label: 'Pengguna',  value: stats.users,    icon: 'group',          color: '#6a1b9a' },
        ]" :key="item.label" class="stat-card">
          <VaCardContent>
            <div class="stat-inner">
              <div class="stat-icon" :style="{ background: item.color }">
                <VaIcon :name="item.icon" color="white" size="1.5rem" />
              </div>
              <div>
                <div class="stat-value">
                  <VaProgressCircle v-if="loading" indeterminate size="1.5rem" />
                  <span v-else>{{ item.value }}</span>
                </div>
                <div class="stat-label">{{ item.label }}</div>
              </div>
            </div>
          </VaCardContent>
        </VaCard>
      </div>

      <!-- Service Health -->
      <h2 class="section-title mt-8">Status Layanan</h2>
      <VaCard>
        <VaCardContent>
          <div v-if="Object.keys(health).length === 0" class="health-empty">
            <VaProgressCircle indeterminate size="2rem" />
            <span>Memeriksa status layanan...</span>
          </div>
          <div v-else class="health-grid">
            <div
              v-for="(info, url) in health"
              :key="url"
              class="health-item"
            >
              <VaBadge
                :color="info.status === 'up' ? 'success' : 'danger'"
                :text="info.status === 'up' ? 'UP' : 'DOWN'"
              />
              <span class="health-url">{{ url.replace('http://', '').replace(':8000', '') }}</span>
            </div>
          </div>
        </VaCardContent>
      </VaCard>

      <!-- Quick Links -->
      <h2 class="section-title mt-8">Akses Cepat</h2>
      <div class="menu-grid">
        <VaCard
          v-for="item in [
            { label: 'Kendaraan',   icon: 'directions_car',  tab: 'vehicles'   },
            { label: 'Pengemudi',   icon: 'person',          tab: 'drivers'    },
            { label: 'Peminjaman',  icon: 'assignment',      tab: 'bookings'   },
            { label: 'Pengguna',    icon: 'group',           tab: 'users'      },
            { label: 'Lokasi',      icon: 'place',           tab: 'locations'  },
            { label: 'Bahan Bakar', icon: 'local_gas_station', tab: 'fuellogs' },
          ]"
          :key="item.tab"
          class="menu-card"
          @click="$emit('navigate', item.tab)"
          style="cursor:pointer"
        >
          <VaCardContent class="menu-item">
            <VaIcon :name="item.icon" size="2rem" color="primary" />
            <span>{{ item.label }}</span>
          </VaCardContent>
        </VaCard>
      </div>
    </div>
  </div>
</template>

<style scoped>
.nav-title { font-size: 1.1rem; font-weight: 700; margin-left: 0.5rem; }
.nav-user  { margin-right: 1rem; font-size: 0.9rem; opacity: 0.85; }
.dashboard-body { max-width: 1200px; margin: 0 auto; padding: 0 1.5rem 3rem; }
.section-title { font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem; color: #333; }
.mt-8 { margin-top: 2rem; }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}
.stat-inner { display: flex; align-items: center; gap: 1rem; }
.stat-icon { width: 3rem; height: 3rem; border-radius: 0.75rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.stat-value { font-size: 2rem; font-weight: 700; line-height: 1; }
.stat-label { font-size: 0.85rem; color: #666; margin-top: 0.25rem; }

.health-empty { display: flex; align-items: center; gap: 1rem; color: #666; }
.health-grid { display: flex; flex-wrap: wrap; gap: 1rem; }
.health-item { display: flex; align-items: center; gap: 0.5rem; background: #f5f5f5; padding: 0.5rem 1rem; border-radius: 0.5rem; }
.health-url { font-size: 0.85rem; font-weight: 500; }

.menu-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 1rem; }
.menu-item { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; padding: 1.5rem 1rem; font-weight: 500; }
.menu-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.12); transform: translateY(-2px); transition: all 0.2s; }
</style>
