

<template>
  <div>
    <p>Home page</p>

                    <div class="form-group">
                        <label for="userinput">Artikel-link, Tweet-link oder Tweet-id einfügen...</label>
                        <input
                                type="text"
                                id="userinput"
                                class="form-control"
                                v-model="input">
                    </div>
    <p>Ergebnis: {{output}}</p>

    <button @click="getResult()">Analysieren</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
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
    getResultFromBackend () {
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
  created () {
    // this.getRandom();
    this.getResult()
  }
}
</script>
