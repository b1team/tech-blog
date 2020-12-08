
  window.onload = function() {
    loadComments(0);
};

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
          var comment_html = 
               `<div class="comment media mb-4">
                <img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">
                <div class="media-body">
                <h5 class="mt-0"> {0}  - <small>{1}</small></h5>
                 {2}
              </div>
            </div>`.format(comment.username, comment.created_at, comment.content);
          node.innerHTML = comment_html;
        document.getElementById("comment-box").appendChild(node); 
        }
  
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      });
}

  function addComment() {
    var content = document.getElementById("create_comment").value;
    if(!content){
      alert("Please enter comment");
      return
    }
    axios.post("/addcmt", {"comment": content})
      .then(function (response) {
        document.getElementById("create_comment").value = "";
        loadComments()
      })
  }
