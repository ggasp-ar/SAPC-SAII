(function() {
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

const btnFinalizarAsiento = document.querySelector('button[id="finalizarAsiento"]');

const csrf_token=document.querySelector("[name='csrf_token']").value;


function getTablaInfo(){
    let mitabla = [];
    $("#main-table tr").each(function (i, row) {
        let $row = $(row);
        let nro_lista = $row.find("td:nth-child(1)").text();
        let cuenta_id = $row.find("td:nth-child(1)").attr("cuenta-id");
        let cuenta = $row.find("td:nth-child(2)").text();
        let tipo = 0;
        let debe = $row.find("td:nth-child(3)").text();
        let haber = $row.find("td:nth-child(4)").text();
        let valor = debe;
        if (debe.includes("-")){
          tipo=1;
          valor = haber;
        }

        mitabla.push([nro_lista,cuenta_id,cuenta,valor,tipo])
        
    })
    return mitabla;
}

btnFinalizarAsiento.addEventListener('click',function(){
  tabla = document.querySelectorAll('table[id="tabla-asientos"]');
  confirmarAsiento();
})

const confirmarAsiento = () => {
    Swal.fire({
        title: '¿Está seguro?',
        inputAttributes: {
            autocapitalize: 'off'
        },
        showCancelButton: true,
        cancelButtonColor: '#d33',
        cancelButtonText: 'Cancelar carga',
        confirmButtonText: 'Cargar',
        confirmButtonColor: '#2b3436',
        backdrop: 'rgba(0,0,0,0.8)',
        showLoaderOnConfirm: true,
            preConfirm: async () => {
                return await fetch(`${window.origin}/cargarAsiento`, {
                    method:'POST',
                    mode:'same-origin',
                    Credentials: 'same-origin',
                    headers:{
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf_token
                    },
                    body:JSON.stringify({
                        'asientos':getTablaInfo()
                    })
                }).then(response => {
                    if(!response.ok){
                        notificacionSwal('Error',response.statusText,'error','Cerrar');
                    }
                    return response.json();
                }).then(data=>{
                    if(data.exito){
                        notificacionSwal('¡Éxito!','success','Ok!');
                    }else{
                        notificacionSwal('Ocurrio un error..', data.mensaje,'warning','Ok');
                    }
                }).catch(error=>{
                    notificacionSwal('¡Error!',error,'error','Cerrar');
                });
        },
        allowOutsideClick: () => false,
        allowEscapeKey: () => false,
    });
};
})();