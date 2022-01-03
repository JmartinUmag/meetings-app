<template>
  <div class="container mt-3">
    <h1 class="page-title">Nueva Reunión</h1>
    <section class="columns">
      <div class="column is-half-desktop mx-auto">
        <MeetingForm
          :meeting="meeting"
          :users="users"
          :assistants="assistants"
          :files="files"
          @save="saveMeeting"
        />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
  import { reactive, Ref, ref } from 'vue'
  import { MeetingCreate, MeetingFormData, User } from '@/interfaces'
  import { createFile, createMeeting, getUsers } from '@/api'
  import MeetingForm from '@/components/MeetingForm.vue'
  import { useRouter } from 'vue-router'

  const router = useRouter()

  let meeting: MeetingCreate = reactive({
    title: '',
    summary: '',
    details: '',
    datetime: new Date(),
    place: '',
    assistantsIds: [],
  })
  const assistants: Ref<User[]> = ref([])
  const files: Ref<File[]> = ref([])
  const users: Ref<User[]> = ref([])

  async function loadUsers() {
    users.value = await getUsers()
  }

  async function saveMeeting(data: MeetingFormData) {
    meeting = reactive(data.meeting)
    assistants.value = data.assistants
    files.value = data.files

    meeting.assistantsIds = assistants.value.map((user: User) => user.id)
    const apiMeeting = await createMeeting(meeting)
    await Promise.all(
      files.value.map((file: File) => createFile(file, apiMeeting.id))
    )

    await router.push({ name: 'ViewMeeting', params: { id: apiMeeting.id } })
  }

  loadUsers()
</script>

<style scoped></style>
