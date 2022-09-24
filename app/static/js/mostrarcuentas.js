(() => {
  const data = $('#tdata')[0].innerHTML
  $('#tree').treeview(
    {
      data: JSON.parse(data),
      showTags: true,
      levels: 2,
      onNodeSelected: function (event, data) {
        $('#inforow')[0].style.visibility = 'visible'
        console.log(data)
        $('#nombre-cuenta')[0].innerHTML = data.text
        $('#saldo-cuenta')[0].value = data.saldo
        $('#tipo-cuenta')[0].innerHTML = 'Tipo: ' + data.tipo.descripcion
        const addAccBtn = $('#addacc')[0]
        if (data.recibe) {
          addAccBtn.disabled = true
          console.log('recibe saldo')
        } else {
          addAccBtn.disabled = false
        }
      }
    })
  $('#tdata')[0].innerHTML = ''
})()
