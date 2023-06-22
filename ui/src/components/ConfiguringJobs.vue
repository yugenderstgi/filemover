<!-- eslint-disable -->
<template>
  <v-main>
    <div class="d-flex row justify-content-between w-100 mb-5">
      <span class="col-7 fs-3 header">Configuring Jobs</span>
      <div class="d-flex col-4">
        <v-icon class="px-2">mdi-magnify</v-icon>
        <v-text-field
          :counter="false"
          class="inputBox"
          label="Search by FM Jobs"
          v-model="search"
          solo
          single-line
          dense
          hide-details
          :placeholder="
            currentStep === 2 ? 'Search by Transform Name' : 'Search by FM Jobs'
          "
        ></v-text-field>
      </div>
    </div>
    <v-stepper non-linear v-model="currentStep" flat>
      <v-stepper-header>
        <v-stepper-step editable step="1"> FM Jobs(200) </v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step v-if="currentStep===2" step="2">
          {{ stepperHeading }}
        </v-stepper-step>
      </v-stepper-header>
      <v-stepper-items>
        <v-stepper-content step="1">
          <v-data-table
            class="mt-5 pt-5 customTableHeader"
            :headers="fmHeaders"
            :items="fmJobs"
            item-key="jobId"
            :search="search"
            dense
            :loading="isLoading"
            loading-text="Loading..."
            hide-rows-per-page
            hide-default-footer
          >
            <template v-slot:item.action="{ item }">
              <button class="small smallBtn" @click="getEtranPayment(item)">
                View Action
              </button>
            </template>
          </v-data-table>
        </v-stepper-content>
        <v-stepper-content step="2">
          <v-data-table
            class="mt-5 pt-5 customTableHeader"
            dense
            :headers="etranHeaders"
            :items="etranItems"
            item-key="jobId"
            :loading="isLoading"
            :search="search"
            loading-text="Loading..."
            hide-rows-per-page
            hide-default-footer
            ><template v-slot:item.action="{ item }">
              <button class="small smallBtn" @click="getActionParams(item.id)">
                View Action Params
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
        from="configuringJobs"
        @close="
          () => {
            drawer = !drawer;
          }
        "
        @openDialog="
          () => {
            drawer = false;
            openDialog = true;
          }
        "
      ></RightPanel>
    </v-overlay>
    <v-overlay :value="openDialog" color="var(--lc-primary)" opacity="0.75">
      <v-dialog v-model="openDialog" max-width="900">
        <v-card class="px-5 py-3 d-flex flex-column" light>
          <h4 class="header">Edit Action Params</h4>
          <div class="d-flex row">
            <div class="d-flex flex-column col-4">
              <span class="small">transform_name </span>
              <span class="header">{{ actionParams.transform_name }}</span>
            </div>
            <div class="d-flex col-8 justify-content-start row">
              <div
                class="col-6 gap-1 mb-2"
                v-for="(value, key) in actionParams.transform_params"
              >
                <span>{{ key }}</span>
                <v-text-field
                  v-model="actionParams.transform_params[key]"
                  class="inputBox"
                  dense
                  solo
                  hide-details
                ></v-text-field>
              </div>
            </div>
          </div>
          <div class="d-flex justify-content-end gap-3 mt-5 mr-10">
            <button
              class="smallBtn"
              @click="
                () => {
                  actionParams = ogActionParams;
                  openDialog = false;
                }
              "
            >
              Cancel
            </button>
            <button class="bigBtn px-3" @click="handleSave()">Save</button>
          </div>
        </v-card></v-dialog
      >
    </v-overlay>
  </v-main>
</template>
<script>
import RightPanel from './RightPanel.vue';
import axios from 'axios';

export default {
  components: { RightPanel },
  data() {
    return {
      currentStep: 1,
      drawer: false,
      search: '',
      openDialog: false,
      currentId: null,
      currentActionId: null,
      transform_params: [],
      fmHeaders: [
        {
          text: 'Job_ID',
          value: 'id',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Job Name',
          value: 'name',
          sortable: false,
        },
        {
          text: 'Time Stamp',
          value: 'dml_ts',
          sortable: false,
          filterable: false,
        },
        {
          value: 'action',
          sortable: false,
          filterable: false,
        },
      ],
      etranHeaders: [
        {
          text: 'Action_ID',
          value: 'id',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Sequence',
          value: 'seq',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Action Type',
          value: 'action_type',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Transform Name',
          value: 'transform_name',
          sortable: false,
          filterable: true,
        },
        {
          text: 'Description',
          value: 'description',
          sortable: false,
          filterable: false,
        },
        {
          text: 'Time Stamp',
          value: 'dml_ts',
          sortable: false,
          filterable: false,
        },

        {
          value: 'action',
          sortable: false,
          filterable: false,
        },
      ],
      fmJobs: [],
      etranItems: [],
      actionParams: {},
      ogActionParams: {},
      isLoading: Boolean,
      stepperHeading: '',
    };
  },
  methods: {
    getEtranPayment(job) {
      this.isLoading = true;
      this.currentStep = 2;
      axios
        .get(`http://127.0.0.1:8000/fmaction/?fm_job_id=${job.id}`)
        .then((response) => {
          this.currentId = job.id;
          this.etranItems = response.data;
          this.isLoading = false;
        })
        .catch((error) => {
          this.isLoading = false;
          console.log(error);
        });
      this.stepperHeading = job.name;
    },
    async getActionParams(actionId) {
      await axios
        .get(
          `http://127.0.0.1:8000/fmaction/?fm_job_id=${this.currentId}&fm_action_id=${actionId}`
        )
        .then((response) => {
          this.actionParams = response.data[0].action_parms.params;
          this.ogActionParams = this.actionParams;
          this.isLoading = false;
        })
        .catch((error) => {
          console.error(error);
          this.isLoading = false;
        });
      this.drawer = true;
      this.currentActionId = actionId;
    },
    handleSave() {
      const url = `http://127.0.0.1:8000/fmaction/${this.currentActionId}/update_action_params/`;
      const data = {
        action_parms: {
          params: {
            transform_params: {
              ...this.actionParams.transform_params,
            },
          },
        },
      };

      axios.put(url, data).then((response) => {
        // Handle the response data
        console.log('Response:', response.data);
      });
      this.openDialog = false;
    },
  },
  created() {
    this.isLoading = true;
    axios

      .get('http://127.0.0.1:8000/fmjobs')
      .then((response) => {
        this.fmJobs = response.data;
        this.isLoading = false;
        console.log(this.item);
      })
      .catch((error) => {
        this.isLoading = false;
        console.log(error);
      });
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