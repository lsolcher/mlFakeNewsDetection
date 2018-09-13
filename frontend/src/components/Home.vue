<template>
  <div>
    <p>Home page</p>

    <v-container grid-list-md text-xs-center align-center>
      <v-layout row wrap>
        <br>
        <v-flex xs12 sm6 md3>
          <v-text-field
            class="text-xs-center"
            label="Artikel-link, Tweet-link oder Tweet-id einfügen..."
            placeholder="https://twitter.com/i/web/status/1038073678058139648"
            id="userinput"
            @keyup.enter="getDNNAnalysisResult()"
            v-model="input"
          ></v-text-field>
        </v-flex>
        <br>
      </v-layout>
    </v-container>
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
        :disabled="input === ''"
      >Artikel nach Textstil analysieren</v-btn>
      <p>{{dnnAnalysisOutput}}</p>
    </template>

    <template v-if="!bowAnalysisDone">
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
      >Ähnliche Artikel in Datenbank finden</v-btn>
      <p>{{bowAnalysisOutput}}</p>
    </template>

    <template v-if="!scrapingDone">
      <p>Aktualisiere Datenbank...</p>
      <v-progress-circular
        indeterminate
        color="primary"
      ></v-progress-circular>
    </template>
    <template v-else>
      <v-btn
        @click="scrape()"
      >Artikeldatenbank aktualisieren</v-btn>
      <p>{{scrapingOutput}}</p>
    </template>


  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    data() {
      return {
        randomNumber: 0,
        input: '',
        dnnAnalysisOutput: '',
        bowAnalysisOutput: '',
        scrapingOutput: '',
        dnnAnalysisDone: true,
        bowAnalysisDone: true,
        scrapingDone: true,
        progress: ''
      }
    },
    methods: {
      scrape() {
        this.scrapingDone = false;
        //this.updateProgress(); TODO
        this.scrapingOutput = this.getScrapingResultFromBackend()
      },
      getDNNAnalysisResult() {
        this.dnnAnalysisDone = false;
        console.log(this.input);
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
      },
      getBOWAnalysisResult() {
        this.dnnAnalysisDone = false;
        console.log(this.input);
        this.dnnAnalysisOutput = this.getBOWAnalysisResultFromBackend()
      },
      getBOWAnalysisResultFromBackend() {
        const path = 'http://localhost:5000/api/analyzeBOW';
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
      },
      getScrapingResultFromBackend() {
        const path = 'http://localhost:5000/api/scrape';
        axios.get(path)
          .then(response => {
            this.scrapingOutput = response.data.result;
            console.log(this.scrapingOutput);
            this.scrapingDone = true
          })
          .catch(error => {
            console.log(error);
            this.scrapingOutput = "Ein unerwarteter Fehler ist aufgetreten";
            this.scrapingDone = true
          })
      },
      //TODO:
      updateProgress() {
        setInterval(function () {
          this.readProgress();
        }.bind(this), 3000);
      },
      readProgress() {
        const path = 'http://localhost:5000/api/scrape_progress';
        axios.get(path)
          .then(response => {
            this.progress = response.data;
            console.log(response.data.result);
            console.log(this.progress)
          })
          .catch(error => {
            console.log(error);
          })
      }
    },
    created() {
      // this.getRandom();
      //this.getDNNAnalysisResult();
      //this.scrape()
    }
  }
</script>
