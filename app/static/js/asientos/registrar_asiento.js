(() => {
  function generarRow (row, id, codigoCuenta, nombreCuenta, valor, haber) {
    // Cell 1
    row.insertCell(0).innerHTML = id
    // Cell 2
    const cell2 = row.insertCell(1)
    cell2.style.textAlign = 'left'
    cell2.innerHTML = nombreCuenta
    cell2.className = `cuentaID = {$codigoCuenta}`
    if (haber) {
      cell2.style.paddingLeft = '3em'
    }
    // Cell 3
    row.insertCell(2).innerHTML = ((haber) ? '-' : '$ ' + valor)
    // Cell 4
    row.insertCell(3).innerHTML = ((haber) ? '$ ' + valor : '-')
    // Cell 5
    row.insertCell(4).innerHTML = `<button id="editarAsiento" rowid={$id} class="btn btn-block btn-dark btnEditarLibro st-btn">Editar</button>`
    row.insertCell(5).innerHTML = `<button id="eliminarAsiento" rowid={$id} class="btn btn-block btn-dark btnEliminarLibro st-btn">Eliminar</button>`
  }

  function getRow (id) {
    const table = $('#main-table')[0]
    $(table.rows[2]).find('td:nth-child(2)').text()
    return 0
  }

  /* CHEQUEO DE SI ES POR EL DEBE O POR EL HABER */
  function getRadio (id) {
    return $(id).prop('checked')
  }

  function getHaber () {
    if (getRadio('#checkDebe')) {
      return false
    } else if (getRadio('#checkHaber')) {
      return true
    } else {
      throw 'error al elegir debe/haber'
    }
  }

  /* CHEQUEO DE QUE HAYA INGRESADO UN MONTO */
  function getMonto () {
    const v = $('#monto')[0].value
    if (v > 0) {
      return v
    } else {
      throw 'Monto invalido'
    }
  }

  /* OBTENER CUENTA SELECCIONADA */

  function getCuenta () {
    const cuenta = $('#cuenta')[0]
    const selection = cuenta.options[cuenta.selectedIndex]
    return { id: selection.getAttribute('cid'), nombre: selection.getAttribute('value') }
  }

  /* AL APRETAR AGREGAR */
  document.querySelector('button[id="addAsiento"]').addEventListener('click', function () {
    const table = $('#main-table')[0]
    const row = table.insertRow(-1)
    const cuenta = getCuenta()
    generarRow(row, 1, cuenta.id, cuenta.nombre, getMonto(), getHaber())
  })

  $('#descripcion').keydown(function (e) {
    // Enter was pressed without shift key
    if (e.keyCode === 13 && !e.shiftKey) {
      // prevent default behavior
      e.preventDefault()
    }
  })

  $(window).bind('beforeunload', function () {
    return 'Seguro que desea salir? Se perdera todo el progreso en el asiento'
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
