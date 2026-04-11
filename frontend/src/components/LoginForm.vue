<script setup>
import { ref } from 'vue'
import { api } from '../services/api.js'
import { auth } from '../store/auth.js'

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const emit = defineEmits(['login-success'])

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    const res = await api.login(email.value, password.value)
    auth.login(res.access_token, { email: email.value })
    emit('login-success')
  } catch (e) {
    error.value = e.message || 'Login gagal. Periksa email dan password.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-wrap">
    <VaCard class="login-card">
      <VaCardTitle>
        <div class="login-title">
          <VaIcon name="directions_car" size="2rem" color="primary" />
          <span>Peminjaman Kendaraan</span>
        </div>
      </VaCardTitle>
      <VaCardContent>
        <p class="login-sub">Masuk ke sistem manajemen kendaraan</p>
        <VaInput
          v-model="email"
          label="Email"
          type="email"
          class="mb-4"
          placeholder="admin@example.com"
          @keyup.enter="handleLogin"
        />
        <VaInput
          v-model="password"
          label="Password"
          type="password"
          class="mb-4"
          placeholder="••••••••"
          @keyup.enter="handleLogin"
        />
        <VaAlert v-if="error" color="danger" class="mb-4">{{ error }}</VaAlert>
        <VaButton
          :loading="loading"
          @click="handleLogin"
          block
          color="primary"
        >
          Masuk
        </VaButton>
      </VaCardContent>
    </VaCard>
  </div>
</template>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a237e 0%, #0d47a1 50%, #1565c0 100%);
}
.login-card {
  width: 100%;
  max-width: 400px;
  margin: 1rem;
}
.login-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
}
.login-sub {
  color: #666;
  margin-bottom: 1.5rem;
}
</style>
