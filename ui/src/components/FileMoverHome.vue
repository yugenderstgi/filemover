<template>
  <SideMenuPage :options="options">
    <template v-slot:menu-header>
      <div class="d-flex flex-column p-3">
        <h3>Admin Console</h3>
        <span class="small">Select Schema</span>
        <Dropdown v-model="selectedSchema" :items="schemaOptions" background-color="var(--lc-secondary)" hide-details dark
          solo @change="changeSchema"></Dropdown>
      </div>
    </template>
  </SideMenuPage>
</template>

<script>
import axios from 'axios';
import {
  SideMenuPage,
  Dropdown,
} from '@lenders-cooperative/los-app-ui-component-lib';
import ConfiguringJobs from './ConfiguringJobs.vue';
import JobHistory from './JobHistory.vue';
import JobExecution from './JobExecution.vue';
import JobTermination from './JobTermination.vue';

export default {
  components: { SideMenuPage, Dropdown },
  computed: {
    options() {
      return [
        {
          textKey: 'Job Configuration',
          //icon: 'fa-memo-circle-info',
          icon: 'mdi mdi-database-cog',
          component: ConfiguringJobs,
          props: {
            // fmJobsProps: this.fmJobs,
            schema: this.schema
          },
        },
        {
          textKey: 'Job Execution',
          icon: 'mdi mdi-progress-clock',
          component: JobExecution,
        },
        {
          textKey: 'Job Termination',
          // icon: 'fa-users-rectangle',
          icon: 'mdi mdi-alert-octagon-outline',
          component: JobTermination,
        },
        {
          textKey: 'Job History',
          // icon: 'fa-clock-rotate-left',
          icon: 'mdi mdi-history',
          component: JobHistory,
          props: {
            // fmJobsProps: this.fmJobs,
            schema: this.schema
          },
        },
      ]
    },
  },
  // watch: {
  //   selectedSchema() {
  //     try {
  //       const payload = {
  //         schema_name: this.selectedSchema,
  //       };

  //       const response = axios.post(
  //         'http://127.0.0.1:8000/schema-names/',
  //         payload
  //       );
  //       console.log(response.data)
  //       this.getFmJobs();

  //     } catch (error) {
  //       console.error(error);
  //     }
  //     // window.location.reload();
  //   },
  // },
  data() {
    return {
      page: 1,
      pageSize: 4,
      selectedSchema: 'public',
      schemaOptions: [],
      // fmJobs: [],
      schema: {}
    };
  },
  methods: {
    async changeSchema() {
      try {
        const payload = {
          schema_name: this.selectedSchema,
        };
        const response = await axios.post(
          'http://127.0.0.1:8000/schema-names/',
          payload
        );
        this.schema = response
        // this.getFmJobs(this.pageSize, this.page);

      } catch (error) {
        console.error(error);
      }
    },
    getSchemaNames() {
      axios
        .get('http://127.0.0.1:8000/schema-names/')
        .then((response) => {
          // Handle the response data here
          this.schemaOptions = response.data.schema_names;
        })
        .catch((error) => {
          // Handle any errors that occur
          console.error(error);
        });
    },
    // getFmJobs(pageSize, page) {
    //   const url = `http://127.0.0.1:8000/fmjobs/?page=${page}&page_size=${pageSize}`
    //   axios.get(url).then((res) => {
    //     console.log(res.data)
    //     this.fmJobs = res.data.results;
    //   }
    //   ).catch((err) => {
    //     console.log(err)
    //   })
    // },
  },
  created() {
    this.getSchemaNames();
    // this.getFmJobs(this.pageSize, this.page);
    this.changeSchema();
  },
};
</script>
<style scoped>
>>>.primary {
  background-color: var(--lc-primary);
}

>>>.side-menu {

  height: 100vh !important;

}

>>>.card-background {
  margin: 2rem !important;
  border-radius: 0;
  box-shadow: none !important;
}
</style>