<template>
  <v-card>
    <v-layout>
      <v-navigation-drawer
        class="bg-deep-purple"
        color="blue-darken-4"
        theme="dark"
        permanent
        rounded="false"
        :width="300"
      >
        <div></div>
        <v-list color="transparent">
          <v-list-item
            prepend-icon="mdi-folder-information-outline"
            title="Configuring Jobs"
          ></v-list-item>
          <v-divider
            :thickness="2"
            class="border-opacity-50"
            color="info"
          ></v-divider>
          <v-list-item
            prepend-icon="mdi-file-alert"
            title="Triggering Jobs"
          ></v-list-item>
          <v-divider
            :thickness="2"
            class="border-opacity-50"
            color="info"
          ></v-divider>
          <v-list-item
            prepend-icon="mdi-account-group-outline"
            title="Terminating Jobs"
          ></v-list-item>
          <v-divider
            :thickness="2"
            class="border-opacity-50"
            color="info"
          ></v-divider>
          <v-list-item
            prepend-icon="mdi-history"
            title="Job History"
          ></v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-main style="height: 100vh"></v-main>
    </v-layout>
  </v-card>
</template>

<script>
export default {
  data() {
    return {};
  },
};
</script>

