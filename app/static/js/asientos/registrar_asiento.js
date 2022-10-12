(() => {
  const tabla = {}
  const data = JSON.parse($('#data')[0].innerHTML)
  const csrfToken = document.querySelector("[name='csrf_token']").value
  const cuentasUsadas = []

  const checkDebe = $('#checkDebe')
  const checkHaber = $('#checkHaber')

  let cuentasSaldo = []

  let asientoActual = 0
  let debe = 0
  let haber = 0

  const dp = document.getElementById('datePicker')
  const today = new Date()
  dp.value = today.toISOString().slice(0, 16)

  const btnFinalizarAsiento = document.querySelector('button[id="finalizar"]')

  const cuentaSelect = $('#cuenta')[0]
  const refreshBtn = $('#refresh')[0]
  const addCuentaBtn = $('#addAccBtn')[0]

  refreshBtn.addEventListener('click', () => {
    recargarCuentas()
  })
  addCuentaBtn.addEventListener('click', () => {
    window.open('/cuentas', '_blank')
  })

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
      option.setAttribute('tipo', elem.tipo.tipo)
      cuentaSelect.add(option)
    }
  }

  function bloquearDH () {
    checkDebe.prop('disabled', true)
    checkHaber.prop('disabled', true)
  }

  function desbloquearDH () {
    checkDebe.prop('disabled', false)
    checkHaber.prop('disabled', false)
  }

  cuentaSelect.addEventListener('change', () => {
    const cuenta = getCuenta()
    if (cuenta.cuenta_tipo === 'R-') {
      bloquearDH()
      setRadio(checkHaber, false)
      setRadio(checkDebe, true)
    } else if (cuenta.cuenta_tipo === 'R+') {
      bloquearDH()
      setRadio(checkHaber, true)
      setRadio(checkDebe, false)
    } else {
      desbloquearDH()
    }
  })

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
  function getRadio (radio) {
    return radio.prop('checked')
  }
  function setRadio (radio, bool) {
    return radio.prop('checked', bool)
  }

  function getHaber () {
    if (getRadio(checkDebe)) {
      return false
    } else if (getRadio(checkHaber)) {
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
    const selection = cuentaSelect.options[cuentaSelect.selectedIndex]
    return {
      nombre: selection.text,
      cuenta_id: parseInt(selection.getAttribute('cid')),
      cuenta_tipo: selection.getAttribute('tipo')
    }
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
