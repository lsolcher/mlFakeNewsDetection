<template>
  <div>
    <!-- CREATE BOW MODEL -->
    <template v-if="!createBowDone">
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
      <p>{{createBowOutput}}</p>
    </template>
  </div>
</template>

<script>
  import axios from 'axios'


  export default {
    name: 'create_bow',
    data() {
      return {
        input: '',
        createBowOutput: '',
        createBowDone: true,
        bowProgress: '',
        bowProgressId: 0
      }
    },
    methods: {
      // ---- CREATE BOW MODEL ---- //
      createBowModel() {
        this.createBowDone = false;
        console.log(this.input);
        this.updateCreateBowProgress();
        this.createBowOutput = this.createBowBackend()
      },
      createBowBackend() {
        const path = 'http://localhost:5000/api/createBOW';
        axios.get(path)
          .then(response => {
            this.createBowOutput = response.data.result;
            console.log(this.createBowOutput);
            this.createBowDone = true;
            clearInterval(this.bowProgressId)
          })
          .catch(error => {
            console.log(error);
            this.createBowDone = true
          })
      },

      updateCreateBowProgress() {
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
      }
    }
  }
</script>
