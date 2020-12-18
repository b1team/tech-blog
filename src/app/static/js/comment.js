
String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
}

  function loadComments(page) {
    document.getElementById("comment-box").innerHTML = "";
    axios.get("/loadcmt?page={0}".format(page))
      .then(function (response) {
        console.log(response)
        var comments = response.data.data;
        for (comment of comments) {
          var node = document.createElement("div");
          var avatar_url = "/static/images/50x50.png";
          if(comment.avatar_url){
            avatar_url = comment.avatar_url;
          }
          var comment_html = 
               `<div class="comment media mb-4">
                <img class="d-flex mr-3 rounded-circle" src="{0}" alt="">
                <div class="media-body">
                <h5 class="mt-0"> {1}  - <small>{2}</small></h5>
                 {3}
              </div>
            </div>`.format(avatar_url, comment.username, comment.created_at, comment.content);

          }
          node.innerHTML = comment_html;
          document.getElementById("comment-box").appendChild(node);
          pagenation(response.data.num_of_page);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      });
}

  function addComment() {
    var content = document.getElementById("create_comment").value;
    if(!content){
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Please enter content',
          })
      return;
    }
    axios.post("/addcmt", {"comment": content})
      .then(function (response) {
        var login = response.data.login;
        if(!login){
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Please login',
            footer: '<a href="/login">Login</a>'
          })
        }

        document.getElementById("create_comment").value = "";
        loadComments()
      })
      .catch(function (error){
        console.log(error);
      })
  }

function pagenation(num_of_page){
    document.getElementById('pagination').innerHTML = "";
    var num_of_page = num_of_page;
    for (var i = 0; i < num_of_page; i++){
      var node = document.createElement("div")
      var pagenation = `<button type="button" class="btn btn-link" 
      onclick="loadComments({0}); return false;">{1}</button>`.format(i, i+1);
      node.innerHTML = pagenation;
      document.getElementById('pagination').appendChild(node);
    }
}