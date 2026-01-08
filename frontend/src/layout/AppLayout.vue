<!-- layouts/MainLayout.vue -->
<script setup lang="ts">
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import emitter from '@/utils/bus'

const toast = useToast()
const confirm = useConfirm()

emitter.on('toast:response', (data: any) => {
  toast.add(data)
})

emitter.on('toast', (data: any) => {
  toast.add(data)
})

emitter.on('confirm', (data: any) => {
  confirm.require({
    message: data.message,
    header: data.title,
    icon: 'pi pi-exclamation-triangle',
    rejectLabel: '取消',
    acceptLabel: '确认',
    accept: data.onConfirm,
    reject: data.onCancel,
  })
})
</script>

<template>
  <Toast />
  <ConfirmDialog />
  <router-view />
</template>
