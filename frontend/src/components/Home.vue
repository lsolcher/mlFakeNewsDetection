<template>
  <div>
    <p>Home page</p>

    <!-- DNN ANALYSIS -->
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


    <!-- CREATE BOW MODEL -->
    <template v-if="!bowModelDone">
      <p>Analysiere Link...</p>
      <p>{{bowProgress}}</p>
      <v-progress-circular
        indeterminate
        color="primary"
      ></v-progress-circular>
    </template>
    <template v-else>
      <v-btn
        @click="createBowModel()"
      >BOW-Modell aktualisieren</v-btn>
      <p>{{bowModelOutput}}</p>
    </template>

    <!-- GET BOW ANALYSIS -->
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
      >Link auf Wortähnlichkeit untersuchen</v-btn>
      <p>{{bowAnalysisOutput}}</p>
    </template>


    <!-- SCRAPING -->
    <template v-if="!scrapingDone">
      <p>Aktualisiere Datenbank...</p>
      <p>{{scrapeProgress}}</p>
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
        bowModelOutput: '',
        bowAnalysisOutput: '',
        scrapingOutput: '',
        dnnAnalysisDone: true,
        bowModelDone: true,
        bowAnalysisDone: true,
        scrapingDone: true,
        scrapeProgress: '',
        bowProgress: '',
        scrapeProgressId: 0,
        bowProgressId: 0
      }
    },
    methods: {
      // ---- SCRAPING ---- //
      scrape() {
        this.scrapingDone = false;
        this.updateScrapeProgress();
        this.scrapingOutput = this.getScrapingResultFromBackend()
      },
      getScrapingResultFromBackend() {
        const path = 'http://localhost:5000/api/scrape';
        axios.get(path)
          .then(response => {
            this.scrapingOutput = response.data.result;
            console.log(this.scrapingOutput);
            this.scrapingDone = true;
            clearInterval(this.scrapeProgressId)
          })
          .catch(error => {
            console.log(error);
            this.scrapingOutput = "Ein unerwarteter Fehler ist aufgetreten";
            this.scrapingDone = true
          })
      },

      //TODO:
      updateScrapeProgress() {
        this.scrapeProgressId = setInterval(function () {
          this.readScrapeProgress();
        }.bind(this), 3000);
      },
      readScrapeProgress() {
        const path = 'http://localhost:5000/api/scrape_progress';
        axios.get(path)
          .then(response => {
            this.scrapeProgress = response.data;
            console.log(this.scrapeProgress)
          })
          .catch(error => {
            console.log(error);
          })
      },

      // ---- DNN ---- //
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

      // ---- CREATE BOW MODEL ---- //
      getBOWAnalysisResult() {
        this.bowModelDone = false;
        console.log(this.input);
        this.bowAnalysisOutput = this.getBOWAnalysisResultFromBackend()
      },
      getBOWAnalysisResultFromBackend() {
        const path = 'http://localhost:5000/api/getBOW';
        axios.get(path)
          .then(response => {
            this.bowAnalysisOutput = response.data.result;
            console.log(this.bowAnalysisOutput);
            this.bowAnalysisDone = true;
          })
          .catch(error => {
            console.log(error);
            this.bowAnalysisDone = true
          })
      },

      // ---- GET BOW ---- //
      createBowModel() {
        this.bowModelDone = false;
        console.log(this.input);
        this.updateBowProgress();
        this.bowModelOutput = this.getBOWModelResultFromBackend()
      },
      getBOWModelResultFromBackend() {
        const path = 'http://localhost:5000/api/createBOW';
        axios.get(path, {
          params: {
            input: this.input
          }
        })
          .then(response => {
            this.bowModelOutput = response.data.result;
            console.log(this.bowModelOutput);
            this.bowModelDone = true;
            clearInterval(this.bowProgressId)
          })
          .catch(error => {
            console.log(error);
            this.bowModelDone = true
          })
      },

      updateBowProgress() {
        this.bowProgressId = setInterval(function () {
          this.readBowProgress();
        }.bind(this), 3000);
      },
      readBowProgress() {
        const path = 'http://localhost:5000/api/bow_progress';
        axios.get(path)
          .then(response => {
            this.bowProgress = response.data;
            console.log(this.bowProgress)
          })
          .catch(error => {
            console.log(error);
          })
      },



      killThreads() {
        let id = window.setTimeout(function() {}, 0);
        console.log(id)
        while (id--) {
          clearInterval(id);
        }

      }


    },
    created() {
      this.killThreads()
      // this.getRandom();
      //this.getDNNAnalysisResult();
      //this.scrape()
    }
  }
</script>
