<template>
  <div class="d-flex">
    <v-navigation-drawer height="100vh" class="pt-5 navDrawer w-25" permanent>
      <div class="px-5 pb-4">
        <span class="fs-3">Admin Console</span>
        <div class="small">Select Schema</div>
        <v-select
          v-model="selectedOption"
          class="py-0 my-0 text-white"
          color="white"
          background-color="var(--lc-secondary)"
          dark
          height="45"
          hide-details
          solo
          :items="options"
        ></v-select>
      </div>

      <v-list>
        <template v-for="item in items">
          <v-list-item
            class="px-5 text-white"
            :class="item.id == selectedTab ? 'activeTab' : ''"
            :key="item.id"
            link
            @click="handleClick(item)"
          >
            <v-list-item-icon>
              <v-icon class="text-white">{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-divider
            :key="item.id"
            :thickness="10"
            class="my-0"
            color="var(--lc-secondary)"
          ></v-divider>
        </template>
      </v-list>
    </v-navigation-drawer>
    <div class="bg-light p-5 w-75">
      <div class="bg-white h-100 p-4">
        <component :is="items[selectedTab].type"></component>
      </div>
    </div>
  </div>
</template>

<script>
import ConfiguringJobs from './ConfiguringJobs.vue';
import JobHistory from './JobHistory.vue';
import TerminatingJobs from './TerminatingJobs.vue';
import TriggeringJobs from './TriggeringJobs.vue';
import RightPanel from './RightPanel.vue';

export default {
  components: {
    ConfiguringJobs,
    JobHistory,
    TerminatingJobs,
    TriggeringJobs,
    RightPanel,
  },
  data: () => ({
    items: [
      {
        id: 0,
        icon: 'mdi-email',
        title: 'Configuring Jobs',
        type: 'ConfiguringJobs',
      },
      {
        id: 1,
        icon: 'mdi-account-supervisor-circle',
        title: 'Triggering Jobs',
        type: 'TriggeringJobs',
      },
      {
        id: 2,
        icon: 'mdi-clock-start',
        title: 'Terminating Jobs',
        type: 'TerminatingJobs',
      },
      {
        id: 3,
        icon: 'mdi-history',
        title: 'Job History',
        type: 'JobHistory',
      },
    ],
    options: ['DLAP', 'Bar', 'Fizz', 'Buzz'],
    selectedOption: 'DLAP',
    selectedTab: 0,
  }),
  methods: {
    handleClick(item) {
      this.selectedTab = item.id;
    },
  },
};
</script>

<style scoped>
.navDrawer {
  background-color: var(--lc-primary);
  color: white;
  min-height: 100%;
  min-width: 25%;
}
.activeTab,
.v-input__slot,
.v-list-item:hover {
  background-color: var(--lc-secondary) !important;
  color: white;
}
</style>
