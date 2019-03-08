<template>

  <div>
    <div class="col 4">
      <h5>
        Mummy Money
      </h5>
      <a>{{this.dashboard.mummyMoney}}</a>
      <h5>
        AVG Money
      </h5>
      <a>{{this.dashboard.avgMoney.money__avg}}</a>
      <h5>
        Total Population
      </h5>
      <a>{{this.dashboard.totalPopulation}}</a>
      <h5>
        Total Members
      </h5>
      <a>{{this.dashboard.totalMembers}}</a>
    </div>
    <div class="col 8">
      <div class="row">
        <ul class="col s8 offset-s2 card-panel grey lighten-5">
          <h3>
            Mummy Money
          </h3>

          <Table
            :investors="investors"
          >
          </Table>

          <h4>
            Candidates
          </h4>
          <Table
            :investors="candidates"
          >
          </Table>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import Table from './Table'

  export default {
    name: 'Dashboard',
    data() {
      return {
        dashboard: [],
        investors: [],
        candidates: [],
      }
    },
    components: {Table},
    methods: {
      getDashboard: function () {
        axios.get('http://localhost:8000/investors/')
          .then(response => {
            this.dashboard = response.data
            this.investors = response.data.investors
            this.candidates = response.data.candidates
          })
          .catch(e => {
            this.errors.push(e)
          })
      }
    },
    created() {
      this.getDashboard()
    }
  }
</script>

<style scoped>
  li {
    list-style: none;
    padding-left: 10px;
  }
</style>
