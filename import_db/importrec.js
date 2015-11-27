var fs        = require('fs');
var Sequelize = require('sequelize');
var sequelize = new Sequelize('postgres://user:pw@localhost:5432/db');

var Rec = sequelize.define("Rec", {
  title: Sequelize.STRING,
  done: Sequelize.BOOLEAN,
  genre: Sequelize.ARRAY(Sequelize.STRING),
  description: Sequelize.TEXT
});

Rec.sync({force: false}).then(function() {

  var records = [];
  var obj = JSON.parse(fs.readFileSync('data.json'));
  
  for (var category in obj.recs) {
  
    var genre;
    var old;
  
    switch (category) {
      case 'n': 
      case 'a':
        genre = ['n'];
        old = false;
        break;
      case 'm':
        genre = ['m'];
        old = false;
        break;
      case 'o':
        genre = ['n'];
        old = true;
        break;
    }
    
    obj.recs[category].forEach(function(rec) {
      records.push({
        title: rec.title,
        description: rec.description,
        old: old,
        genre: genre
      });
    });
  
  }


  return Rec.bulkCreate(records);

}).then(function(instances) {
  console.log(instances);
});
