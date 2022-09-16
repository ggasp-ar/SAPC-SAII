document.querySelector('button[id="addAsiento"]').addEventListener('click',function(){
    alert("Todavia no implementado");
})

$("#descripcion").keydown(function(e){
  // Enter was pressed without shift key
  if (e.keyCode == 13 && !e.shiftKey)
  {
      // prevent default behavior
      e.preventDefault();
  }
  });
var dp = document.getElementById("datePicker");
var today = new Date();
var dd = today.getDate();
var mm = today.getMonth()+1; //January is 0 so need to add 1 to make it 1!
var yyyy = today.getFullYear();
if(dd<10){
  dd='0'+dd
} 
if(mm<10){
  mm='0'+mm
} 
today = yyyy+'-'+mm+'-'+dd;

//tomorrow = yyyy+'-'+mm+'-'+(dd+1);
dp.value=today;
