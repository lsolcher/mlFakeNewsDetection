<template>
  <div>
    <!-- GET BOW ANALYSIS -->
    <template v-if="!getBowDone">
      <p>Analysiere Link...</p>
      <v-progress-circular
        indeterminate
        color="primary"
      ></v-progress-circular>
    </template>
    <template v-else>
      <v-btn
        @click="getBOWAnalysisResult()"
        :disabled="input === ''"
      >Link auf Wortähnlichkeit untersuchen</v-btn>
      <p>{{getBowOutput}}</p>
    </template>
  </div>
</template>

<script>
  import axios from 'axios'
  import { dataBus } from "../../main";


  export default {
    name: 'get_bow',
    data() {
      return {
        getBowOutput: '',
        getBowDone: true,
        input: ''
      }
    },
    methods: {
      // ---- GET BOW MODEL ---- //
      getBOWAnalysisResult() {
        this.getBowDone = false;
        console.log(this.input);
        this.getBowOutput = this.getBOWResultFromBackend()
      },
      getBOWResultFromBackend() {
        const path = 'http://localhost:5000/api/getBOW';
        axios.get(path, {
          params: {
            input: this.input
          }
        })
          .then(response => {
            this.getBowOutput = response.data.result;
            console.log(this.getBowOutput);
            this.getBowDone = true;
          })
          .catch(error => {
            console.log(error);
            this.getBowDone = true
          })
      },
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
    },
    mounted() {
      dataBus.$on('get_input', (input) => {
        this.input = input;
      });
    }
  }
</script>
