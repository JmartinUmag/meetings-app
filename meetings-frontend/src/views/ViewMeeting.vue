<template>
  <div class="container mt-4">
    <h1 class="page-title">Detalles de Reunión</h1>

    <div class="columns">
      <div class="column is-one-quarter has-text-right">
        <strong>Título</strong>
      </div>
      <div class="column">
        {{ meeting.title }}
      </div>
    </div>

    <div class="columns">
      <div class="column is-one-quarter has-text-right">
        <strong>Fecha / Hora</strong>
      </div>
      <div class="column">
        {{ formattedDateTime }}
      </div>
    </div>

    <div class="columns">
      <div class="column is-one-quarter has-text-right">
        <strong>Lugar</strong>
      </div>
      <div class="column">
        {{ meeting.place }}
      </div>
    </div>

    <div class="columns">
      <div class="column is-one-quarter has-text-right">
        <strong>Asistentes</strong>
      </div>
      <div class="column">
        <ul>
          <li v-for="assistant in meeting.assistants" :key="assistant.id">
            {{ assistant.fullname }}
          </li>
        </ul>
      </div>
    </div>

    <div class="columns">
      <div class="column is-one-quarter has-text-right">
        <strong>Resumen</strong>
      </div>
      <div class="column">
        <span style="white-space: pre">{{ meeting.summary }}</span>
      </div>
    </div>

    <div class="columns">
      <div class="column is-one-quarter has-text-right">
        <strong>Detalles</strong>
      </div>
      <div class="column">
        <span style="white-space: pre">{{ meeting.details }}</span>
      </div>
    </div>

    <div class="columns">
      <div class="column is-one-quarter has-text-right">
        <strong>Archivos</strong>
      </div>
      <div class="column">
        <div v-for="file in meeting.files" :key="file.id" class="tags mb-0">
          <a :href="formatFileUrl(file.path)" target="_blank">
            <span class="tag is-info">
              <o-icon icon="file" size="small" class="mr-1" /> {{ file.name }}
            </span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { useRoute } from 'vue-router'
  import { Meeting } from '@/interfaces'
  import { computed, Ref, ref } from 'vue'
  import { getMeetingById } from '@/api'
  import { formatDateTime, getFileUrl } from '@/utilities'

  const meeting: Ref<Meeting> = ref({
    id: 0,
    title: '',
    summary: '',
    details: '',
    datetime: new Date(),
    place: '',
    assistants: [],
    files: [],
  })
  const route = useRoute()

  const formattedDateTime = computed(() =>
    formatDateTime(meeting.value.datetime)
  )

  const formatFileUrl = (filename: string) => getFileUrl(filename)

  async function loadMeeting() {
    meeting.value = await getMeetingById(String(route.params.id))
  }

  loadMeeting()
</script>

<style scoped></style>
