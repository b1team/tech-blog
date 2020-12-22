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
        Swal.fire({
			title: "Your avatar has been uploaded",
			icon: "success",
			confirmButtonColor: "#3085d6",
			confirmButtonText: "OK",
		}).then((result) => {
			if (result.isConfirmed) {
                imagefile.value = "";
                location.reload();
			}
		});
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
		title: "Info has been update",
		showConfirmButton: false,
		timer: 2000,
	});
}