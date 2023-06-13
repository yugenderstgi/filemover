<template>
  <div>
    <v-breadcrumbs :items="items" divider="">
      <template v-slot:item="{ item }">
        <span>{{ item.text }} > </span>
      </template>
    </v-breadcrumbs>
  </div>
</template>
<script>
export default {
  data() {
    return {
      items: [{ text: 'step1' }, { text: 'step2' }],
    };
  },
};
</script>
