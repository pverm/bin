var fs         = require('fs');
var path       = require('path');
var models     = require('./models'); 
var dateFormat = require('dateformat');

const CHANNEL_ID = 2;

/*
    getChannel(channelName, serverName).then(function(channel) {
      models.Message.create({
        prefix: message.prefix,
        nick: message.nick,
        host: message.host,
        command: command,
        postedAt: now,
        postedAtDate: dateFormat('yyyy-mm-dd'),
        text: text,
        channel_id: channel.id
      });
    }).catch(function(err) {
      console.error(err);
    });
*/

function enter(filepath) {
  var basename = path.basename(filepath);
  var data = fs.readFileSync(filepath, encoding='utf-8');
  var logdata = JSON.parse(data);
  var records = []
  
  console.log(logdata);
  
  for (var i=0; i<logdata.length; i++) {
  
    var obj = {
      nick: logdata[i].nick,
      postedAt: new Date(basename.slice(9,-4) + ' ' + logdata[i].time),
      postedAtDate: basename.slice(9,-4),
      channel_id: CHANNEL_ID
    }
    
    // var text = (command === 'KICK') ? message.args[1] + '(' + message.args[2] + ')' : message.args[1];
    
    if (logdata[i].msg) {
      obj.command = 'PRIVMSG';
      obj.text = logdata[i].msg
    } else if (logdata[i].action.startsWith('changed topic')) {
      obj.command = 'TOPIC';
      obj.text = logdata[i].action.slice(18,-2)
    } else if (logdata[i].action.startsWith('joined')) {
      obj.command = 'JOIN';
    } else if (logdata[i].action.startsWith('kicked')) {
      obj.command = 'KICK';
      obj.text = logdata[i].action.slice(7)
    } else if (logdata[i].action.startsWith('left')) {
      obj.command = 'PART';
    } else {
      obj.command = 'EMOTE';
      obj.text = logdata[i].action
    }
    
    records.push(obj);
  }
  
  models.Message.bulkCreate(records).then(function(instances) {
    console.log(instances);
  });
  
  
}

module.exports = {
  test: "test",
  enter: enter
}