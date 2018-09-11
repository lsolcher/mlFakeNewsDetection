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
            @keyup.enter="getAnalysisResult()"
            v-model="input"
          ></v-text-field>
        </v-flex>
        <br>
      </v-layout>
    </v-container>
    <template v-if="!analysisDone">
      <v-progress-circular
        indeterminate
        color="primary"
      ></v-progress-circular>
    </template>
    <template v-else>
      <v-btn
        @click="getAnalysisResult()"
        :disabled="input === ''"
      >Analysieren</v-btn>
      <p>{{analysisOutput}}</p>
    </template>
    <template v-if="!scrapingDone">
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
        analysisOutput: '',
        scrapingOutput: '',
        analysisDone: true,
        scrapingDone: true
      }
    },
    methods: {
      scrape() {
        this.scrapingDone = false;
        this.scrapingOutput = this.getScrapingResultFromBackend()
      },
      getAnalysisResult() {
        this.analysisDone = false;
        console.log(this.input);
        this.analysisOutput = this.getAnalysisResultFromBackend()
      },
      getAnalysisResultFromBackend() {
        const path = 'http://localhost:5000/api/analyze'
        axios.get(path, {
          params: {
            input: this.input
          }
        })
          .then(response => {
            this.analysisOutput = response.data.result;
            console.log(this.analysisOutput);
            this.analysisDone = true
          })
          .catch(error => {
            console.log(error);
            this.analysisDone = true
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
            this.scrapingDone = true
          })
      }
    },
    created() {
      // this.getRandom();
      this.getAnalysisResult();
      this.scrape()
    }
  }
</script>
