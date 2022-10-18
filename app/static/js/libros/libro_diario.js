(() => {
  document.forms.mainform.reset()
  const dateDesde = document.querySelector('input[id="dateDesde"]')
  const dateHasta = document.querySelector('input[id="dateHasta"]')
  const tabla = document.querySelector('table[id="tabla-asientos"]')
  const btnRealizarBusqueda = document.querySelector('button[id="realizarbusqueda"]')
  const csrfToken = document.querySelector("[name='csrf_token']").value
  const vacioText = document.querySelector('#vacioText')

  btnRealizarBusqueda.addEventListener('click', function () {
    if (dateDesde.value === '' | dateHasta.value === '') {
      Swal.fire('Por favor seleccione el rango de fechas')
      return
    }
    realizarBusqueda(dateDesde.value, dateHasta.value)
  })

  dateDesde.addEventListener('change', () => {
    dateHasta.setAttribute('min', dateDesde.value)
  })

  dateHasta.addEventListener('change', () => {
    dateDesde.setAttribute('max', dateHasta.value)
  })

  function realizarBusqueda (desde, hasta) {
    fetch(`${window.origin}/librodiario`, {
      method: 'POST',
      mode: 'same-origin',
      Credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        fechaDesde: desde,
        fechaHasta: hasta
      })
    }).then(response => {
      if (!response.ok) {
        notificacionSwal('Error al intentar cargar los asientos', response.statusText, 'error', 'Cerrar')
      }
      return response.json()
    }).then(respData => {
      console.log(respData)
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
    for (const [key, value] of Object.entries(data)) {
      let i = 0
      for (const elem in value) {
        const e = value[elem]
        if (i === 0) {
          row = table.insertRow(-1)
          generarRow(row, key, e.Cuenta, e.Valor, e.Haber, e.Asiento, true)
        } else {
          row = table.insertRow(-1)
          generarRow(row, '', e.Cuenta, e.Valor, e.Haber, e.Asiento)
        }
        i += 1
      }
    }
  }

  function generarRow (row, fecha, desc, valor, haber, aid, btn = false) {
    // Cell 1
    row.insertCell(0).innerHTML = fecha
    // Cell 2
    const cell2 = row.insertCell(1)
    cell2.style.textAlign = 'left'
    cell2.innerHTML = desc
    if (haber) {
      cell2.style.paddingLeft = '3em'
    }
    // Cell 3
    row.insertCell(2).innerHTML = ((haber) ? '-' : '$ ' + valor)
    // Cell 4
    row.insertCell(3).innerHTML = ((haber) ? '$ ' + valor : '-')
    // Cell 4
    if (btn) {
      const delBtn = document.createElement('button')
      delBtn.onclick = () => { window.open('/verasiento?asiento_id=' + String(aid), '_blank') }
      delBtn.innerHTML = 'Ver'
      delBtn.className = 'btn btn-block btn-dark st-btn'
      row.insertCell(4).appendChild(delBtn)
    } else {
      row.insertCell(4)
    }
  }
})()
