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

  export default {
    data() {
      return {
        getBowOutput: '',
        getBowDone: true,
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
      }
    }
  }
</script>
