<template>
  <table id="firstTable">
    <thead>
    <tr>
      <th>ID</th>
      <th>innocence</th>
      <th>experience</th>
      <th>charisma</th>
      <th>money</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="investor in investors">
      <td>{{investor.id}}</td>
      <td>{{investor.innocence}}</td>
      <td>{{investor.experience}}</td>
      <td>{{investor.charisma}}</td>
      <td>{{investor.money}}</td>
    </tr>
    </tbody>
  </table>
</template>

<script>
  export default {
    name: "Table",
    props: {
      investors: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        investors: this.investors
      }
    }
  }
</script>

<style scoped>
  table {
    font-family: 'Open Sans', sans-serif;
    width: 750px;
    border-collapse: collapse;
    border: 3px solid #44475C;
    margin: 10px 10px 0 10px;
  }

  table th {
    text-transform: uppercase;
    text-align: left;
    background: #44475C;
    color: #FFF;
    padding: 8px;
    min-width: 30px;
  }

  table td {
    text-align: left;
    padding: 8px;
    border-right: 2px solid #7D82A8;
  }

  table td:last-child {
    border-right: none;
  }

  table tbody tr:nth-child(2n) td {
    background: #D4D8F9;
  }

</style>
