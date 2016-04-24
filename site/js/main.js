"use strict";

$(function(){
  var sortDate = function(a, b) {
    return b.date - a.date;
  };


  _.template.formatdate = function (stamp) {
    var fragments = [
      stamp.getMonth() + 1,
      stamp.getDate(),
      stamp.getFullYear()
    ];
    return fragments.join('/');
  };

  _.template.formattime = function(stamp) {
    var hours = stamp.getHours(),
        minutes = stamp.getMinutes(),
        ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
  }
  
  var data;
  var readingTemp = _.template(
    $("#readingTemplate").html()
  );

  d3.csv('./data/readings.csv', function(rows){
    rows.forEach(function(d){
      d.date = new Date(d.date);
      d.temperature = Math.round( +d.temperature *  10 ) / 10;
      d.humidity = Math.round( +d.humidity * 10 ) / 10;
    });
    data = rows.sort(sortDate);
    var lastReading = readingTemp(data[0]);
    $("#reading").html(lastReading);
    console.log(typeof(data[0].date));
  });

  // d3.csv('./data/readings.csv', function(d){
  //   return {
  //     timestamp : new Date(d.date),
  //     temperature : +d.temperature,
  //     humidity : +d.humidity,
  //   };
  // }, function(error, rows){
  //   return rows;
  // });

console.log(data);
});
