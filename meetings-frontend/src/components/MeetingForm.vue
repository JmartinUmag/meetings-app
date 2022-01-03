<template>
  <form>
    <o-field horizontal label="Título">
      <o-input type="text" v-model="meetingLocal.title" maxlength="64" />
    </o-field>

    <o-field horizontal label="Resumen">
      <o-input
        type="textarea"
        v-model="meetingLocal.summary"
        rows="2"
        maxlength="128"
      />
    </o-field>

    <o-field horizontal label="Detalles">
      <o-input type="textarea" v-model="meetingLocal.details" />
    </o-field>

    <o-field horizontal label="Fecha / Hora">
      <o-datetimepicker icon="calendar" v-model="meetingLocal.datetime">
        <div class="buttons-footer has-text-centered mt-2">
          <o-button
            variant="primary"
            icon-left="calendar"
            @click="meetingLocal.datetime = new Date()"
          >
            Ahora
          </o-button>
          <o-button
            variant="danger"
            icon-left="close"
            class="ml-1"
            @click="meetingLocal.datetime = null"
          >
            Limpiar
          </o-button>
        </div>
      </o-datetimepicker>
    </o-field>

    <o-field horizontal label="Lugar">
      <o-input type="text" v-model="meetingLocal.place" maxlength="128" />
    </o-field>

    <o-field horizontal label="Asistentes">
      <o-inputitems
        v-model="assistantsLocal"
        :data="availableUsers"
        field="fullname"
        icon="account"
        placeholder="Añada usuarios"
        open-on-focus
        autocomplete
      >
      </o-inputitems>
    </o-field>

    <o-field horizontal label="Archivos">
      <FilesSelector v-model="filesLocal" />
    </o-field>

    <o-field horizontal>
      <o-button variant="primary" @click="saveMeeting">Guardar</o-button>
    </o-field>
  </form>
</template>

<script setup lang="ts">
  import { computed, ref, Ref } from 'vue'
  import { MeetingCreate, MeetingFormData, User } from '@/interfaces'
  import FilesSelector from '@/components/FilesSelector.vue'

  const props = defineProps<{
    users: User[]
    meeting: MeetingCreate
    assistants: User[]
    files: File[]
  }>()

  const emit = defineEmits<{
    (e: 'save', data: MeetingFormData): void
  }>()

  const meetingLocal: Ref<MeetingCreate> = ref(props.meeting)
  const assistantsLocal: Ref<User[]> = ref(props.assistants)
  const filesLocal: Ref<File[]> = ref(props.files)

  const availableUsers = computed(() =>
    props.users.filter((user: User) => !props.assistants.includes(user))
  )

  async function saveMeeting() {
    emit('save', {
      meeting: meetingLocal.value,
      assistants: assistantsLocal.value,
      files: filesLocal.value,
    })
  }
</script>

<style scoped></style>
