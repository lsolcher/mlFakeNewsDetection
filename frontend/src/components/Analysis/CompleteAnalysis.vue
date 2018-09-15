<template>
  <div>
    <!-- GET BOW ANALYSIS -->
    <template v-if="!done">
      <p>Analysiere Link nach allen Methoden...</p>
      <v-progress-circular
        indeterminate
        color="primary"
      ></v-progress-circular>
    </template>
    <template v-else>
      <v-btn
        @click="getCompleteResult()"
        :disabled="input === ''"
      >Link nach allen Methoden untersuchen</v-btn>
      <ul>
        <p v-for="(item, index) in output.url"> <span v-html="output.url[index]"></span> : {{output.value[index]}}</p>
      </ul>

    </template>
  </div>
</template>

<script>
  import axios from 'axios'
  import { dataBus } from "../../main";


  export default {
    data() {
      return {
        output: '',
        done: true,
        input: ''
      }
    },
    methods: {
      // ---- GET COMPLETE RESULT ---- //
      getCompleteResult() {
        this.done = false;
        console.log(this.input);
        this.output = this.getCompleteResultFromBackend()
      },
      getCompleteResultFromBackend() {
        const path = 'http://localhost:5000/api/getCompleteResult';
        axios.get(path, {
          params: {
            input: this.input
          }
        })
          .then(response => {
            this.output = response.data;
            console.log(this.output);
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
