

String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
}

function popular(){
    axios.get("/favorite?top=5")
    .then(function (response) {
        console.log(response)
        var posts = response.data.posts;
        for(post of posts){
            var node = document.createElement("div");
            var html = `
                    <a href="/posts/{0}" class="list-group-item list-group-item-action flex-column align-items-start">
                        <div class="w-100 justify-content-between">
                            <img src="/static/images/tech_blog_04.jpg" alt="pic" class="img-fluid float-left">
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

function loadtag(){
    axios.get("/tags")
        .then(function(response){
            console.log(response);
            var tags = response.data.tags;
            for (tag of tags){
                var node = document.createElement("li")
                var html =`<a href="/tag/{0}">{1}({2})</a>`.format(tag.slug, tag.name, tag.count);
                node.innerHTML = html;
                document.getElementById("list-tags").appendChild(node);
            }
        })
        .catch(function(err) {
            console.log(err);
        })
}

function func_delete() {
	var r = confirm("Delete post");
	if (r == true) {
		return true;
	} else {
		return false;
	}
}