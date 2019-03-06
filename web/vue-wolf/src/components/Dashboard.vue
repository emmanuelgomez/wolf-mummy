<template>
  <div
  >
    <label>

      <span
        :class="classObject"
      >
       {{this.info.totalPopulation}}
      </span>

    </label>
  </div>
</template>

<script>
  export default {
    name: "Dashboard",
    data() {
      return {
        info: [],
        errors: [],
      }
    },
    methods: {
      getInfo: function () {
        axios.get('http://localhost:8000/dashboard/?format=json')
          .then(response => {
            this.info = response.data
          })
          .catch(e => {
            this.errors.push(e)
          })
      }
    },
    created() {
      this.getInfo()
    }
  }
</script>

<style scoped>

</style>
