<template>
  <v-sheet class="rightPanel" v-if="openRightPanel" light>
    <div class="d-flex flex-column pt-5 px-4">
      <button class="small btn-white" @click="$emit('close')">Close</button>
      <div class="d-flex flex-column">
        <div class="d-flex justify-content-between my-3">
          <span class="header fs-4">Action Params</span>
          <button
            v-if="from === 'configuringJobs'"
            class="btn-primary"
            @click="$emit('openDialog')"
          >
            Edit Action Params
          </button>
        </div>

        <v-data-table
          class="customTable"
          :headers="headers"
          :items="items"
          dense
          hide-default-footer
        >
        </v-data-table>
      </div>
    </div>
  </v-sheet>
</template>
<script>
export default {
  props: {
    openRightPanel: Boolean,
    actionParams: Object,
    from: String,
  },
  computed: {
    items() {
      const transform_params = Object.entries(
        this.actionParams.transform_params
      ).map(([key, value]) => ({ key, value }));
      return [
        {
          key: 'transform_name',
          value: this.actionParams.transform_name,
        },

        ...transform_params,
      ];
    },
  },
  data() {
    return {
      openDialog: false,
      openEditDialog: false,
      headers: [
        { text: 'Key', value: 'key', sortable: false, filterable: false },
        { text: 'Value', value: 'value', sortable: false, filterable: false },
      ],
    };
  },
};
</script>
<style scoped>
.rightPanel {
  position: fixed !important;
  right: 0 !important;
  top: 0 !important;
  height: 100% !important;
  width: 55% !important;
  background-color: var(--lc-bg-light);
  /* background-color: var(--lc-background-color); */
}
.customTable {
  background-color: var(--lc-bg-light);
}
.customTable >>> tbody tr:nth-child(even) {
  background-color: var(--lc-background-color);
}
.customTable >>> thead tr {
  border-bottom: 2px solid var(--lc-primary);
}
.customTable >>> thead tr th {
  color: var(--lc-primary) !important;
  font-size: 0.875rem !important;
}
</style>
