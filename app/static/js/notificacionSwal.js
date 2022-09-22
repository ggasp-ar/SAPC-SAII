const notificacionSwal = (titleText, maintext, notifIcon, confirmText) => {
  Swal.fire({
    title: titleText,
    text: maintext,
    icon: notifIcon,
    confirmButtonText: confirmText,
    confirmButtonColor: '#8fce00',
    backdrop: 'rgba(0,60,0,0.7)'
  })
}
