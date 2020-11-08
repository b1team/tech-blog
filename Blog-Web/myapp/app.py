from app import app
from app.views.login.login import login_bp
from app.views.home.home import home_bp
from app.views.register.register import register_bp
from app.views.about.about import about_bp
from app.views.post.post import post_bp

app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(about_bp)
app.register_blueprint(post_bp)


if __name__ == "__main__":
    app.run(debug=True)
