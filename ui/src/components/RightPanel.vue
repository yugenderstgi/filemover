<template>
  <v-sheet class="rightPanel" v-if="drawer" elevation="1" light>
    <div class="d-flex flex-column mt-10 ml-7">
      <button class="small smallBtn" @click="$emit('close')">Close</button>
      <div class="d-flex flex-column mt-5">
        <span class="fs-3 header">Action Params</span>
        <v-data-table
          class="customTableHeader"
          :headers="headers"
          :items="items"
          dense
          hide-default-footer
        ></v-data-table>
      </div>
    </div>
  </v-sheet>
</template>
<script>
export default {
  props: {
    drawer: Boolean,
  },
  data() {
    return {
      headers: [
        { text: 'Key', value: 'key', sortable: false, filterable: false },
        { text: 'Value', value: 'value', sortable: false, filterable: false },
      ],
      items: [
        { key: 'transform_name', value: 'Get Country File' },
        { key: 'transform_name', value: 'Get Country File' },
        { key: 'transform_name', value: 'Get Country File' },
        { key: 'transform_name', value: 'Get Country File' },
        { key: 'transform_name', value: 'Get Country File' },
      ],
    };
  },
};
</script>
<style scoped>
.customTableHeader >>> thead.v-data-table-header tr {
  border-bottom: 2px solid var(--lc-primary);
  font-size: 1.5rem;
}
.rightPanel {
  position: fixed !important;
  right: 0 !important;
  top: 0 !important;
  height: 100% !important;
  width: 60% !important;
}
</style>
