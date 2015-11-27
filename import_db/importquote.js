var fs = require('fs');
var Sequelize = require('sequelize');
var sequelize = new Sequelize('postgres://user:pw@localhost:5432/db');

var Quote = sequelize.define("Quote", {
  nick: Sequelize.STRING,
  quote: Sequelize.TEXT,
  savedBy: Sequelize.STRING,
  lastPostedAt: Sequelize.DATE,
});

Quote.sync({force: true}).then(function() {

  var records = [];
  var obj = JSON.parse(fs.readFileSync('quote.json'));
  
  for (var nick in obj) {
    for (var i=0; i<obj[nick].length; i++) {
      records.push({
        nick: nick,
        quote: obj[nick][i],
        savedBy: 'kb',
        lastPostedAt: new Date()
      });
    }
  }
  
  return Quote.bulkCreate(records);

}).then(function(instances) {
  console.log(instances);
});



