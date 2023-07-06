<template>

  <BreadCrumb :items="items"></BreadCrumb>
  <!-- <h1>This is job execution page</h1> -->

</template>
<script>
import {

  BreadCrumb,
  
} from '@lenders-cooperative/los-app-ui-component-lib';

export default {
  components: { 
    BreadCrumb    
   },
   data(){
    return{
    items : [{text : 'home','status' : 'completed','href' : '','disabled'  : true}]
   }}}
  </script>