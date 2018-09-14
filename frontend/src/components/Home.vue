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
            @keyup.enter="getDNNAnalysisResult()"
            v-model="input"
          ></v-text-field>
        </v-flex>
        <br>
      </v-layout>
    </v-container>
    <dnn />
    <create_bow />
    <get_bow />
    <scrape />
  </div>
</template>

<script>
  import axios from 'axios'
  import DNN from './Analysis/DNN'
  import CreateBow from './Analysis/CreateBow'
  import GetBowResult from './Analysis/GetBowResult'
  import Scrape from './Analysis/Scrape'

  export default {
    components: {
      'dnn': DNN,
      'create_bow':  CreateBow,
      'get_bow': GetBowResult,
      'scrape': Scrape
    },
    data() {
      return {
      }
    },
    methods: {
      killThreads() {
        let id = window.setTimeout(function() {}, 0);
        console.log(id)
        while (id--) {
          clearInterval(id);
        }
      }
    },
    created() {
      this.killThreads()
    }
  }
</script>
