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
      </template>
      <template v-else>
        <v-btn block color="info"
          @click="getAnalysisResult()"
          :disabled="input === ''"
        >Tweet oder Artikel auf Wortähnlichkeit untersuchen</v-btn>
        <template v-if="output.value">
          <p v-if="output.value === -1" >{{"Die Eingabe verlinkt auf keinen Tweet oder Link"}}</p>
          <p v-else-if="output.value > 0.33"style="color:green;"> <img src="../../assets/trump_sad.jpg" width="80%">  <br /> Nach Wortähnlichkeitsanalyse wurden Artikel in der Datenbank gefunden! <span v-html="link"></span> um den Artikel aufzurufen. (Cosinus-Ähnlichkeit: {{output.value}}) Dieser Artikel ist wahrscheinlich so oder in ähnlicher Form schon erschienen. </p>
          <p v-else style="color:red;" > <img src="../../assets/trump_happy.jpg" width="100%">  Nach Wortähnlichkeitsanalyse wurden keine ähnlichen Artikel in der Datenbank gefunden! <span v-html="link"></span> um den "ähnlichsten" Artikel in der Datenbank aufzurufen. (Cosinus-Ähnlichkeit: {{output.value}}). Dieser Artikel ist so oder in ähnlicher Form nicht in der Datenbank vorhanden.</p>
        </template>
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
        input: '',
        link: ''
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
            this.link = String(this.output.url).replace(/\"/g, '');
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
