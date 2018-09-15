<template>
  <!-- DNN ANALYSIS -->
  <div>
  <template v-if="!dnnAnalysisDone">
    <p>Analysiere Link...</p>
    <v-progress-circular
      indeterminate
      color="primary"
    ></v-progress-circular>
  </template>
  <template v-else>
    <v-btn
      @click="getDNNAnalysisResult()"
    >Artikel nach Textstil analysieren</v-btn> <!-- :disabled="input === ''" !-->
    <p>{{dnnAnalysisOutput}}</p>
  </template>
  </div>
</template>

<script>
  import axios from 'axios'
  import { dataBus } from "../../main";

  export default {
    name: 'dnn',
    data() {
      return {
        dnnAnalysisOutput: '',
        dnnAnalysisDone: true,
        input: ''
      }
    },
    methods: {
      // ---- DNN ---- //
      getDNNAnalysisResult() {
        this.dnnAnalysisDone = false;
        console.log('INPUT: ' + this.input);
        this.dnnAnalysisOutput = this.getDNNAnalysisResultFromBackend()
      },
      getDNNAnalysisResultFromBackend() {
        const path = 'http://localhost:5000/api/analyzeDNN';
        axios.get(path, {
          params: {
            input: this.input
          }
        })
          .then(response => {
            this.dnnAnalysisOutput = response.data;
            console.log(this.dnnAnalysisOutput);
            this.dnnAnalysisDone = true
          })
          .catch(error => {
            console.log(error);
            this.dnnAnalysisDone = true
          })
      }
    },
    mounted() {
      dataBus.$on('get_input', (input) => {
        this.input = input;
      });
    }
  }
</script>
