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
      <ul>
        <p v-for="(item, index) in bowOutput.url"> {{bowOutput.url[index]}} : {{bowOutput.value[index]}}</p>
      </ul>

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
        bowOutput: '',
        getBowDone: true,
        input: ''
      }
    },
    methods: {
      // ---- GET BOW MODEL ---- //
      getBOWAnalysisResult() {
        this.getBowDone = false;
        console.log(this.input);
        this.bowOutput = this.getBOWResultFromBackend()
      },
      getBOWResultFromBackend() {
        const path = 'http://localhost:5000/api/getBOW';
        axios.get(path, {
          params: {
            input: this.input
          }
        })
          .then(response => {
            this.bowOutput = response.data;
            console.log(this.bowOutput);
            console.log(typeof this.bowOutput);
            this.getBowDone = true;
          })
          .catch(error => {
            console.log(error);
            this.getBowDone = true
          })
      },
      killThreads() {
        let id = window.setTimeout(function() {}, 0);
        console.log(id);
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
