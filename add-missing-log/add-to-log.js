var fs = require('fs');

if (process.argv.length < 5) {
  console.log("Add json formatted log content to existing logfile");
  console.log("  node add-to-log.js <new.json> <existing.log> <merged.log>");
  process.exit(0)
}

var contentToAddFile = process.argv[2];
var existingLogFile = process.argv[3];
var mergedLogFile = process.argv[4];

function compareByTime(a,b) {
  if (a.time < b.time)
    return -1;
  if (a.time > b.time)
    return 1;
  return 0;
}

function loadJSON(file) {
  return JSON.parse(fs.readFileSync(file))
}

var contentToAdd = loadJSON(contentToAddFile);
var existingLog = loadJSON(existingLogFile);
var mergedLog = existingLog.concat(contentToAdd);
mergedLog.sort(compareByTime);

console.log("Existing logfile: " + existingLog.length + " entries.");
console.log("     New logdata: " + contentToAdd.length + " entries.");
console.log("  Merged logfile: " + mergedLog.length + " entries.");

fs.writeFile(mergedLogFile, JSON.stringify(mergedLog), function(e) {
  console.log("Wrote merged logdata to " + mergedLogFile);
});
