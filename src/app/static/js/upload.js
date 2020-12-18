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
        alert("Avatar was updated");
        imagefile.value = "";
        location.reload();
    }).catch(function(error){
        response = error.response
        alert(response.data.message);
    })
}
