from src.app import app
from src.app.views.login import login_bp
from src.app.views.home import home_bp
from src.app.views.register import register_bp
from src.app.views.profile import profile_bp
from src.app.views.post import post_bp
from src.app.views.sidebar import sidebar_bp
from src.app.api import upload_file_router

app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(post_bp)
app.register_blueprint(sidebar_bp)
app.register_blueprint(upload_file_router)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
