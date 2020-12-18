function upload_file(){
    var formData = new FormData();
    var imagefile = document.querySelector('#file-input');
    formData.append("file", imagefile.files[0]);
    axios.post('/avatar/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
    }).then(function(response){
        console.log(response);
        let timerInterval;
        Swal.fire({
            icon: 'success',
            title: 'Avatar has been updated',
            showConfirmButton: false,
            timer: 50000,
        });
        imagefile.value = "";
        location.reload();
    }).catch(function(error){
        response = error.response;
        Swal.fire({
			title: response.data.message,
			showClass: {
				popup: "animate__animated animate__fadeInDown",
			},
			hideClass: {
				popup: "animate__animated animate__fadeOutUp",
			},
		});
    })
}

function info_update(){
    Swal.fire({
		icon: "success",
		title: "Your work has been saved",
		showConfirmButton: false,
		timer: 1500,
	});
}