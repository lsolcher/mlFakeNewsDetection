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
        <ul v-for="msg in scrapeProgress">
          <p>
            {{ msg }}
          </p>
        </ul>
      </template>

    </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'scrape',
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
        }.bind(this), 1000);
      },
      readScrapeProgress() {
        const path = 'http://localhost:5000/api/scrape_progress';
        axios.get(path)
          .then(response => {
            this.scrapeProgress = Array.from(response.data);
            console.log(typeof this.scrapeProgress)
            console.log(Array.isArray(this.scrapeProgress))
            console.log(this.scrapeProgress)
          })
          .catch(error => {
            console.log(error);
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
    }
  }
</script>

<style scoped>

</style>
