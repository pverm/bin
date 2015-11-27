var fs = require('fs');
var Sequelize = require('sequelize');
var sequelize = new Sequelize('postgres://user:pw@localhost:5432/db');

var Uploadpic = sequelize.define("Uploadpic", {
  host: Sequelize.STRING,
  data: Sequelize.JSON,
  nick: Sequelize.STRING
});

Uploadpic.sync({force: true}).then(function() {
  var records = [];
  var obj = JSON.parse(fs.readFileSync('uploadpic.json'));
  for (var id in obj) {
    var host;
    if (Number(id)) {
      host = 'u';
    } else if (id.indexOf(".") > 0) {
      host = 'p';
    } else {
      host = 'i';
    }
    records.push({
      host: host,
      data: obj[id],
      nick: 'kb'
    });
  }
  return Uploadpic.bulkCreate(records);
}).then(function(instances) {
  console.log(instances);
});



