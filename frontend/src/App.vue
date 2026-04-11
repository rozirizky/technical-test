<script setup>
import { ref, computed } from 'vue'
import { auth } from './store/auth.js'
import { api } from './services/api.js'
import LoginForm from './components/LoginForm.vue'
import Dashboard from './components/Dashboard.vue'
import CrudTable from './components/CrudTable.vue'

const currentTab = ref('dashboard')

const views = {
  vehicles: {
    title: 'Kendaraan', icon: 'directions_car',
    columns: [
      { key: 'id',             label: 'ID' },
      { key: 'plate_number',   label: 'Plat Nomor' },
      { key: 'brand',          label: 'Merek' },
      { key: 'model',          label: 'Model' },
      { key: 'year',           label: 'Tahun' },
      { key: 'ownership_type', label: 'Kepemilikan' },
      { key: 'status',         label: 'Status' },
    ],
    formFields: [
      { key: 'plate_number',   label: 'Plat Nomor' },
      { key: 'brand',          label: 'Merek' },
      { key: 'model',          label: 'Model' },
      { key: 'type',           label: 'Tipe Kendaraan' },
      { key: 'year',           label: 'Tahun', type: 'number' },
      { key: 'ownership_type', label: 'Kepemilikan (dinas/sewa)' },
      { key: 'status',         label: 'Status' },
    ],
    fetchFn:  () => api.getVehicles(auth.token),
    createFn: (d) => api.createVehicle(d, auth.token),
    updateFn: (id, d) => api.updateVehicle(id, d, auth.token),
    deleteFn: (id) => api.deleteVehicle(id, auth.token),
  },
  drivers: {
    title: 'Pengemudi', icon: 'person',
    columns: [
      { key: 'id',             label: 'ID' },
      { key: 'user_id',        label: 'ID Pengguna' },
      { key: 'license_number', label: 'No. SIM' },
      { key: 'license_type',   label: 'Tipe SIM' },
      { key: 'license_expiry', label: 'Exp. SIM' },
      { key: 'status',         label: 'Status' },
    ],
    formFields: [
      { key: 'user_id',        label: 'ID Pengguna', type: 'number' },
      { key: 'vehicle_id',     label: 'ID Kendaraan', type: 'number' },
      { key: 'license_number', label: 'Nomor SIM' },
      { key: 'license_type',   label: 'Tipe SIM (A/B1/B2)' },
      { key: 'license_expiry', label: 'Tanggal Expired SIM', type: 'date' },
    ],
    fetchFn:  () => api.getDrivers(auth.token),
    createFn: (d) => api.createDriver(d, auth.token),
    updateFn: (id, d) => api.updateDriver(id, d, auth.token),
    deleteFn: (id) => api.deleteDriver(id, auth.token),
  },
  bookings: {
    title: 'Peminjaman', icon: 'assignment',
    columns: [
      { key: 'id',                 label: 'ID' },
      { key: 'booking_code',       label: 'Kode' },
      { key: 'requester_id',       label: 'Pemohon' },
      { key: 'vehicle_id',         label: 'Kendaraan' },
      { key: 'departure_datetime', label: 'Berangkat' },
      { key: 'return_datetime',    label: 'Kembali' },
      { key: 'status',             label: 'Status' },
    ],
    formFields: [
      { key: 'booking_code',       label: 'Kode Peminjaman' },
      { key: 'requester_id',       label: 'ID Pemohon', type: 'number' },
      { key: 'vehicle_id',         label: 'ID Kendaraan', type: 'number' },
      { key: 'driver_id',          label: 'ID Pengemudi', type: 'number' },
      { key: 'departure_datetime', label: 'Waktu Berangkat', type: 'datetime-local' },
      { key: 'return_datetime',    label: 'Waktu Kembali', type: 'datetime-local' },
      { key: 'purpose',            label: 'Tujuan Perjalanan' },
      { key: 'destination',        label: 'Destinasi' },
      { key: 'passenger_count',    label: 'Jumlah Penumpang', type: 'number' },
    ],
    fetchFn:  () => api.getBookings(auth.token),
    createFn: (d) => api.createBooking(d, auth.token),
    updateFn: (id, d) => api.updateBooking(id, d, auth.token),
    deleteFn: (id) => api.deleteBooking(id, auth.token),
  },
  users: {
    title: 'Pengguna', icon: 'group',
    columns: [
      { key: 'id',        label: 'ID' },
      { key: 'name',      label: 'Nama' },
      { key: 'email',     label: 'Email' },
      { key: 'role.name', label: 'Role' },
    ],
    formFields: [
      { key: 'name',     label: 'Nama Lengkap' },
      { key: 'email',    label: 'Email', type: 'email' },
      { key: 'password', label: 'Password', type: 'password' },
      { key: 'role_id',  label: 'ID Role', type: 'number' },
    ],
    fetchFn:  () => api.getUsers(auth.token),
    createFn: (d) => api.createUser(d, auth.token),
    updateFn: (id, d) => api.updateUser(id, d, auth.token),
    deleteFn: (id) => api.deleteUser(id, auth.token),
  },
  locations: {
    title: 'Lokasi', icon: 'place',
    columns: [
      { key: 'id',      label: 'ID' },
      { key: 'name',    label: 'Nama Lokasi' },
      { key: 'type',    label: 'Tipe' },
      { key: 'address', label: 'Alamat' },
      { key: 'region',  label: 'Wilayah' },
    ],
    formFields: [
      { key: 'name',    label: 'Nama Lokasi' },
      { key: 'type',    label: 'Tipe Lokasi' },
      { key: 'address', label: 'Alamat' },
      { key: 'region',  label: 'Wilayah' },
    ],
    fetchFn:  () => api.getLocations(auth.token),
    createFn: (d) => api.createLocation(d, auth.token),
    updateFn: (id, d) => api.updateLocation(id, d, auth.token),
    deleteFn: (id) => api.deleteLocation(id, auth.token),
  },
  fuellogs: {
    title: 'Log Bahan Bakar', icon: 'local_gas_station',
    columns: [
      { key: 'id',         label: 'ID' },
      { key: 'vehicle_id', label: 'Kendaraan' },
      { key: 'log_date',   label: 'Tanggal' },
      { key: 'liters',     label: 'Liter' },
      { key: 'odometer',   label: 'Odometer' },
    ],
    formFields: [
      { key: 'vehicle_id', label: 'ID Kendaraan', type: 'number' },
      { key: 'booking_id', label: 'ID Booking', type: 'number' },
      { key: 'liters',     label: 'Jumlah Liter', type: 'number' },
      { key: 'odometer',   label: 'Odometer (km)', type: 'number' },
      { key: 'log_date',   label: 'Tanggal', type: 'date' },
    ],
    fetchFn:  () => api.getFuelLogs(auth.token),
    createFn: (d) => api.createFuelLog(d, auth.token),
    updateFn: (id, d) => api.updateFuelLog(id, d, auth.token),
    deleteFn: (id) => api.deleteFuelLog(id, auth.token),
  },
}

const currentView = computed(() => views[currentTab.value])
</script>

<template>
  <div>
    <!-- Not logged in -->
    <LoginForm v-if="!auth.isLoggedIn" @login-success="currentTab = 'dashboard'" />

    <!-- Logged in - Dashboard -->
    <Dashboard
      v-else-if="currentTab === 'dashboard'"
      @logout="currentTab = 'dashboard'"
      @navigate="(tab) => currentTab = tab"
    />

    <!-- Logged in - CRUD views -->
    <div v-else-if="currentView" class="crud-body">
      <CrudTable
        :title="currentView.title"
        :icon="currentView.icon"
        :columns="currentView.columns"
        :form-fields="currentView.formFields"
        :fetch-fn="currentView.fetchFn"
        :create-fn="currentView.createFn"
        :update-fn="currentView.updateFn"
        :delete-fn="currentView.deleteFn"
        @back="currentTab = 'dashboard'"
      />
    </div>
  </div>
</template>

<style>
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Source Sans Pro', sans-serif; background: #f5f5f5; }
.crud-body { max-width: 1200px; margin: 0 auto; padding: 2rem 1.5rem; }
</style>
