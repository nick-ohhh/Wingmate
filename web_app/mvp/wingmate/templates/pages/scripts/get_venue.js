$(document).ready(function(){
  const locate = {};
  $("button").click(function(){
    date_location = $("input:text").val();
    $("#me").text(date_location);
  });
});
