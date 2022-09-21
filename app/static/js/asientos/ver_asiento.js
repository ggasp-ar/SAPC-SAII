(() => {
  document.querySelector('input[id="descripcion"]').disabled = true
  document.querySelector('input[id="datePicker"]').disabled = true

  const btnFinalizarAsiento = document.querySelector('button[id="finalizar"]')
  btnFinalizarAsiento.innerHTML = 'Volver Atras'
  btnFinalizarAsiento.style.display = 'block'

  btnFinalizarAsiento.addEventListener('click', function () {
    window.location = '/'
  })
})()
