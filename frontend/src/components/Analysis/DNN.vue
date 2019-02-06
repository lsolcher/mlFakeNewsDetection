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
      <v-btn block color="info"
             :disabled="input === ''"
             :loading="!dnnAnalysisDone"
        @click="getDNNAnalysisResult()"
      >Tweet oder Artikel nach Textstil analysieren</v-btn>
      <template v-if="dnnAnalysisOutput">
        <p v-if="dnnAnalysisOutput === -1" >{{"Die Eingabe verlinkt auf keinen Tweet oder Link"}}</p>
        <p v-else-if="dnnAnalysisOutput < 0.5" style="color:green;"> <img src="../../assets/trump_sad.jpg" width="100%"> Nach Textstilanalyse beinhaltet der Artikel wahrscheinlich keine Fake News! Die errechnete Wahrscheinlichkeit beträgt {{1 - dnnAnalysisOutput}}%.</p>
        <p v-else style="color:red;"><img src="../../assets/trump_happy.jpg" width="100%"> Nach Textstilanalyse beinhaltet der Artikel wahrscheinlich Fake News! Die errechnete Wahrscheinlichkeit beträgt {{1 - dnnAnalysisOutput}}%.</p>
      </template>
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
            this.dnnAnalysisOutput = response.data.result;
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
