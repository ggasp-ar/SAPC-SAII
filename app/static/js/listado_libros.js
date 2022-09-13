(function() {
    const btnsComprarLibro = document.querySelectorAll('.btnComprarLibro');
    let isbnLibroSeleccionado = null;
    const csrf_token=document.querySelector("[name='csrf_token']").value;

    btnsComprarLibro.forEach((btn) => {
        btn.addEventListener('click',function(){
            isbnLibroSeleccionado = this.id;
            confirmarComprar();
        })
    });

    const confirmarComprar = () => {
        Swal.fire({
            title: '¿Está seguro de que desea comprar este libro?',
            inputAttributes: {
                autocapitalize: 'off'
            },
            showCancelButton: true,
            cancelButtonColor: '#d33',
            cancelButtonText: 'No, Gracias',
            confirmButtonText: 'Si, ¡comprarlo!',
            confirmButtonColor: '#2b3436',
            backdrop: 'rgba(0,0,0,0.8)',
            showLoaderOnConfirm: true,
                preConfirm: async () => {
                    return await fetch(`${window.origin}/comprarLibro`, {
                        method:'POST',
                        mode:'same-origin',
                        Credentials: 'same-origin',
                        headers:{
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrf_token
                        },
                        body:JSON.stringify({
                            'isbn':isbnLibroSeleccionado
                        })
                    }).then(response => {
                        if(!response.ok){
                            notificacionSwal('Error',response.statusText,'error','Cerrar');
                        }
                        return response.json();
                    }).then(data=>{
                        if(data.exito){
                            notificacionSwal('¡Éxito!', '¡Gracias por su Compra!','success','Ok!');
                        }else{
                            notificacionSwal('¡Alerta!', data.mensaje,'warning','Ok');
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