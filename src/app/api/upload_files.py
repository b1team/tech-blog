import os
from werkzeug.utils import secure_filename
from flask import (send_from_directory, jsonify, request, Blueprint, session,
        abort)
from src.app import app


upload_file_router = Blueprint("upload_file_api", __name__)


def upload_image(file_name: str = None):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if 'file' not in request.files:
        return jsonify(message='No file part', success=False), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(message='No selected file', success=False), 400
    if file and allowed_file(file.filename):
        if not file_name:
            filename = secure_filename(file.filename)
        else:
            s_file_name = secure_filename(file.filename)
            ext = s_file_name[s_file_name.rfind("."):]
            filename = f"{file_name}{ext}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
        file.save(file_path)
        return jsonify(path=f"/images/{filename}", message="File successfully uploaded", success=True), 201
    else:
        return jsonify(message="File extension is invalid", success=False), 400


@upload_file_router.route('/image/upload', methods=['POST'])
def upload_file():
    return upload_image()


@upload_file_router.route('/avatar/upload', methods=['POST'])
def upload_avatar():
    user_id = session.get("user_id")
    if not user_id:
        return abort(401)
    return upload_image(f"avatar/{user_id}")


@upload_file_router.route('/images/avatar/<filename>')
def show_avatars(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], "avatar"), filename)


@upload_file_router.route('/images/<filename>')
def show_images(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
