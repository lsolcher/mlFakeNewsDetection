<template>
  <div>
    <v-app>
      <h2>Fake News Detection</h2>
      <v-container grid-list-md text-xs-center align-center >
          <v-flex xs12 sm12 md12 mt-5 mb-5>
            <vue-flip :active-hover="true" width=100% height="100px" class="simple-test">
              <div slot="front">how to </div>
              <div slot="back">URL eingeben, die auf einen Link oder einen Tweet verweist. Der Link kann nach Wortähnlichkeit (BoW-Modell), nach Textstilanalyse mit Deep Neural Networks oder nach beiden Methoden untersucht werden. Ist die Eingabe ein Tweet, wird in die Analyse zusätzlich der Tweet-Text und die Daten des Tweeters miteinbezogen. Um die Güte der Wortähnlichkeit zu erhöhen, wird empfohlen, vor Analyse die Datenbank und das Bow-Modell zu aktualisieren.</div>
            </vue-flip>
          </v-flex>
           <v-flex xs12 sm12 md12 offset -sm3 mb-3>
            <v-text-field
              class="text-xs-center"
              label="Artikel-link, Tweet-link oder Tweet-id einfügen..."
              placeholder="https://twitter.com/i/web/status/1038073678058139648"
              id="userinput"
              v-model="input"
              @input="updateInput()"
            ></v-text-field>
          </v-flex>
        <v-layout row wrap>
          <v-flex xs6 sm6 md6>
            <scrape />
          </v-flex>
          <v-flex xs6 sm6 md6>
            <create_bow />
          </v-flex>
          <v-flex xs6 sm6 md6>
            <get_bow />
          </v-flex>
          <v-flex xs6 sm6 md6>
            <dnn />
          </v-flex>
          <v-flex xs12 sm12 md12>
          <complete_analysis />
          </v-flex>
          <v-flex xs12 sm12 md12>

          </v-flex>
        </v-layout>
        <v-flex  xs12 sm12 md12 mt-5>
          <vue-flip :active-hover="true" width=100% height="50px" class="simple-test">
            <div slot="front">about </div>
            <div slot="back">&#9400; Lucas Solcher <br> <a href="mailto:l.solcher@gmail.com">Mail</a> </div>
          </vue-flip>
        </v-flex>
      </v-container>
    </v-app>
  </div>
</template>

<script>
  import DNN from './Analysis/DNN'
  import CreateBow from './Analysis/CreateBow'
  import GetBowResult from './Analysis/GetBowResult'
  import Scrape from './Analysis/Scrape'
  import CompleteAnalysis from './Analysis/CompleteAnalysis'
  import VueFlip from '../../node_modules/vue-flip'
  import { dataBus } from "../main";

  export default {
    components: {
      'dnn': DNN,
      'create_bow':  CreateBow,
      'get_bow': GetBowResult,
      'scrape': Scrape,
      'complete_analysis': CompleteAnalysis,
      'vue-flip': VueFlip
    },
    props: ['input'],
    data() {
      return {
      }
    },
    methods: {
      updateInput() {
        console.log(this.input);
        dataBus.$emit('get_input', this.input)
      }
    }
  }
</script>

<style>

  .flipper .front {
    background: hotpink;
  }
  .simple-test div .front {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #6B5B95;
    color: white;
  }

  .simple-test .back {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #6B5B95;
    color: white
  }
</style>
