from app import app
from app.views.login import login_bp
from app.views.home import home_bp
from app.views.register import register_bp
from app.views.profile import profile_bp
from app.views.post import post_bp
from app.views.sidebar import sidebar_bp

app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(post_bp)
app.register_blueprint(sidebar_bp)


if __name__ == "__main__":
    app.run(debug=True)
