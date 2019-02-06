<template>
    <div>
      <!-- GET BOW ANALYSIS -->
      <template v-if="!done">
        <p>Analysiere Link nach Textstil und Metadaten..</p>
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
      </template>
      <template v-else>
        <v-btn block color="info"
          @click="getCompleteResult()"
          :disabled="input === ''"
        >Tweet oder Artikel nach Textstil, Metadaten und Wortähnlichkeit untersuchen</v-btn>
        <template v-if="output && output.dnn_result[0]">
          <p v-if="output.dnn_result[0] === -1" >Die Eingabe verlinkt auf keinen Tweet oder Link oder der Tweet verlinkt auf keinen Artikel.</p>
          <template v-else-if="output.dnn_result[0] < 0.5 && output.bow_value[0] > 0.33"> <img src="../../assets/trump_sad.jpg" width="25%">
            <p style="color:green;">Der Tweet beinhaltet sehr wahrscheinlich keine Fake News! Es wurde sowohl ein ähnlicher Artikel in der Datenbank gefunden (<span v-html="output.bow_url[0]"></span>), als auch eine niedrige
              Wahrscheinlichkeit von Fake News aufgrund der Textstil-, und Metadatenanalyse ermittelt ({{output.dnn_result[0]*100}}%)</p></template>
          <template v-else-if="output.dnn_result[0] < 0.5 && output.bow_value[0] <= 0.33"> <img src="../../assets/trump_sad.jpg" width="25%">
            <p style="color:orange;">Der Tweet beinhaltet wahrscheinlich keine Fake News! Es wurde zwar kein ähnlicher Artikel in der Datenbank gefunden,
              die Metadaten- und Textstilanalyse ergibt aber eine geringe Wahrscheinlichkeit von Fake News ({{output.dnn_result[0]*100}}%). Dennoch ist Vorsicht geboten!</p></template>
          <template v-else-if="output.dnn_result[0] >= 0.5 && output.bow_value[0] > 0.33"> <img src="../../assets/trump_sad.jpg" width="25%">
            <p style="color:orange;"> Der Tweet beinhaltet wahrpcheinlich keine Fake News! Zwar ermittelt die Metadaten- und Textstilanalyse eine hohe Ähmlichkeit zu Fake News ({{1- output.dnn_result[0]}}),
              es wurde aber ein ähnlicher Artikel in der Datenbank gefunden (<span v-html="output.bow_url[0]"></span>). Dennoch ist Vorsicht geboten!</p></template>
          <template v-else><img src="../../assets/trump_happy.jpg" width="25%">
            <p style="color:red;">Vorsicht, der Link könnte auf Fake News verweisen! Es wurde kein ähnlicher Artikel in der Datenbank gefunden UND
              die Metadaten- und Textstilanalyse eine hohe Ählichkeit zu Fake News ({{output.dnn_result[0]*100}}%). </p></template>
        </template>
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
            console.log(this.output.dnn_result[0]);
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
