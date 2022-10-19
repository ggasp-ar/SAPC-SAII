(() => {
  document.forms.mainform.reset()
  const dateDesde = document.querySelector('input[id="dateDesde"]')
  const dateHasta = document.querySelector('input[id="dateHasta"]')
  const tabla = document.querySelector('table[id="tabla-asientos"]')
  const btnRealizarBusqueda = document.querySelector('button[id="realizarbusqueda"]')
  const csrfToken = document.querySelector("[name='csrf_token']").value
  const cuentaSelect = $('#cuenta')[0]
  const vacioText = document.querySelector('#vacioText')

  function cargarSeleccion (cuentas = []) {
    cuentaSelect.innerHTML = ''
    for (const elem of cuentas) {
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
  btnRealizarBusqueda.addEventListener('click', function () {
    if (dateDesde.value === '' | dateHasta.value === '') {
      Swal.fire('Por favor seleccione el rango de fechas')
      return
    }

    const selection = cuentaSelect.options[cuentaSelect.selectedIndex]
    const id = parseInt(selection.getAttribute('cid'))
    realizarBusqueda(id, dateDesde.value, dateHasta.value)
  })

  dateDesde.addEventListener('change', () => {
    dateHasta.setAttribute('min', dateDesde.value)
  })

  dateHasta.addEventListener('change', () => {
    dateDesde.setAttribute('max', dateHasta.value)
  })

  function realizarBusqueda (id, desde, hasta) {
    fetch(`${window.origin}/libromayor`, {
      method: 'POST',
      mode: 'same-origin',
      Credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        fechaDesde: desde,
        fechaHasta: hasta,
        cuenta: id
      })
    }).then(response => {
      if (!response.ok) {
        notificacionSwal('Error al intentar cargar los asientos', response.statusText, 'error', 'Cerrar')
      }
      return response.json()
    }).then(respData => {
      if (JSON.stringify(respData) === JSON.stringify({})) {
        tabla.style.display = 'None'
        vacioText.style.display = 'block'
      } else {
        cargarTransacciones(respData)
        tabla.style.display = ''
        vacioText.style.display = 'None'
      }
      return respData
    }).catch(error => {
      notificacionSwal('¡Error!', error, 'error', 'Cerrar')
    })
  }

  function cargarTransacciones (data) {
    const table = $('#main-table')[0]
    $('#main-table tr').remove()
    let row = null
    const len = Object.keys(data).length
    let i = 1
    for (const [key, value] of Object.entries(data)) {
      row = table.insertRow(-1)
      generarRow(row, key, value.Desc, value.Valor, value.Haber, value.SaldoParcial, value.Asiento, true)
      if (i === len) {
        row = table.insertRow(-1)
        row.className = 'remarcado'
        generarRow(row, key, 'Saldo a la fecha', '-', false, value.SaldoParcial, '-')
      }
      i++
    }
  }

  function generarRow (row, fecha, desc, valor, haber, saldo, aid, btn = false) {
    // Cell 1
    row.insertCell(0).innerHTML = fecha
    // Cell 2
    const cell2 = row.insertCell(1)
    cell2.style.textAlign = 'left'
    cell2.innerHTML = desc
    if (haber) {
      cell2.style.paddingLeft = '3em'
    }
    if (valor === '-') {
      row.insertCell(2).innerHTML = valor
      row.insertCell(3).innerHTML = valor
    } else {
      // Cell 3
      row.insertCell(2).innerHTML = ((haber) ? '-' : '$ ' + valor)
      // Cell 4
      row.insertCell(3).innerHTML = ((haber) ? '$ ' + valor : '-')
    }

    // Cell 5
    row.insertCell(4).innerHTML = saldo
    // Cell 6
    if (btn) {
      const delBtn = document.createElement('button')
      delBtn.onclick = () => { window.open('/verasiento?asiento_id=' + String(aid), '_blank') }
      delBtn.innerHTML = 'Ver'
      delBtn.className = 'btn btn-block btn-dark st-btn'
      row.insertCell(5).appendChild(delBtn)
    } else {
      row.insertCell(5)
    }
  }
  recargarCuentas()
})()
