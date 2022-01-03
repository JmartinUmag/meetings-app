<template>
  <div class="file is-boxed">
    <label class="file-label">
      <input
        class="file-input"
        type="file"
        name="resume"
        multiple
        @change="addFiles"
      />
      <span class="file-cta">
        <span class="file-icon">
          <o-icon icon="upload" />
        </span>
        <span class="file-label">Arrastra tus archivos aquí</span>
        <span class="file-lable"> o presiona para seleccionarlos </span>
      </span>
    </label>
  </div>

  <div class="field is-grouped is-grouped-multiline mt-2">
    <div class="control" v-for="(file, index) in files" :key="index">
      <div class="tags has-addons">
        <span class="tag is-light">{{ file.name }}</span>
        <a
          class="tag is-delete is-light is-danger"
          @click="removeFile(index)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, Ref } from 'vue'

  const props = defineProps<{
    modelValue: File[]
  }>()

  const emit = defineEmits<{
    (e: 'update:modelValue', files: File[]): void
  }>()

  const files: Ref<File[]> = ref(props.modelValue)

  async function addFiles(event: Event | null) {
    if (!event) return
    const eventFiles = (event.target as HTMLInputElement).files

    if (eventFiles) {
      files.value.push(...Array.from(eventFiles))
    }

    emit('update:modelValue', files.value)
  }

  async function removeFile(index: number) {
    files.value.splice(index, 1)

    emit('update:modelValue', files.value)
  }
</script>

<style scoped></style>
