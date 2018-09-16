<template>
  <div>
    <!-- GET BOW ANALYSIS -->

    <!-- currently analysing -->
    <template v-if="!done">
      <p>Analysiere Link...</p>
      <v-progress-circular
        indeterminate
        color="primary"
      ></v-progress-circular>
      <ul>
        <p v-for="(item, index) in output.url"> <span v-html="output.url[index]"></span> : {{output.value[index]}}</p>
      </ul>
    </template>



    <template v-else>
      <v-btn
        @click="getAnalysisResult()"
        :disabled="input === ''"
      >Link auf Wortähnlichkeit untersuchen</v-btn>

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
        output: '',
        done: true,
        input: ''
      }
    },
    methods: {
      // ---- GET BOW MODEL ---- //
      getAnalysisResult() {
        this.done = false;
        console.log(this.input);
        this.output = this.getAnalysisResultFromBackend()
      },
      getAnalysisResultFromBackend() {
        const path = 'http://localhost:5000/api/getBOW';
        axios.get(path, {
          params: {
            input: this.input
          }
        })
          .then(response => {
            this.output = response.data;
            console.log(this.output);
            console.log(typeof this.output);
            this.done = true;
          })
          .catch(error => {
            console.log(error);
            this.done = true
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
