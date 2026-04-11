<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  title: String,
  icon: String,
  columns: Array,   // [{ key, label, render? }]
  fetchFn: Function,
  createFn: Function,
  updateFn: Function,
  deleteFn: Function,
  formFields: Array, // [{ key, label, type }]
})

const emit = defineEmits(['back'])

const items = ref([])
const loading = ref(false)
const error = ref('')
const showForm = ref(false)
const editItem = ref(null)
const formData = ref({})
const saving = ref(false)

// Mendukung nested key seperti "role.name"
function getNestedValue(obj, key) {
  return key.split('.').reduce((o, k) => (o != null ? o[k] : null), obj)
}

async function loadItems() {
  loading.value = true
  error.value = ''
  try {
    items.value = await props.fetchFn()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editItem.value = null
  formData.value = {}
  showForm.value = true
}

function openEdit(item) {
  editItem.value = item
  formData.value = { ...item }
  showForm.value = true
}

async function saveItem() {
  saving.value = true
  try {
    if (editItem.value) {
      await props.updateFn(editItem.value.id, formData.value)
    } else {
      await props.createFn(formData.value)
    }
    showForm.value = false
    await loadItems()
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}

async function deleteItem(item) {
  if (!confirm(`Hapus item ini?`)) return
  try {
    await props.deleteFn(item.id)
    await loadItems()
  } catch (e) {
    error.value = e.message
  }
}

onMounted(loadItems)
</script>

<template>
  <div>
    <!-- Header -->
    <div class="page-header">
      <VaButton flat icon="arrow_back" @click="$emit('back')" />
      <VaIcon :name="icon" size="1.5rem" color="primary" />
      <h2 class="page-title">{{ title }}</h2>
      <VaButton icon="add" @click="openCreate" color="primary" class="ml-auto">
        Tambah
      </VaButton>
    </div>

    <VaAlert v-if="error" color="danger" class="mb-4" closeable @close="error=''">{{ error }}</VaAlert>

    <!-- Table -->
    <VaCard>
      <VaCardContent>
        <div v-if="loading" class="loading-center">
          <VaProgressCircle indeterminate size="3rem" />
        </div>
        <div v-else-if="items.length === 0" class="empty-state">
          <VaIcon name="inbox" size="3rem" color="secondary" />
          <p>Belum ada data</p>
        </div>
        <div v-else class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in items" :key="item.id">
                <td v-for="col in columns" :key="col.key">
                  {{ getNestedValue(item, col.key) ?? '—' }}
                </td>
                <td class="action-cell">
                  <VaButton flat icon="edit" size="small" @click="openEdit(item)" />
                  <VaButton flat icon="delete" size="small" color="danger" @click="deleteItem(item)" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </VaCardContent>
    </VaCard>

    <!-- Modal Form -->
    <VaModal v-model="showForm" :title="editItem ? 'Edit ' + title : 'Tambah ' + title" ok-text="Simpan" cancel-text="Batal" @ok="saveItem" :ok-loading="saving">
      <div class="form-grid">
        <div v-for="field in formFields" :key="field.key">
          <VaInput
            v-if="field.type !== 'select'"
            v-model="formData[field.key]"
            :label="field.label"
            :type="field.type || 'text'"
            class="mb-3"
          />
          <VaSelect
            v-else
            v-model="formData[field.key]"
            :label="field.label"
            :options="field.options"
            class="mb-3"
          />
        </div>
      </div>
    </VaModal>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem; }
.page-title  { font-size: 1.25rem; font-weight: 600; }
.ml-auto     { margin-left: auto; }
.mb-4        { margin-bottom: 1rem; }
.mb-3        { margin-bottom: 0.75rem; }

.loading-center { display: flex; justify-content: center; padding: 3rem; }
.empty-state { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; padding: 3rem; color: #888; }

.table-wrap { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.data-table th { text-align: left; padding: 0.75rem 1rem; background: #f5f5f5; font-weight: 600; color: #444; border-bottom: 2px solid #e0e0e0; white-space: nowrap; }
.data-table td { padding: 0.75rem 1rem; border-bottom: 1px solid #f0f0f0; }
.data-table tr:hover td { background: #fafafa; }
.action-cell { white-space: nowrap; }

.form-grid { display: flex; flex-direction: column; min-width: 320px; }
</style>
