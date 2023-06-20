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
    selectedSchema() {
      return this.schemaOptions[0];
    },
  },
  data() {
    return {
      schemaOptions: ['dlap', 'dsf', 'dsf'],
      options: [
        {
          textKey: 'Job Configuration',
          icon: 'fa-memo-circle-info',
          component: ConfiguringJobs,
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
      ],
    };
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
