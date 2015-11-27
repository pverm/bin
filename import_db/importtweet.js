var fs = require('fs');
var Sequelize = require('sequelize');
var sequelize = new Sequelize('postgres://user:pw@localhost:5432/db');

var Tweet = sequelize.define("Tweet", {
  data: Sequelize.JSON,
  nick: Sequelize.STRING
});

Tweet.sync({force: true}).then(function() {
  var records = [];
  var obj = JSON.parse(fs.readFileSync('tweet.json'));
  for (var tid in obj) {
    records.push({
      data: obj[tid],
      nick: 'kb'
    });
  }
  return Tweet.bulkCreate(records);
}).then(function(instances) {
  console.log(instances);
});
