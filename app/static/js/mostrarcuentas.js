(() => {
  const data = $('#tdata')[0].innerHTML
  const addAccMenuBtn = $('#addaccmenu')[0]
  const addAccForm = $('#addaccform')[0]
  const newAccForm = $('#accform')
  const addAccBtn = $('#addacc')[0]

  $('#tdata')[0].innerHTML = ''
  $('#tree').treeview(
    {
      data: JSON.parse(data),
      showTags: true,
      levels: 2,
      onNodeSelected: function (event, data) {
        $('#inforow')[0].style.visibility = 'visible'
        $('#nombre-cuenta')[0].innerHTML = data.text + ' # ' + data.codigo
        $('#saldo-cuenta')[0].value = data.saldo
        $('#tipo-cuenta')[0].innerHTML = 'Tipo: ' + data.tipo.descripcion
        if (data.recibe) {
          addAccMenuBtn.disabled = true
        } else {
          addAccMenuBtn.disabled = false
        }
        ocultarElemento(addAccForm)
        newAccForm[0].reset()
      }
    })

  function ocultarElemento (elem) {
    elem.style.display = 'none'
  }
  function mostrarElemento (elem) {
    elem.style.display = 'block'
  }

  addAccMenuBtn.addEventListener('click', () => {
    addAccMenuBtn.disabled = true
    mostrarElemento(addAccForm)
  })

  addAccBtn.addEventListener('click', function () {
    const treeSel = $('#tree').treeview('getSelected')[0]
    const data = newAccForm.serializeArray().reduce(function (obj, item) {
      obj[item.name] = item.value
      return obj
    }, {})
    if (data.recibeSaldo === 'on') {
      data.recibe = true
    } else {
      data.recibe = false
    }
    data.padre_cid = treeSel.cid
    data.tipo_id = treeSel.tipo.id
    confirmarCuenta(data)
  })

  const confirmarCuenta = (data) => {
    Swal.fire({
      title: '¿Está seguro?',
      inputAttributes: {
        autocapitalize: 'off'
      },
      showCancelButton: true,
      cancelButtonColor: '#d33',
      cancelButtonText: 'Cancelar carga',
      confirmButtonText: 'Agregar',
      confirmButtonColor: '#2b3436',
      backdrop: 'rgba(0,0,0,0.8)',
      showLoaderOnConfirm: true,
      preConfirm: () => {
        return fetch(`${window.origin}/registrarcuenta`, {
          method: 'POST',
          mode: 'same-origin',
          Credentials: 'same-origin',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': data.csrf_token
          },
          body: JSON.stringify({
            cuenta: data.Cuenta,
            codigo: data.Codigo,
            recibe: data.recibe,
            padre_cid: data.padre_cid,
            tipo: data.tipo_id
          })
        }).then(response => {
          if (!response.ok) {
            notificacionSwal('Error', response.statusText, 'error', 'Cerrar')
          }
          return response.json()
        }).then(respData => {
          if (respData.exito) {
            document.forms.accform.reset()
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
})()
