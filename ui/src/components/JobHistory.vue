<template>
  <v-main>
    <div class="d-flex flex-column">
      <span class="fs-3 header">Job History</span>
      <div class="d-flex flex-column">
        <v-stepper v-model="el" flat>
          <v-stepper-items>
            <v-stepper-content step="1">
              <v-data-table
                class="mt-5 pt-5 customTableHeader"
                :headers="headers"
                dense
                :search="search"
                :items="items"
                item-key="jobId"
              >
                <!-- <template v-slot:item="{ item }">
                  <tr class="zebra-stripe-row">
                    <td>{{ item.id }}</td>
                    <td>{{ item.name }}</td>
                    <td>{{ item.dml_ts }}</td>
                    <td>
                      <button class="small smallBtn" @click="el = 2">
                        View Action
                      </button>
                    </td>
                  </tr>
                </template> -->
              </v-data-table>
            </v-stepper-content>
            <v-stepper-content step="2">
              <v-data-table
                class="mt-5 pt-5 customTableHeader"
                dense
                :headers="headers"
                :items="items"
                item-key="jobId"
                ><template v-slot:item="{ item }">
                  <tr>
                    <td>{{ item.jobId }}</td>
                    <td>{{ item.jobName }}</td>
                    <td>{{ item.timeStamp }}</td>
                    <td>
                      <button class="small smallBtn" @click="openDrawer()">
                        View Actions Params
                      </button>
                    </td>
                  </tr>
                </template></v-data-table
              >
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
        <v-overlay :value="drawer" color="var(--lc-primary)" opacity="0.75"
          ><RightPanel
            :drawer="drawer"
            @close="
              () => {
                drawer = !drawer;
              }
            "
          ></RightPanel>
        </v-overlay>
      </div>
    </div>
  </v-main>
</template>
<script>
import RightPanel from './RightPanel.vue';
import axios from 'axios';

export default {
  components: { RightPanel },
  data() {
    return {
      el: 1,
      headers: [
        { text: 'Job Event ID', value: 'id', sortable: false, filterable: false },
        { text: 'Job ID', value: 'fm_job_id', sortable: false, filterable: false },
        {
          text: 'Job Name',
          value: 'job_name',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Job Duration',
          value: 'job_duration',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Job Start',
          value: 'start_tms',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Job End',
          value: 'end_tms',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Status',
          value: 'status',
          sortable: false,
          filterable: false,
        },
      ],
      items: []
,      drawer: false,
      dates: null,
      datePickerOpen: false,
      selectedDates: null,
      dateRange: '',
    };
  },
  methods: {
    openDrawer() {
      this.drawer = true;
    },
    openDatePicker() {
      this.datePickerOpen = true;
    },
    closeDatePicker() {
      this.datePickerOpen = false;
    },
    updateDateRange() {
      if (this.selectedDates) {
        const startDate = this.selectedDates.start;
        const endDate = this.selectedDates.end;
        this.dateRange = `${startDate.toLocaleDateString()} - ${endDate.toLocaleDateString()}`;
      }
    },
  },
  created() {
    axios.get('http://127.0.0.1:8000/fmjobevent/')
  .then(response => {
    this.items=response.data
    console.log(this.item);
  })
  .catch(error => {
    console.error(error);
  });

  },
  computed: {
    dateRangeText() {
      if (this.dates) return this.dates.join(' ~ ');
      return '';
    },
  },
};
</script>
