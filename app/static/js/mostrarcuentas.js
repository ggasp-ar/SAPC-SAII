(() => {
  $('document').ready($('#tree').treeview(
    {
      data: arbol,
      levels: 2,
      onNodeSelected: function (event, data) {
        $('#inforow')[0].style.visibility = 'visible'
        console.log(data)
        $('#nombre-cuenta')[0].innerHTML = `(${data.tipo.tipo})  ` + data.text
        $('#saldo-cuenta')[0].value = data.saldo
        $('#tipo-cuenta')[0].innerHTML = 'Tipo: ' + data.tipo.descripcion
      }
    }))
})()
