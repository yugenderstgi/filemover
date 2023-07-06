<template>
  <div id="app" data-app>
    <HeaderView></HeaderView>
    <FileMoverHome></FileMoverHome></div>
</template>

<script>
// import HelloWorld from './components/HelloWorld';
import FileMoverHome from './components/FileMoverHome.vue';
import HeaderView from './components/HeaderView.vue'

export default {
  name: 'App',

  components: {
    FileMoverHome,
    HeaderView
  },

  data: () => ({
    //
  }),
};
</script>
