var fs = require('fs');
var Sequelize = require('sequelize');
var sequelize = new Sequelize('postgres://user:pw@localhost:5432/db');

var Memo = sequelize.define("Memo", {
  nick: Sequelize.STRING,
  text: Sequelize.TEXT,
  cleared: {
    type: Sequelize.BOOLEAN,
    allowNull: false,
    defaultValue: false
  }
});

Memo.sync({force: false}).then(function() {

  var records = [];
  var obj = JSON.parse(fs.readFileSync('memo.json'));
  
  for (var nick in obj) {
    
    for (var memo in obj[nick].memos) {
      records.push({
        nick: nick,
        text: obj[nick].memos[memo].memo,
        cleared: false,
        createdAt: new Date(obj[nick].memos[memo].created)
      });
    }
  
    for (var memo in obj[nick].history) {
      records.push({
        nick: nick,
        text: obj[nick].history[memo].memo,
        cleared: true,
        createdAt: new Date(obj[nick].history[memo].created)
      });
    }
    
  }
  
  Memo.bulkCreate(records).then(function(instances) {
    console.log(instances);
  });

});



