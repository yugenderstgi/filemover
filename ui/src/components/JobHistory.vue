<!-- eslint-disable -->
<template>
  <div class="d-flex flex-column px-4">
    <div class="d-flex justify-content-between mt-4">
      <span class="header fs-3">Job History</span>
      <SearchBar v-model="search" :action="true" :placeholder="'Search by Job Name'
        "></SearchBar>
      <!-- <p>search value is : {{ search }}</p> -->
    </div>
    <div class="datepicker" v-if="!showActionsBreadcrumb">
      <DatePicker v-model="selectedDates.start"></DatePicker>
      <!-- <p>Start Date: {{ selectedDates.start}}</p> -->
      <DatePicker v-model="selectedDates.end"></DatePicker>
      <!-- <p>End Date: {{ selectedDates.end }}</p> -->
    </div>
    <!-- <div class="btnContainer" v-if="showActionsBreadcrumb">
      <button type="button" id="btn1" class="jobEventList">Job Event List </button>
      <button type="button" id="btn2" class="jobActionList">{{currentJobName}}</button>
    </div>
       -->


    <div class="d-flex flex-column">
      <v-stepper v-model="el" flat>
        <!-- <div class="stepcontainer" v-if="showActionsBreadcrumb"> -->
        <div class="stepcontainer">

          <v-stepper-header class="stepper-header">
            <v-stepper-step editable step="1" class="step1"> Job Event List
            </v-stepper-step>
            <v-stepper-step editable v-if="el == 2" step="2" class="step2">
              {{ currentJobName }} </v-stepper-step>
          </v-stepper-header>
        </div>
        <v-stepper-items>
          <v-stepper-content step="1">
            <v-data-table id="jobEventTable" loading="true" class="customTable" :headers="headers" :items="items"
              :search="search" :server-items-length="pagination.totalItems" :options.sync="pagination"
              @update:options="fetchData" item-key="jobId" dense>
              <template v-slot:header.status="{ header }">
                <div class="column-header">
                  <span>{{ header.text }}</span>
                  <v-icon class="filter-icon" @click="showFilter = !showFilter">mdi-filter-outline</v-icon>
                  <div v-if="showFilter" class="filter-box">
                    <label v-for="option in filterOptions" :key="option.value">
                      <input type="checkbox" :value="option.value" v-model="selectedFilters">
                      {{ option.label }}
                    </label>
                    <button class="applyButton" @click="fetchData">Apply</button>
                  </div>
                </div>
              </template>
              <template v-slot:item.action="{ item }">
                <button class="small smallBtn" @click="getActions(item.id, item.job_name)">
                  View Action
                </button>
              </template>
            </v-data-table>
          </v-stepper-content>
          <v-stepper-content step="2" class="pl-0">
            <v-data-table class="mt-5 pt-5 customTable mr-10" dense :headers="jobDescHeader" :items="jobDescItems"
              item-key="jobId">
              <template v-slot:header.status="{ header }">
                <div class="column-header">
                  <span>{{ header.text }}</span>
                  <v-icon class="filter-icon" @click="showFilter = !showFilter">mdi-filter-outline</v-icon>
                  <div v-if="showFilter" class="filter-box">
                    <label v-for="option in filterOptions" :key="option.value">
                      <input type="checkbox" :value="option.value" v-model="selectedFilters">
                      {{ option.label }}
                    </label>
                    <button class="applyButton" @click="applyFiltersJobActions">Apply</button>
                  </div>
                </div>
              </template>



              <template v-slot:item.action="{ item }">
                <button class="small smallBtn" @click="getResolvedActionParams(item.id)">
                  View Resolved Action Params
                </button>
              </template></v-data-table>


          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>

      <v-overlay :value="openRightPanel" color="var(--lc-primary)" opacity="0.75">
        <RightPanel :open-right-panel="openRightPanel" :action-params="actionParams" @close="() => {
          openRightPanel = !openRightPanel;
        }
          " @openDialog="() => {
    openRightPanel = false;
    openDialog = true;
  }
    "></RightPanel>
      </v-overlay>
    </div>
  </div>
</template>
<script>
import RightPanel from './RightPanel.vue';
import axios from 'axios';
import {
  DatePicker,
  SearchBar,
  //BreadCrumb
} from '@lenders-cooperative/los-app-ui-component-lib';

export default {
  components: {
    RightPanel,
    DatePicker,
    SearchBar,
    //BreadCrumb
  },
  props: ['schema'],
  data() {
    return {
      search: '',
      pagination: {
        page: 1,
        itemsPerPage: 4,
        totalItems: 0
      },
      openRightPanel: false,
      currentStep: 1,
      currentJobName: '',
      showJobTable: true,
      showActionsBreadcrumb: false,
      el: 1,
      showFilter: false,
      filterOptions: [
        { label: 'Fail', value: 'fail' },
        { label: 'Pass', value: 'pass' },
        { label: 'Skipped', value: 'skipped' },
      ],
      selectedFilters: [],
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
      selectedDates: {
        start: null,
        end: null
      },
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
          text: 'Transform Name',
          value: 'transform_name',
          sortable: false,
          // filterable: false,
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
          // filterable: false,
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
  watch: {
    selectedDates: {
      handler(newVal) {

        if (newVal.start && newVal.end) {
          this.fetchData();
        }
        else if (!newVal.start && !newVal.end) {
          this.fetchData();
        }
      },
      deep: true
    },
    search(newSearchValue) {
      if (newSearchValue && newSearchValue.length > 4) {
        let url = `http://127.0.0.1:8000/fmjobevent/?job_name=${newSearchValue}`
        console.log('URL is : ', url)
        this.searchByJobName(url);
      }
      else if (newSearchValue.length == 0) {
        this.fetchData()
      }
    },
    schema() {
      this.fetchData();
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
    modifyDate(date) {
      console.log("modifyDate method")
      console.log(" Date before change: ", date)
      const syear = date.getFullYear();
      const smonth = String(date.getMonth() + 1).padStart(2, "0");
      const sday = String(date.getDate()).padStart(2, "0");
      date = `${syear}-${smonth}-${sday}`;
      console.log("Date after change: ", date)
      return date

    },
    // updateDateRange() {
    //   if (this.selectedDates) {
    //     //start date modification
    //     console.log("updateDateRange method")
    //     let startDate = this.selectedDates.start;
    //     startDate = this.modifyDate(startDate)
    //     let endDate = this.selectedDates.end;
    //     endDate = this.modifyDate(endDate)
    //     let url = `http://127.0.0.1:8000/fmjobevent/?start_tms=${startDate}&end_tms=${endDate}`;
    //     this.callApiWithDate(url);
    //   }
    // },
    fetchData() {
      if (!this.selectedFilters.length && !this.selectedDates.start && !this.selectedDates.end) {
        axios
          .get(`http://127.0.0.1:8000/fmjobevent/?page=${this.pagination.page}&page_size=${this.pagination.itemsPerPage}`)
          .then((response) => {
            this.items = response.data.results;
            console.log(response.data)
            this.pagination.totalItems = response.data.count;
            console.log(this.items);
          })
          .catch((error) => {
            console.error(error);
          });
        console.log("Fetch Data API - ENDED")
      }
      else if (this.selectedFilters.length && !this.selectedDates.start && !this.selectedDates.end) {
        console.log(this.selectedFilters)
        axios
          .get(`http://127.0.0.1:8000/fmjobevent/?status=${this.selectedFilters}&page=${this.pagination.page}&page_size=${this.pagination.itemsPerPage}`)
          .then((response) => {
            this.items = response.data.results;
            console.log(response.data)
            this.pagination.totalItems = response.data.count;
            console.log(this.items);
          })
          .catch((error) => {
            console.error(error);
          });
        console.log("Fetch Data API - ENDED")
      }
      else if (this.selectedDates.start && this.selectedDates.end && !this.selectedFilters.length) {
        //start date modification
        console.log("updateDateRange method")
        let startDate = this.selectedDates.start;
        startDate = this.modifyDate(startDate);
        let endDate = this.selectedDates.end;
        endDate = this.modifyDate(endDate);
        axios
          .get(`http://127.0.0.1:8000/fmjobevent/?start_tms=${startDate}&end_tms=${endDate}&page=${this.pagination.page}&page_size=${this.pagination.itemsPerPage}`)
          .then((response) => {
            this.items = response.data.results;
            console.log(response.data)
            this.pagination.totalItems = response.data.count;
            console.log(this.items);
          })
          .catch((error) => {
            console.error(error);
          });
        console.log("Fetch Data API - ENDED")
      }
      else if (this.selectedDates.start && this.selectedDates.end && this.selectedFilters) {
        console.log("updateDateRange method")
        let startDate = this.selectedDates.start;
        startDate = this.modifyDate(startDate)
        let endDate = this.selectedDates.end;
        endDate = this.modifyDate(endDate);
        axios
          .get(`http://127.0.0.1:8000/fmjobevent/?status=${this.selectedFilters}&start_tms=${startDate}&end_tms=${endDate}&page=${this.pagination.page}&page_size=${this.pagination.itemsPerPage}`)
          .then((response) => {
            this.items = response.data.results;
            console.log(response.data)
            this.pagination.totalItems = response.data.count;
            console.log(this.items);
          })
          .catch((error) => {
            console.error(error);
          });
        console.log("Fetch Data API - ENDED")
      }
    }
    ,
    // callApiWithDate(url) {
    //   console.log("callApiWithDate API - STARTED")
    //   axios(url)
    //     .then((response) => {
    //       this.items = response.data.results;
    //       console.log(this.item);
    //     })
    //     .catch((error) => {
    //       console.error(error);
    //     });
    //   console.log("callApiWithDate API - ENDED")
    // },
    searchByJobName(url) {
      console.log("searchByJobName API - STARTED")
      axios(url)
        .then((response) => {
          this.items = response.data.results;
          // console.log("Response Data : ",this.items);
        })
        .catch((error) => {
          console.error(error);
        });
      console.log("searchByJobName API - ENDED")
    },


    getActions(jobEventId, jobname) {
      this.currentJobName = jobname;
      this.currentStep = 2;
      this.showActionsBreadcrumb = true;
      this.showJobTable = false;
      this.currentJobEventId = jobEventId;
      axios(
        `http://127.0.0.1:8000/fmjobactionevent/?fm_job_event_id=${jobEventId}`
      ).then((res) => {
        console.log(res.data)
        this.jobDescItems = res.data.results;
      });
      this.el = 2;
    },
    async getResolvedActionParams(actionId) {
      console.log("getResolvedActionParams - STARTED")
      await axios
        .get(
          `http://127.0.0.1:8000/fmjobactionevent/?fm_job_event_id=${this.currentJobEventId}&fm_job_action_event_id=${actionId}`
        )

        .then((response) => {
          this.actionParams = response.data.results[0].resolved_action_parms.params;
          console.log(this.actionParams);
        })
        .catch((error) => {
          console.error(error);
        });
      this.drawer = true;
      this.openRightPanel = true;
      console.log("getResolvedActionParams - ENDED")
    },
    changeShowTableValue() {
      console.log("Job table value : ", this.showJobTable)
      this.showJobTable = !this.showJobTable
      console.log("Job table value : ", this.showJobTable)
    },
    applyFiltersJobActions() {
      console.log('Selected Filters:', this.selectedFilters);
      // if (source == 'jobEvents') {
      //   const url = `http://127.0.0.1:8000/fmjobevent/?status=${this.selectedFilters}`
      //   this.searchEventsByStatus(url);
      // }
      // else if (source == 'jobActions') {
      const url = `http://127.0.0.1:8000/fmjobactionevent/?fm_job_event_id=${this.currentJobEventId}&status=${this.selectedFilters}`
      console.log("Status Type URL is : ", url)
      this.searchActionsByStatus(url);
      // }

    },
    searchActionsByStatus(url) {
      console.log("searchActionsByStatus API - STARTED")
      axios(url)
        .then((response) => {
          // this.$attrs.fmJobs = response.data;
          this.jobDescItems = response.data.results;
          // console.log("Response Data : ",this.items);
        })
        .catch((error) => {
          console.error(error);
        });
      console.log("searchActionsByStatus API - ENDED")
    },
    // searchEventsByStatus(url) {
    //   console.log("searchEventsByStatus API - STARTED")
    //   axios(url)
    //     .then((response) => {
    //       // this.$attrs.fmJobs = response.data;
    //       this.items = response.data.results;
    //       // console.log("Response Data : ",this.items);
    //     })
    //     .catch((error) => {
    //       console.error(error);
    //     });
    //   console.log("searchEventsByStatus API - ENDED")
    // }
  },
  created() {
    this.fetchData();
  },

};
</script>
<style scoped>
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

.container {
  display: inline-block;
}

.datepicker {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-top: 20px;
  margin-right: 600px;
}

/* .datepicker > * {
    margin-right: 250px;
  } */

.stepper-header {
  background-color: var(--lc-text-light);
  box-shadow: none;
}

.stepcontainer {
  display: flex;
  justify-content: space-between;
  margin-top: 2vh;
  border: none;
  background-color: var(--lc-text-light);
}

.step1 {
  width: 200px;
  height: 50px;
  background-color: #4673ae;
  clip-path: polygon(0% 0%, 88% 0%, 100% 50%, 88% 100%, 0% 100%);
  padding: 0.5rem 1rem 0.5rem 1rem;
  text-align: center;
  margin-right: 30px;
  font-size: large;
  color: var(--lc-text-light) !important;
}

.step2 {
  margin-right: 30px;
  width: 200px;
  height: 50px;
  background-color: #4673ae;
  clip-path: polygon(0% 0%, 88% 0%, 100% 50%, 88% 100%, 0% 100%);
  padding: 0.5rem 1rem 0.5rem 1rem;
  text-align: center;
  font-size: large;

}

.filter-icon {
  margin-left: 5px;
  color: var(--lc-primary);
}

.filter-box {
  margin-top: 10px;
}

.applyButton {
  margin-left: 10px;
}
</style>
