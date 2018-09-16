<template>
    <div>
      <v-app>
        <!-- SCRAPING -->

        <!-- currently scraping -->
        <template v-if="!scrapingDone">
          <p>Aktualisiere Datenbank...</p>
          <v-progress-circular
            indeterminate
            color="btnColor"
          ></v-progress-circular>
          <ul v-for="msg in scrapeProgress">
            <p>
              {{ msg }}
            </p>
          </ul>
        </template>



        <template v-else>
          <v-btn
            :disabled="!btnEnabled"
            @click="scrape()"
          >{{ btnText }}</v-btn>
        </template>
      </v-app>
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
        scrapeProgress: '',
        btnText: 'Artikeldatenbank aktualisieren',
        btnEnabled: true,
        btnColor:'info'
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
            this.btnText = 'Datenbank erfolgreich aktualisiert!';
            this.btnEnabled = false;
            this.btnColor = 'success'
            clearInterval(this.scrapeProgressId)
          })
          .catch(error => {
            console.log(error);
            this.scrapingOutput = "Ein unerwarteter Fehler ist aufgetreten";
            this.scrapingDone = true
          });
        this.scrapingOutput = ''
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
