<!-- eslint-disable -->
<template>
  <div class="d-flex flex-column px-4">
    <div class="d-flex justify-content-between mt-4">
      <span class="header fs-3">Job Configuration</span>
      <SearchBar v-model="search" :action="true" :placeholder="el === 2 ? 'Search by Transform Name' : 'Search by FM Jobs'
        "></SearchBar>
    </div>
    <!-- <div>{{schema}}</div> -->
    <v-stepper v-model="el" flat>
      <div class="stepcontainer">
        <v-stepper-header>
          <v-stepper-step editable step="1" class="step1"> Fm_Jobs
          </v-stepper-step>
          <v-stepper-step editable v-if="el == 2" step="2" class="step2">
            {{ currentJobName }} </v-stepper-step>
        </v-stepper-header>
      </div>
      <v-stepper-items>
        <v-stepper-content step="1">
          <!-- <v-data-table id="jobTable" class="customTable" :headers="fmHeaders" :search="search" :items="fmJobs"
            :loading="true" :footer-props="{
              'items-per-page-options': [4],
              'disable-items-per-page': true,
            }" :options.sync="pagination" item-key="id" dense> -->
          <v-data-table id="jobTable" class="customTable" :headers="fmHeaders" :search="search" :items="fmJobs"
            :server-items-length="pagination.totalItems" :options.sync="pagination" @update:options="getFmJobs"
            :loading="true" item-key="id" dense>
            <template v-slot:[`item.action`]="{ item }">
              <button class="small btn-white" @click="getFmJobsActions(item.id, item.name)">
                View Action
              </button>
            </template>
          </v-data-table>
        </v-stepper-content>
        <v-stepper-content step="2">
          <v-data-table :headers="jobActionHeaders" :items="jobActions" :search="search" class="customTable" dense
            item-key="id">
            <template v-slot:[`header.action_type`]="{ header }">
              <div class="column-header">
                <span>{{ header.text }}</span>

                <v-icon class="filter-icon" @click="showFilter = !showFilter">mdi-filter-outline</v-icon>
                <div v-if="showFilter" class="filter-box">
                  <label v-for="option in filterOptions" :key="option.value">
                    <input type="checkbox" :value="option.value" v-model="selectedFilters">
                    {{ option.label }}
                  </label>
                  <button class="applyButton" @click="applyFilters">Apply</button>
                </div>
              </div>
            </template>
            <template v-slot:[`item.action`]="{ item }">
              <button class="small btn-white" @click="getActionParams(item.id)">
                View Action Params
              </button>
            </template></v-data-table>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
    <v-overlay :value="openRightPanel" color="var(--lc-primary)" opacity="0.75">
      <RightPanel :open-right-panel="openRightPanel" :action-params="actionParams" from="configuringJobs" @close="() => {
        openRightPanel = !openRightPanel;
      }
        " @openDialog="() => {
    openRightPanel = false;
    openDialog = true;
  }
    "></RightPanel>
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
              <div class="col-6 gap-1 mb-4" v-for="(value, key) in actionParams.transform_params">
                <span>{{ key }}</span>
                <v-text-field v-model="actionParams.transform_params[key]" class="inputBox" dense solo
                  hide-details></v-text-field>
              </div>
            </div>
          </div>
          <div class="d-flex justify-content-end gap-3 mt-3 mr-10">
            <button class="btn-white" @click="() => {
              actionParams = ogActionParams;
              openDialog = false;
            }
              ">
              Cancel
            </button>
            <button class="btn-primary px-3" @click="handleSave()">Save</button>
          </div>
        </v-card></v-dialog>
    </v-overlay>
    <snack-message :snackObj="snackObj"></snack-message>
  </div>
</template>
<script>
import {
  SearchBar,
  SnackMessage,
  SnackMixin,
  //BreadCrumb,

} from '@lenders-cooperative/los-app-ui-component-lib';
import RightPanel from './RightPanel.vue';
import axios from 'axios';
export default {
  components: {
    SearchBar, RightPanel, SnackMessage,
    //BreadCrumb,

  },
  mixins: [SnackMixin],
  props: ['schema'],
  data() {
    return {
      // fmJobsData: this.$attrs.fmJobs,
      fmJobs: [],
      pagination: {
        page: 1,
        itemsPerPage: 5,
        totalItems: 0
      },
      // pagination: {
      // page: 1, // Initial page number
      // itemsPerPage: 4, // Number of items to display per page
      // totalItems: 0 // Set the totalItems based on the initial data length
      // }
      currentJobName: '',
      currentJobId: '',
      search: '',
      showActionsBreadcrumb: false,
      showFilter: false,
      filterOptions: [
        { label: 'Transform', value: 'transform' },
        { label: 'Unzip', value: 'Unzip' }
      ],
      selectedFilters: [],
      // dataTableId : this.jobTable,
      clickedBreadcrumb: null,
      el: 1,
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
          filterable: true,
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

      actionParams: {},
      ogActionParams: {}, // saves unedited version of actionParms
    };
  },
  watch: {
    el() {
      console.log("El value : ", this.el)
      if (this.el == 1) {
        this.showActionsBreadcrumb = false
      }

    },
    schema() {
      this.getFmJobs();
    },

    search(newSearchValue) {
      if (newSearchValue && newSearchValue.length > 3 && !this.showActionsBreadcrumb) {
        let url = `http://127.0.0.1:8000/fmjobs/?job_name=${newSearchValue}`
        console.log('URL is : ', url)
        this.searchByJobName(url);
      }
      else if (newSearchValue && newSearchValue.length > 2 && this.showActionsBreadcrumb) {
        let url = `http://127.0.0.1:8000/fmaction/?fm_job_id=${this.currentJobId}&transform_name=${newSearchValue}`
        console.log('URL is : ', url)
        this.searchByTransformName(url);

      }
      else if (!newSearchValue && !this.showActionsBreadcrumb) {
        this.getFmJobs()
      }
      else if (!newSearchValue && this.showActionsBreadcrumb) {
        this.getFmJobsActions(this.currentJobId, this.currentJobName)
      }
    }
  },
  // mounted: {
  //   fmJobs(){
  //     console.log(this.props)
  //   }
  // },

  methods: {
    // getFmJobs() {
    //   axios.get(this.url).then((res) => {
    //     console.log(res.data)
    //     this.fmJobs = res.data.results;
    //     this.url = res.data.next;
    //   }
    //   ).catch((err) => {
    //     console.log(err)
    //   })
    // },
    getFmJobs() {
      const url = `http://127.0.0.1:8000/fmjobs/?page=${this.pagination.page}`
      axios.get(url).then((res) => {
        this.fmJobs = res.data.results;
        this.pagination.totalItems = res.data.count

      }
      ).catch((err) => {
        console.log(err)
      })
    },

    getFmJobsActions(fmJobId, fmjobName) {
      // fetches actions for that particular job
      console.log("Item Id : ", fmJobId)
      console.log("Item Name : ", fmjobName)
      this.currentJobName = fmjobName
      this.currentJobId = fmJobId
      this.showActionsBreadcrumb = true;
      this.el = 2;
      axios
        .get(`http://127.0.0.1:8000/fmaction/?fm_job_id=${fmJobId}`)
        .then((response) => {
          this.jobActions = response.data.results;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getActionParams(actionId) {
      // fetches action params for particular action
      axios
        .get(
          `http://127.0.0.1:8000/fmaction/?fm_job_id=${this.currentJobId}&fm_action_id=${actionId}`
        )
        .then((response) => {
          // this.actionParams = response.data[0].action_parms.params;
          this.actionParams = response.data.results[0].action_parms.params;
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
        console.log('Response:', response.data.results);
        this.handleSnack({
          snackMsg: 'Updated Transform params !',
          snackType: 'success',
        });
      });
      this.openDialog = false;
    },
    searchByJobName(url) {
      console.log("searchByJobName API - STARTED")
      axios(url)
        .then((response) => {
          // this.$attrs.fmJobs = response.data;
          this.fmJobs = response.data.results;
          // console.log("Response Data : ",this.items);
        })
        .catch((error) => {
          console.error(error);
        });
      console.log("searchByJobName API - ENDED")
    },
    searchByTransformName(url) {
      console.log("searchByTransformName API - STARTED")
      axios(url)
        .then((response) => {
          // this.$attrs.fmJobs = response.data;
          this.fmJobs = response.data.results;
          // console.log("Response Data : ",this.items);
        })
        .catch((error) => {
          console.error(error);
        });
      console.log("searchByTransformName API - ENDED")
    },
    // getFmJobs() {
    //   this.fmJobs = this.fmJobsProps;
    // },
    applyFilters() {
      console.log('Selected Filters:', this.selectedFilters);
      const url = `http://127.0.0.1:8000/fmaction/?fm_job_id=${this.currentJobId}&action_type=${this.selectedFilters}`
      console.log("Action Type URL is : ", url)
      this.searchByActionType(url);
    },
    searchByActionType(url) {
      console.log("searchByActionType API - STARTED")
      axios(url)
        .then((response) => {
          // this.$attrs.fmJobs = response.data;
          this.jobActions = response.data.results;
          // console.log("Response Data : ",this.items);
        })
        .catch((error) => {
          console.error(error);
        });
      console.log("searchByActionType API - ENDED")
    }
  },
  created() {
    this.getFmJobs();
  }
}
</script>
<style scoped>
>>>.v-text-field.v-text-field--solo.v-input--dense>.v-input__control {
  min-height: 48px;
  min-width: 250px;
}

>>>.v-data-footer {
  justify-content: flex-end;
}

.footer {
  display: flex;
  justify-content: flex-end;
}

>>>.v-stepper__content {
  padding: 0 !important;
}

.customTable {
  background-color: var(--lc-bg-light);
}

.customTable>>>tbody tr:nth-child(even) {
  background-color: var(--lc-background-color);
}

.customTable>>>thead tr {
  border-bottom: 2px solid var(--lc-primary);
}

.customTable>>>thead tr th {
  color: var(--lc-primary) !important;
  font-size: 0.875rem !important;
}

.breadcrumbs-container {
  display: flex;
  align-items: center;
}

.btnContainer {
  display: flex;
  align-items: center;
  margin-top: 60px;
  margin-bottom: 60px;
}

.stepcontainer {
  display: flex;
  justify-content: space-between;
  margin-top: 60px;
  background-color: var(--lc-text-light);

}

.step1 {
  width: 200px;
  height: 50px;
  /* background-color: var(--lc-light-gray); */
  background-color: #4673ae;
  clip-path: polygon(0% 0%, 88% 0%, 100% 50%, 88% 100%, 0% 100%);
  padding: 0.5rem 1rem 0.5rem 1rem;
  text-align: center;
  margin-right: 30px;
  font-size: large;
  border-color: var(--lc-primary);
  border: 2px;
}

.step2 {
  margin-right: 30px;
  background-color: #4673ae;
  width: 200px;
  height: 50px;
  clip-path: polygon(0% 0%, 88% 0%, 100% 50%, 88% 100%, 0% 100%);
  padding: 0.5rem 1rem 0.5rem 1rem;
  text-align: center;
  font-size: large;

}

.filter-dropdown {
  margin-left: auto;
  /* Push the dropdown to the right side */
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-icon {
  margin-left: 5px;
  color: var(--lc-primary);
}

.column-header {
  display: flex;
  align-items: center;
}

.filter-box {
  margin-top: 10px;
}

.applyButton {
  margin-left: 10px;
}

.sort-icon {
  color: var(--lc-primary);
}
</style>