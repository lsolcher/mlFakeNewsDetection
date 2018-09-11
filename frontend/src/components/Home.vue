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
            @keyup.enter="getResult()"
            v-model="input"
          ></v-text-field>
        </v-flex>
        <br>
      </v-layout>
    </v-container>

    <v-btn @click="getResult()">Analysieren</v-btn>
    <p>Ergebnis: {{output}}</p>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    data() {
      return {
        randomNumber: 0,
        input: '',
        output: ''
      }
    },
    methods: {
      getResult() {
        console.log(this.input)
        this.output = this.getResultFromBackend()
      },
      getResultFromBackend() {
        const path = 'http://localhost:5000/api/analyze'
        axios.get(path, {
          params: {
            input: this.input
          }
        })
          .then(response => {
            this.output = response.data.result;
            console.log(this.output)
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    created() {
      // this.getRandom();
      this.getResult()
    }
  }
</script>
