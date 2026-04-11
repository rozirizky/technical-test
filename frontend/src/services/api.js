const BASE_URL = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') || ''

async function request(method, path, body = null, token = null) {
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`

  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }

  if (res.status === 204) return null
  return res.json()
}

export const api = {
  // Auth
  login: (email, password) =>
    request('POST', '/api/auth/login', { email, password }),
  logout: (token) =>
    request('POST', '/api/auth/logout', null, token),

  // Users
  getUsers: (token) => request('GET', '/users/', null, token),
  getUser: (id, token) => request('GET', `/users/${id}`, null, token),
  createUser: (data, token) => request('POST', '/users/', data, token),
  updateUser: (id, data, token) => request('PUT', `/users/${id}`, data, token),
  deleteUser: (id, token) => request('DELETE', `/users/${id}`, null, token),

  // Roles
  getRoles: (token) => request('GET', '/role/', null, token),
  createRole: (data, token) => request('POST', '/role/', data, token),
  updateRole: (id, data, token) => request('PUT', `/role/${id}`, data, token),
  deleteRole: (id, token) => request('DELETE', `/role/${id}`, null, token),

  // Locations
  getLocations: (token) => request('GET', '/location/', null, token),
  createLocation: (data, token) => request('POST', '/location/', data, token),
  updateLocation: (id, data, token) => request('PUT', `/location/${id}`, data, token),
  deleteLocation: (id, token) => request('DELETE', `/location/${id}`, null, token),

  // Vehicles
  getVehicles: (token) => request('GET', '/vehicles/', null, token),
  getVehicle: (id, token) => request('GET', `/vehicles/${id}`, null, token),
  createVehicle: (data, token) => request('POST', '/vehicles/', data, token),
  updateVehicle: (id, data, token) => request('PUT', `/vehicles/${id}`, data, token),
  deleteVehicle: (id, token) => request('DELETE', `/vehicles/${id}`, null, token),

  // Drivers
  getDrivers: (token) => request('GET', '/drivers/', null, token),
  createDriver: (data, token) => request('POST', '/drivers/', data, token),
  updateDriver: (id, data, token) => request('PUT', `/drivers/${id}`, data, token),
  deleteDriver: (id, token) => request('DELETE', `/drivers/${id}`, null, token),

  // Bookings
  getBookings: (token) => request('GET', '/bookings/', null, token),
  getBooking: (id, token) => request('GET', `/bookings/${id}`, null, token),
  createBooking: (data, token) => request('POST', '/bookings/', data, token),
  updateBooking: (id, data, token) => request('PUT', `/bookings/${id}`, data, token),
  deleteBooking: (id, token) => request('DELETE', `/bookings/${id}`, null, token),

  // Fuel Logs
  getFuelLogs: (token) => request('GET', '/fuel-logs/', null, token),
  createFuelLog: (data, token) => request('POST', '/fuel-logs/', data, token),
  updateFuelLog: (id, data, token) => request('PUT', `/fuel-logs/${id}`, data, token),
  deleteFuelLog: (id, token) => request('DELETE', `/fuel-logs/${id}`, null, token),

  // Service Schedules
  getServiceSchedules: (token) => request('GET', '/service-schedules/', null, token),
  createServiceSchedule: (data, token) => request('POST', '/service-schedules/', data, token),

  // Health
  getHealth: () => request('GET', '/health'),
}
