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
    fetch(`${window.origin}/verasientos`, {
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
      if (JSON.stringify(respData) === JSON.stringify([])) {
        tabla.style.display = 'None'
        vacioText.style.display = 'block'
      } else {
        cargarAsientos(respData)
        tabla.style.display = ''
        vacioText.style.display = 'None'
      }
      return respData
    }).catch(error => {
      notificacionSwal('¡Error!', error, 'error', 'Cerrar')
    })
  }

  function cargarAsientos (data) {
    const table = $('#main-table')[0]
    $('#main-table tr').remove()
    let row = null
    for (const elem of data) {
      row = table.insertRow(-1)
      generarRow(row, elem.id, elem.descripcion, elem.fecha)
    }
  }

  function generarRow (row, id, desc, fecha) {
    // Cell 1
    row.insertCell(0).innerHTML = id
    // Cell 2
    row.insertCell(1).innerHTML = desc
    // Cell 3
    row.insertCell(2).innerHTML = fecha
    // Cell 4
    const delBtn = document.createElement('button')
    delBtn.onclick = () => { window.open('/verasiento?asiento_id=' + String(id), '_blank') }
    delBtn.innerHTML = 'Ver'
    delBtn.className = 'btn btn-block btn-dark st-btn'
    delBtn.setAttribute('id_asiento', id)
    row.insertCell(3).appendChild(delBtn)
  }
})()
