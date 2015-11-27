var fs       = require('fs');
var path     = require('path');
var logtodb  = require('./logtodb.js');
//logtodb.enter('./logs/#grpchat-2015-07-03.log');

fs
  .readdirSync('./logs')
  .filter(function(file) {
    return (file.indexOf('.') !== 0);
  })
  .forEach(function(file) {
    if (file.slice(-4) !== '.log') return;
    logtodb.enter('./logs/' + file);
  });