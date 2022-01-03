<template>
  <div class="container mt-4">
    <div class="level-right">
      <div class="buttons">
        <o-button
          variant="primary"
          icon-left="plus"
          tag="router-link"
          :to="{ name: 'NewMeeting' }"
        >
          Nueva Reunión
        </o-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>
