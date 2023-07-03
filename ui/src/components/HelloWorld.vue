<template>
  <SideMenuPage :options="options">
    <template v-slot:menu-header>
      <div class="d-flex flex-column p-3">
        <h3>Admin Console</h3>
        <span class="small">Select Schema</span>
        <Dropdown
          v-model="selectedSchema"
          :items="schemaOptions"
          background-color="var(--lc-secondary)"
          hide-details
          dark
          solo
        ></Dropdown>
      </div> </template
  ></SideMenuPage>
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
          icon: 'fa-memo-circle-info',
          component: ConfiguringJobs,
          props:{fmJobs: this.fmJobs},
        },
        {
          textKey: 'Job Execution',
          icon: 'fa-sensor-triangle-exclaimation',
          component: JobExecution,
        },
        {
          textKey: 'Job Termination',
          icon: 'fa-users-rectangle',
          component: JobTermination,
        },
        {
          textKey: 'Job History',
          icon: 'fa-clock-rotate-left',
          component: JobHistory,
        },
      ]
    },
},
  watch: {
    async selectedSchema() {
      try {
        const payload = {
          schema_name: this.selectedSchema,
        };

        const response = await axios.post(
          'http://127.0.0.1:8000/schema-names/',
          payload
        );
        this.getFmJobs();
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
      // window.location.reload();
    },
  },
  data() {
    return {
      selectedSchema: 'public',
      schemaOptions: [],
      fmJobs: [],
    };
  },
  methods: {
    async getSchemaNames() {
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
    getFmJobs(){
      axios.get('http://127.0.0.1:8000/fmjobs/').then((res) =>{
        this.fmJobs = res.data.results;
      }
      ).catch((err) =>{
        console.log(err)})
    },
  },
  created() {
    this.getSchemaNames();
    this.getFmJobs();
  },
};
</script>
<style scoped>
>>> .primary {
  background-color: var(--lc-primary);
}
>>> .side-menu {
  height: 100vh !important;
}

>>> .card-background {
  margin: 2rem !important;
  border-radius: 0;
  box-shadow: none !important;
}
</style>
