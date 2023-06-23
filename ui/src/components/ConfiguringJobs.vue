<!-- eslint-disable -->
<template>
  <div class="d-flex flex-column px-4">
    <div class="d-flex justify-content-between mt-4">
      <span class="header fs-3">Job Configuration</span>
      <SearchBar
        v-model="search"
        :action="true"
        :placeholder="
          el === 2 ? 'Search by Transform Name' : 'Search by FM Jobs'
        "
      ></SearchBar>
    </div>
    <v-stepper v-model="el" flat>
      <v-stepper-items>
        <v-stepper-content step="1">
          <v-data-table
            class="customTable"
            :headers="fmHeaders"
            :items="$attrs.fmJobs"
            :loading="true"
            item-key="id"
            :search="search"
            dense
          >
            <template v-slot:item.action="{ item }">
              <button
                class="small btn-white"
                @click="getFmJobsActions(item.id)"
              >
                View Action
              </button>
            </template>
          </v-data-table>
        </v-stepper-content>
        <v-stepper-content step="2">
          <v-data-table
            :headers="jobActionHeaders"
            :items="jobActions"
            class="customTable"
            :search="search"
            dense
            item-key="id"
            ><template v-slot:item.action="{ item }">
              <button class="small btn-white" @click="getActionParams(item.id)">
                View Action Params
              </button>
            </template></v-data-table
          >
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
    <v-overlay :value="openRightPanel" color="var(--lc-primary)" opacity="0.75"
      ><RightPanel
        :open-right-panel="openRightPanel"
        :action-params="actionParams"
        from="configuringJobs"
        @close="
          () => {
            openRightPanel = !openRightPanel;
          }
        "
        @openDialog="
          () => {
            openRightPanel = false;
            openDialog = true;
          }
        "
      ></RightPanel>
    </v-overlay>
    <v-overlay :value="openDialog" color="var(--lc-primary)" opacity="0.75">
      <v-dialog v-model="openDialog" max-width="900">
        <v-card class="px-4 py-3 d-flex flex-column" light>
          <span class="header fs-4">Edit Action Params</span>
          <div class="d-flex row mt-3">
            <div class="d-flex flex-column col-3">
              <span class="small">transform_name </span>
              <span class="header">{{ actionParams.transform_name }}</span>
            </div>
            <div class="d-flex col-9 justify-content-start row">
              <div
                class="col-6 gap-1 mb-4"
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
          <div class="d-flex justify-content-end gap-3 mt-3 mr-10">
            <button
              class="btn-white"
              @click="
                () => {
                  actionParams = ogActionParams;
                  openDialog = false;
                }
              "
            >
              Cancel
            </button>
            <button class="btn-primary px-3" @click="handleSave()">Save</button>
          </div>
        </v-card></v-dialog
      >
    </v-overlay>
    <snack-message :snackObj="snackObj"></snack-message>
  </div>
</template>
<script>
import {
  SearchBar,
  SnackMessage,
  SnackMixin,
} from '@lenders-cooperative/los-app-ui-component-lib';
import RightPanel from './RightPanel.vue';
import axios from 'axios';
export default {
  components: { SearchBar, RightPanel, SnackMessage },
  mixins: [SnackMixin],
  data() {
    return {
      el: 1,
      search: '',
      openRightPanel: false,
      openDialog: false,
      jobActions: [],
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
      jobActionHeaders: [
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
      currentJobId: null,
      actionParams: {},
      ogActionParams: {}, // saves unedited version of actionParms
    };
  },
  methods: {
    getFmJobsActions(fmJobId) {
      // fetches actions for that particular job
      this.el = 2;
      axios
        .get(`http://127.0.0.1:8000/fmaction/?fm_job_id=${fmJobId}`)
        .then((response) => {
          this.currentJobId = fmJobId;
          this.jobActions = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    async getActionParams(actionId) {
      // fetches action params for particular action
      await axios
        .get(
          `http://127.0.0.1:8000/fmaction/?fm_job_id=${this.currentJobId}&fm_action_id=${actionId}`
        )
        .then((response) => {
          this.actionParams = response.data[0].action_parms.params;
          this.ogActionParams = this.actionParams;
        })
        .catch((error) => {
          console.error(error);
        });
      this.openRightPanel = true;
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
        this.handleSnack({
          snackMsg: 'Updated Transform params !',
          snackType: 'success',
        });
      });
      this.openDialog = false;
    },
  },
 
};
</script>
<style scoped>
>>> .v-text-field.v-text-field--solo.v-input--dense > .v-input__control {
  min-height: 48px;
  min-width: 250px;
}
>>> .v-data-footer {
  justify-content: flex-end;
}
>>> .v-stepper__content {
  padding: 0 !important;
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