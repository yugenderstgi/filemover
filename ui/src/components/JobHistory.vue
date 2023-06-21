<!-- eslint-disable -->
<template>
  <v-main>
    <div class="d-flex flex-column">
      <span class="fs-3 header">Job History</span>
      <div class="d-flex flex-column">
        <v-stepper v-model="currenStep" flat non-linear>
          <v-stepper-header>
            <v-stepper-step editable step="1"> Job Event List </v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step step="2"> {{ stepperHeading }} </v-stepper-step>
          </v-stepper-header>
          <v-stepper-items>
            <v-stepper-content step="1">
              <v-data-table
                class="mt-5 pt-5 customTableHeader"
                :headers="headers"
                dense
                :search="search"
                :items="items"
                item-key="jobId"
                :loading="isLoading"
                loading-text="Loading..."
                hide-rows-per-page
                hide-default-footer
              >
                <template v-slot:item.action="{ item }">
                  <button class="small smallBtn" @click="getActions(item)">
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
                :search="search"
                :loading="isLoading"
                loading-text="Loading..."
                hide-rows-per-page
                hide-default-footer
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
      currenStep: 1,
      search: '',
      headers: [
        {
          text: 'Job Event ID',
          value: 'id',
          sortable: true,
          filterable: false,
          width: '10%',
        },
        {
          text: 'Job ID',
          value: 'fm_job_id',
          sortable: true,
          filterable: false,
          width: '5%',
        },
        {
          text: 'Job Name',
          value: 'job_name',
          sortable: true,
          filterable: false,
          width: '10%',
        },
        {
          text: 'Job Duration',
          value: 'job_duration',
          sortable: true,
          filterable: false,
          width: '10%',
        },
        {
          text: 'Job Start',
          value: 'start_tms',
          sortable: true,
          filterable: false,
          width: '25%',
        },
        {
          text: 'Job End',
          value: 'end_tms',
          sortable: true,
          filterable: false,
          width: '25%',
        },
        {
          text: 'Status',
          value: 'status',
          sortable: true,
          filterable: false,
          width: '10%',
        },
        {
          value: 'action',
          sortable: true,
          filterable: false,
          width: '10%',
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
          width: '5%',
        },
        {
          text: 'Action ID',
          value: 'fm_action_id',
          sortable: false,
          filterable: false,
          width: '5%',
        },
        {
          text: 'Action Type',
          value: 'transform_name',
          sortable: false,
          filterable: false,
          width: '25%',
        },
        {
          text: 'Action Duration',
          value: 'action_duration',
          sortable: false,
          filterable: false,
          width: '10%',
        },
        {
          text: 'Action Start',
          value: 'start_tms',
          sortable: false,
          filterable: false,
          width: '15%',
        },
        {
          text: 'Action End',
          value: 'end_tms',
          sortable: false,
          filterable: false,
          width: '15%',
        },
        {
          text: 'Status',
          value: 'status',
          sortable: false,
          filterable: false,
          width: '10%',
        },
        {
          value: 'action',
          sortable: false,
          filterable: false,
          width: '15%',
        },
      ],
      jobDescItems: [],
      stepperHeading: 'Finantxn Replicate',
    };
  },
  watch: {
    currentStep() {
      if (this.currentStep == 1) {
        this.stepperHeading = 'Etran Payment Activity Load';
      }
    },
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
    async getActions(jobEvent) {
      this.currentJobEventId = jobEvent.id;
      this.isLoading = true;

      await axios(
        `http://127.0.0.1:8000/fmjobactionevent/?fm_job_event_id=${jobEvent.id}`
      ).then((res) => {
        this.jobDescItems = res.data;
        this.isLoading = false;
      });
      this.currenStep = 2;
      this.stepperHeading = jobEvent.job_name;
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
          this.isLoading = false;
        })
        .catch((error) => {
          console.error(error);
        });
      this.drawer = true;
    },
  },
  created() {
    this.isLoading = true;
    axios
      .get('http://127.0.0.1:8000/fmjobevent/')
      .then((response) => {
        this.items = response.data;
        this.isLoading = false;
      })
      .catch((error) => {
        console.error(error);
        this.isLoading = false;
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

<style scoped>
.customTableHeader >>> thead.v-data-table-header tr {
  border-bottom: 2px solid var(--lc-primary);
  font-size: 1.5rem;
}
.customTableHeader >>> .v-data-table-header th {
  border-bottom: 2px solid var(--lc-primary);
  font-size: 1rem;
  color: var(--lc-primary) !important;
  /* Add more styles as needed */
}
</style>