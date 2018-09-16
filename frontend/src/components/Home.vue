<template>
  <div>
    <p>Home page</p>
    <v-container grid-list-md text-xs-center align-center>
      <v-layout row wrap>
        <br>
        <v-flex xs12 sm6 md3>
          <v-text-field
            class="text-xs-center"
            label="Artikel-link, Tweet-link oder Tweet-id einfügen..."
            placeholder="https://twitter.com/i/web/status/1038073678058139648"
            id="userinput"
            v-model="input"
            @input="updateInput()"
          ></v-text-field>
        </v-flex>
        <br>
      </v-layout>
    </v-container>
    <dnn />
    <create_bow />
    <get_bow />
    <scrape />
    <complete_analysis />
    <template>
      <vue-flip :active-hover="true" width="200px" height="50px" class="simple-test">
        <div slot="front">test </div>
        <slot name="back">test </slot>
      </vue-flip>
    </template>
  </div>
</template>

<script>
  import DNN from './Analysis/DNN'
  import CreateBow from './Analysis/CreateBow'
  import GetBowResult from './Analysis/GetBowResult'
  import Scrape from './Analysis/Scrape'
  import CompleteAnalysis from './Analysis/CompleteAnalysis'
  import VueFlip from '../../node_modules/vue-flip'
  import { dataBus } from "../main";

  export default {
    components: {
      'dnn': DNN,
      'create_bow':  CreateBow,
      'get_bow': GetBowResult,
      'scrape': Scrape,
      'complete_analysis': CompleteAnalysis,
      'vue-flip': VueFlip
    },
    props: ['input'],
    data() {
      return {
      }
    },
    methods: {
      updateInput() {
        console.log(this.input);
        dataBus.$emit('get_input', this.input)
      }
    }
  }
</script>

<style scoped>

  .simple-test div .front {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #673AB7;
    color: white;
  }

  .simple-test .back {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #FFC107;
    color: white
  }
</style>
