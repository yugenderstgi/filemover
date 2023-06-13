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
        ></v-text-field>
      </div>
    </div>
    <v-stepper v-model="el" flat>
      <v-stepper-items>
        <v-stepper-content step="1">
          <v-data-table
            class="mt-5 pt-5 customTableHeader"
            :headers="headers"
            dense
            :search="search"
            :custom-filter="filterByJobId"
            :items="items"
            item-key="jobId"
          >
            <template v-slot:item="{ item }">
              <tr class="zebra-stripe-row">
                <td>{{ item.id }}</td>
                <td>{{ item.name }}</td>
                <td>{{ item.dml_ts }}</td>
                <td>
                  <button class="small smallBtn" @click="fetchIdJob">
                    View Action
                  </button>
                </td>
              </tr>
            </template>
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
                <td>{{ item.id }}</td>
                <td>{{ item.name }}</td>
                <td>{{ item.dml_ts }}</td>
                <td>
                  <button class="small smallBtn" @click="openDrawer()">
                    View Actions Params
                  </button>
                </td>
                <td>
                  <button
                    class="small smallBtn"
                    @click="
                      () => {
                        openDialog = !openDialog;
                      }
                    "
                  >
                    Edit
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
    <v-overlay :value="openDialog" color="var(--lc-primary)" opacity="0.75">
      <v-dialog v-model="openDialog" max-width="900">
        <v-card class="px-5 py-3" light>
          <div class="d-flex flex-column">
            <span class="fs-3 header">Edit FM_Action 15 Details</span>
            <div class="d-flex gap-3">
              <div class="d-flex flex-column flex-grow-1">
                <span class="small">Action Type</span>
                <v-select
                  class="py-0 my-0 text-white inputBox"
                  hide-details
                  dense
                  solo
                  :items="options"
                ></v-select>
              </div>
              <div class="d-flex flex-column flex-grow-1">
                <span class="small">Action ID</span>
                <v-text-field
                  class="inputBox"
                  label="1"
                  solo
                  single-line
                  dense
                  hide-details
                ></v-text-field>
              </div>
              <div class="d-flex flex-column flex-grow-1">
                <span class="small">Sequence</span>
                <v-text-field
                  class="inputBox"
                  label="1"
                  solo
                  single-line
                  dense
                  hide-details
                ></v-text-field>
              </div>
            </div>
            <v-textarea label="Label"></v-textarea>
          </div>
          <div>
            <span class="fs-3 header">Action Params</span>
            <v-row>
              <v-col
                ><span class="small">transform_name</span
                ><v-text-field
                  class="inputBox"
                  label="Get
              country File"
                  solo
                  single-line
                  dense
                  hide-details
                ></v-text-field
              ></v-col>
              <v-col
                ><span class="small">local_location</span
                ><v-text-field
                  class="inputBox"
                  label="Home/sere/.sdg"
                  solo
                  single-line
                  dense
                  hide-details
                ></v-text-field
              ></v-col>
              <v-col
                ><span class="small">transform_name</span
                ><v-text-field
                  class="inputBox"
                  label="Get
              country File"
                  solo
                  single-line
                  dense
                  hide-details
                ></v-text-field
              ></v-col>
            </v-row>
            <v-row>
              <v-col
                ><span class="small">transform_name</span
                ><v-text-field
                  class="inputBox"
                  label="Get
              country File"
                  solo
                  single-line
                  dense
                  hide-details
                ></v-text-field
              ></v-col>
              <v-col
                ><span class="small">local_location</span
                ><v-text-field
                  class="inputBox"
                  label="Home/sere/.sdg"
                  solo
                  single-line
                  dense
                  hide-details
                ></v-text-field
              ></v-col>
            </v-row>
          </div>
          <div class="d-flex justify-content-end">
            <button>Cancel</button>
            <button>Save</button>
          </div>
        </v-card></v-dialog
      ></v-overlay
    >
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
      drawer: false,
      search: '',
      openDialog: false,
      options: ['Foo', 'Bar', 'Fizz', 'Buzz'],
      headers: [
        {
          text: 'Job_ID',
          value: 'id',
          sortable: false,
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
      ],
      items: [],
    };
  },
  methods: {
    openDrawer() {
      this.drawer = true;
    },
    fetchJob() {
      // makes axios call and get res
      //this.items = res;
    },
    fetchIdJob() {
      // makes axios call for that particular id
      this.el = 2;
    },
    filterByJobId(value, search, item) {
      console.log(value, search, item);
    },
  },
  created() {
    axios.get('http://127.0.0.1:8000/fmjobs')
  .then(response => {
    this.items=response.data
    console.log(this.item);
  })
  .catch(error => {
    console.error(error);
  });

  },
};
</script>
<style scoped>
.customTableHeader >>> thead.v-data-table-header tr {
  border-bottom: 2px solid var(--lc-primary);
  font-size: 1.5rem;
}

.inputBox {
  padding: 0;
  border: 2px solid var(--lc-primary);
  border-radius: 0px;
}
.v-icon {
  background-color: var(--lc-primary);
  color: white;
}
</style>
