/* eslint-disable */
<template>
  <v-sheet class="rightPanel" v-if="drawer" elevation="1" light>
    <div class="d-flex flex-column mt-10 mx-7">
      <button class="small smallBtn" @click="$emit('close')">Close</button>
      <div class="d-flex flex-column mt-5">
        <div class="d-flex justify-content-between">
          <span class="header">Action Params</span>
          <button
            v-if="from === 'configuringJobs'"
            class="bigBtn"
            @click="$emit('openDialog')"
          >
            Edit Action Params
          </button>
        </div>

        <v-data-table
          class="customTableHeader"
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
    drawer: Boolean,
    actionParams: Object,
    from: String,
  },
  methods: {
    editItem() {
      this.openEditDialog = true;
    },
  },
  computed: {
    items() {
      const transform_params = Object.entries(
        this.actionParams.transform_params
      ).map(([key, value]) => ({ key, value, isEditable: true }));
      return [
        {
          key: 'transform_name',
          value: this.actionParams.transform_name,
          isEditable: false,
        },

        ...transform_params,
      ];
    },
  },
  data() {
    return {
      openDialog: false,
      transform_params: [],
      openEditDialog: false,
      headers: [
        { text: 'Key', value: 'key', sortable: false, filterable: false },
        { text: 'Value', value: 'value', sortable: false, filterable: false },

        { value: 'action', sortable: false, filterable: false },
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
