
  window.onload = function() {
    popular();
    loadComments(0);
    loadvote();
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
      alert("Please enter comment");
      return
    }
    axios.post("/addcmt", {"comment": content})
      .then(function (response) {
        document.getElementById("create_comment").value = "";
        loadComments()
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

function popular(){
    axios.get("/favorite")
    .then(function (response) {
        console.log(response)
        var data = response.data.top_5
        for(post of data){
            var node = document.createElement("div");
            var html = `
                    <a href="/posts/{0}" class="list-group-item list-group-item-action flex-column align-items-start">
                        <div class="w-100 justify-content-between">
                            <img src="upload/tech_blog_08.jpg" alt="" class="img-fluid float-left">
                            <h5 class="mb-1">{1}</h5>
                            <small>{2}</small>
                        </div>
                    </a>`.format(post.slug, post.title, post.created_at);
            node.innerHTML = html;
            document.getElementById("popular").appendChild(node);
        }
    })
    .catch(function(err) {
        console.log(err);
    })
}