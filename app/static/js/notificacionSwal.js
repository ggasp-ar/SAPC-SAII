const notificacionSwal=(titleText, text, icon, confirmButtonText) => {
    Swal.fire({
        title: titleText,
        text: text,
        icon: icon,
        confirmButtonText: confirmButtonText,
        confirmButtonColor: '#8fce00',
        backdrop: 'rgba(0,60,0,0.7)'
    })
};