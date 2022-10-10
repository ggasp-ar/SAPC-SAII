(() => {
  const tabla = {}
  const data = JSON.parse($('#data')[0].innerHTML)
  const csrfToken = document.querySelector("[name='csrf_token']").value
  const cuentasUsadas = []
  let cuentasSaldo = []

  $('#descripcion').keydown(function (e) {
    // Enter was pressed without shift key
    if (e.keyCode === 13 && !e.shiftKey) {
      // prevent default behavior
      e.preventDefault()
    }
  })

  window.onbeforeunload = function () {
    return 'Si recarga se perdera la informacion del asiento'
  }

  const dp = document.getElementById('datePicker')
  const today = new Date()
  /*
    let dd = today.getDate()
    let mm = today.getMonth() + 1 // January is 0 so need to add 1 to make it 1!
    const yyyy = today.getFullYear()
    if (dd < 10) {
      dd = '0' + dd
    }
    if (mm < 10) {
      mm = '0' + mm
    }
    today = yyyy + '-' + mm + '-' + dd
    console.log(today)
    // tomorrow = yyyy+'-'+mm+'-'+(dd+1);
    // dp.value = today
  */
  dp.value = today.toISOString().slice(0, 16)

  /*
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
  } */

  const btnFinalizarAsiento = document.querySelector('button[id="finalizar"]')
  btnFinalizarAsiento.innerHTML = 'Finalizar Asiento'
  btnFinalizarAsiento.addEventListener('click', function () {
    if ((debe - haber) !== 0) {
      Swal.fire('El asiento no esta balanceado')
      return
    }
    if (Object.keys(tabla).length <= 0) {
      Swal.fire('El asiento esta vacio')
      return
    }
    const descripcion = $('#descripcion')[0].value
    if (descripcion === '') {
      Swal.fire('La descripcion esta vacia.')
      return
    }
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
        return fetch(`${window.origin}/registrarasiento`, {
          method: 'POST',
          mode: 'same-origin',
          Credentials: 'same-origin',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({
            id: data.id,
            responsableid: data.responsableid,
            responsable: data.responsable,
            descripcion: $('#descripcion')[0].value,
            fecha: $('#datePicker')[0].value,
            asientos: tabla
          })
        }).then(response => {
          if (!response.ok) {
            notificacionSwal('Error', response.statusText, 'error', 'Cerrar')
          }
          return response.json()
        }).then(respData => {
          if (respData.exito) {
            notifSwalReset('¡Éxito!', respData.mensaje, 'success', 'Ok')
          } else {
            notificacionSwal('Ocurrio un error..', respData.mensaje, 'warning', 'Ok')
          }
        }).catch(error => {
          notificacionSwal('¡Error!', error, 'error', 'Cerrar')
        })
      },
      allowOutsideClick: () => false,
      allowEscapeKey: () => false
    })
  }

  function cargarSeleccion (cuentas = []) {
    const cuentaSelect = $('#cuenta')[0]
    cuentaSelect.innerHTML = ''
    if (cuentas.length === 0) {
      cuentas = cuentasSaldo
    } else {
      cuentasSaldo = cuentas
    }

    for (const elem of cuentas) {
      if (cuentasUsadas.includes(elem.cid)) {
        continue
      }
      const option = document.createElement('option')
      option.text = elem.text
      option.setAttribute('cid', elem.cid)
      cuentaSelect.add(option)
    }
  }

  function recargarCuentas () {
    fetch(`${window.origin}/cuentas`, {
      method: 'POST',
      mode: 'same-origin',
      Credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      }
    }).then(response => {
      if (!response.ok) {
        notificacionSwal('Error al intentar cargar las cuentas', response.statusText, 'error', 'Cerrar')
      }
      return response.json()
    }).then(respData => {
      cargarSeleccion(respData)
      return respData
    }).catch(error => {
      notificacionSwal('¡Error!', error, 'error', 'Cerrar')
    })
  }

  let asientoActual = 0
  let debe = 0
  let haber = 0

  recargarCuentas()
  /* Funcion utilizada para eliminar filas */

  function eliminarAsiento (btn, rowid) {
    const asiento = tabla[rowid]
    tabla[rowid] = null
    cuentasUsadas.splice(cuentasUsadas.indexOf(asiento.cuenta_id), 1)
    cargarSeleccion()

    const td = btn.parentNode
    const tr = td.parentNode
    tr.parentNode.removeChild(tr)

    if (asiento.haber) {
      haber -= asiento.monto
      $('#totalHaber')[0].innerHTML = '$ ' + haber
    } else {
      debe -= asiento.monto
      $('#totalDebe')[0].innerHTML = '$ ' + debe
    }
  }

  /* Funcion utilizada para generar cada fila de la tabla */
  function generarRow (row, id, nombreCuenta, valor, haber) {
    // Cell 1
    row.insertCell(0).innerHTML = id
    // Cell 2
    const cell2 = row.insertCell(1)
    cell2.style.textAlign = 'left'
    cell2.innerHTML = nombreCuenta
    if (haber) {
      cell2.style.paddingLeft = '3em'
    }
    // Cell 3
    row.insertCell(2).innerHTML = ((haber) ? '-' : '$ ' + valor)
    // Cell 4
    row.insertCell(3).innerHTML = ((haber) ? '$ ' + valor : '-')

    // Cell 5
    // row.insertCell(4).innerHTML = '<button id="editarAsiento" rowid=' + id + ' class="btn btn-block btn-dark btnEditarLibro st-btn">Editar</button>'
    row.insertCell(4).innerHTML = ''

    const delBtn = document.createElement('button')
    delBtn.onclick = () => { eliminarAsiento(delBtn, id) }
    delBtn.innerHTML = 'Eliminar'
    delBtn.className = 'btn btn-block btn-dark btnEliminarLibro st-btn'
    delBtn.setAttribute('rowid', id)
    row.insertCell(5).appendChild(delBtn)
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
      throw new Error('error al elegir debe/haber')
    }
  }

  /* CHEQUEO DE QUE HAYA INGRESADO UN MONTO */
  function getMonto () {
    const v = parseFloat($('#monto')[0].value)
    if (v > 0) {
      return v
    } else {
      Swal.fire('Monto invalido')
      throw new Error('Monto invalido')
    }
  }

  /* OBTENER CUENTA SELECCIONADA */

  function getCuenta () {
    const cuenta = $('#cuenta')[0]
    const selection = cuenta.options[cuenta.selectedIndex]
    return { nombre: selection.text, cuenta_id: parseInt(selection.getAttribute('cid')) }
  }

  /* AL APRETAR AGREGAR */
  document.querySelector('button[id="addAsiento"]').addEventListener('click', function () {
    const table = $('#main-table')[0]
    const cuenta = getCuenta()
    const row = table.insertRow(-1)
    generarRow(row, asientoActual, cuenta.nombre, getMonto(), getHaber())
    tabla[asientoActual] = { // Estructura que se envia al serivdor
      monto: getMonto(),
      haber: getHaber(),
      cuenta: cuenta.nombre,
      cuenta_id: cuenta.cuenta_id
    }

    cuentasUsadas.push(cuenta.cuenta_id)
    cargarSeleccion()

    if (getHaber()) {
      haber += getMonto()
      $('#totalHaber')[0].innerHTML = '$ ' + haber
    } else {
      debe += getMonto()
      $('#totalDebe')[0].innerHTML = '$ ' + debe
    }
    // $('#totalDiferencia')[0].innerHTML = Math.abs(debe - haber)
    // por ultimo
    asientoActual += 1
  })
})()
