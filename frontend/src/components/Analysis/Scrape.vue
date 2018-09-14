<template>
    <div>
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
        scrapingOutput: '',
        scrapingDone: true,
        scrapeProgress: ''
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
      }
    }
  }
</script>

<style scoped>

</style>
