import Vue from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import '@lenders-cooperative/los-app-ui-component-lib/dist/style.css';
import 'bootstrap/dist/css/bootstrap.css';
import '@fortawesome/fontawesome-free/css/all.css';
import './project.css';

Vue.config.productionTip = false;
new Vue({
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
