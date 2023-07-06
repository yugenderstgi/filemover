<template>
    <header>
        <div class="header-container">
        <img src="../assets/lc.png" alt="Logo" class="logo">
        <div class="text">
      <span class="name">LENDERS</span>
        <span class="sname">COOPERATIVE</span></div>
    </div>
      <!-- <div class="user-icon">

        <i class="mdi mdi-account-circle"></i>
        <i class="user-class">Brajput</i>
        <i class="mdi mdi-triangle-down mr-4"></i>
        <i class="mdi mdi-earth"></i>
        <i class="user-class">En</i>
        <i class="mdi mdi-triangle-down"></i>


    </div>  -->
  

    </header>
  </template>

<script>
import {

  //Dropdown,DropdownButton
  //Btn
} from '@lenders-cooperative/los-app-ui-component-lib';
export default {
  components: { 
    // Dropdown,
    // DropdownButton,
    //Btn   
   }}
</script>

<style scoped>
header {
  display: flex;
  background-color: var(--lc-bg-light);
  padding: 10px;
  /* justify-content: space-between; */
}
.user-icon i {
  font-size: 17px;
  margin-right: 2px;
  align-self: flex-end;
  /* margin-right: 10px */
}
.user-class{
    margin-right: 15px;
    /* font-size: 10px; */
}

.logo {
  height: 60px;
  /* margin-left: 5px; */
}
.entity-class {
  height: 29px;
  /* margin-left: 5px; */
}
.name {
font-weight: 750;
color: var(--lc-primary);
font-size: 21px;
letter-spacing: 0.30em;
}

.sname{
color: var(--lc-primary);
font-size: 20px;
margin-top: -0.5em;
letter-spacing: 0.01em;
}

.header-container {
  display: flex;
  gap: 5px;
  align-self: flex-start;
}

.text{
    display: flex;
    flex-direction: column;
}
</style>