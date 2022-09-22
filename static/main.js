const months = [
  'January', 
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
];

var inputTime, convertedTime;

window.onload = function init() {
  swapText('report_time_source', 'report_time')
  swapText('data_time_source', 'data_time')
}

function swapText(source, target) {
  inputTime = document.getElementById(source).textContent;
  convertedTime = convert_time(inputTime);
  document.getElementById(target).textContent += convertedTime
}

function convert_time(milliseconds) {
  let date = new Date(parseFloat(milliseconds));
  let month = date.getMonth();
  let day = date.getDate();
  month = months[month];
  
  let output = month + ' ' + day;

  let hour = date.getHours();
  morn = hour > 11 ? " PM" : " AM"
  hour = hour > 12 ? hour - 12 : hour;
  hour = hour == 0 ? 12 : hour;
  var minute = date.getMinutes();
  minute = minute < 10 ? '0' + minute : minute
  output += ' at ' + hour + ':' + minute + morn

  return output
}
