<!-- eslint-disable -->
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
                <template v-slot:item.action="{ item }">
                  <button class="small smallBtn" @click="getActions(item.id)">
                    View Action
                  </button>
                </template>
              </v-data-table>
            </v-stepper-content>
            <v-stepper-content step="2" class="pl-0">
              <v-data-table
                class="mt-5 pt-5 customTableHeader mr-10"
                dense
                :headers="jobDescHeader"
                :items="jobDescItems"
                item-key="jobId"
                ><template v-slot:item.action="{ item }">
                  <button
                    class="small smallBtn"
                    @click="getResolvedActionParams(item.id)"
                  >
                    View Resolved Action Params
                  </button>
                </template></v-data-table
              >
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
        <v-overlay :value="drawer" color="var(--lc-primary)" opacity="0.75"
          ><RightPanel
            :drawer="drawer"
            :action-params="actionParams"
            from="jobHistory"
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
        {
          text: 'Job Event ID',
          value: 'id',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Job ID',
          value: 'fm_job_id',
          sortable: false,
          filterable: false,
        },
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
        {
          value: 'action',
          sortable: false,
          filterable: false,
        },
      ],
      items: [],
      drawer: false,
      dates: null,
      datePickerOpen: false,
      selectedDates: null,
      dateRange: '',
      currentJobEventId: '',
      actionParams: {},
      jobDescHeader: [
        {
          text: 'Job Action Event ID',
          value: 'id',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Action ID',
          value: 'fm_action_id',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Action Type',
          value: 'transform_name',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Action Duration',
          value: 'action_duration',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Action Start',
          value: 'start_tms',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Action End',
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
        {
          value: 'action',
          sortable: false,
          filterable: false,
        },
      ],
      jobDescItems: [],
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
    async getActions(jobEventId) {
      this.currentJobEventId = jobEventId;
      await axios(
        `http://127.0.0.1:8000/fmjobactionevent/?fm_job_event_id=${jobEventId}`
      ).then((res) => {
        this.jobDescItems = res.data;
      });
      this.el = 2;
    },
    async getResolvedActionParams(actionId) {
      await axios
        .get(
          `http://127.0.0.1:8000/fmjobactionevent/?
fm_job_event_id=${this.currentJobEventId}&fm_job_action_event_id=${actionId}`
        )

        .then((response) => {
          this.actionParams = response.data[0].resolved_action_parms.params;
          console.log(this.actionParams);
        })
        .catch((error) => {
          console.error(error);
        });
      this.drawer = true;
    },
  },
  created() {
    axios
      .get('http://127.0.0.1:8000/fmjobevent/')
      .then((response) => {
        this.items = response.data;
        console.log(this.item);
      })
      .catch((error) => {
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
