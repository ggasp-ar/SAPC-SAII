(() => {
  document.querySelector('button[id="addAsiento"]').addEventListener('click', function () {
    alert('Todavia no implementado')
  })

  $('#descripcion').keydown(function (e) {
    // Enter was pressed without shift key
    if (e.keyCode === 13 && !e.shiftKey) {
      // prevent default behavior
      e.preventDefault()
    }
  })

  let today = new Date()
  let dd = today.getDate()
  let mm = today.getMonth() + 1 // January is 0 so need to add 1 to make it 1!
  const dp = document.getElementById('datePicker')
  const yyyy = today.getFullYear()
  if (dd < 10) {
    dd = '0' + dd
  }
  if (mm < 10) {
    mm = '0' + mm
  }
  today = yyyy + '-' + mm + '-' + dd

  // tomorrow = yyyy+'-'+mm+'-'+(dd+1);
  dp.value = today

  const csrfToken = document.querySelector("[name='csrf_token']").value

  function getTablaInfo () {
    const mitabla = []
    $('#main-table tr').each(function (i, row) {
      const $row = $(row)
      const nroLista = $row.find('td:nth-child(1)').text()
      const cuentaId = $row.find('td:nth-child(1)').attr('cuenta-id')
      const cuenta = $row.find('td:nth-child(2)').text()
      let tipo = 0
      const debe = $row.find('td:nth-child(3)').text()
      const haber = $row.find('td:nth-child(4)').text()
      let valor = debe
      if (debe.includes('-')) {
        tipo = 1
        valor = haber
      }

      mitabla.push([nroLista, cuentaId, cuenta, valor, tipo])
    })
    return mitabla
  }

  const btnFinalizarAsiento = document.querySelector('button[id="finalizar"]')
  btnFinalizarAsiento.innerHTML = 'Finalizar Asiento'
  btnFinalizarAsiento.addEventListener('click', function () {
    confirmarAsiento()
  })
  btnFinalizarAsiento.style.display = 'block'

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
      preConfirm: () => {
        return fetch(`${window.origin}/cargarasiento`, {
          method: 'POST',
          mode: 'same-origin',
          Credentials: 'same-origin',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({
            asientos: getTablaInfo()
          })
        }).then(response => {
          if (!response.ok) {
            notificacionSwal('Error', response.statusText, 'error', 'Cerrar')
          }
          return response.json()
        }).then(data => {
          if (data.exito) {
            notificacionSwal('¡Éxito!', 'success', 'Ok!')
          } else {
            notificacionSwal('Ocurrio un error..', data.mensaje, 'warning', 'Ok')
          }
        }).catch(error => {
          notificacionSwal('¡Error!', error, 'error', 'Cerrar')
        })
      },
      allowOutsideClick: () => false,
      allowEscapeKey: () => false
    })
  }
})()
