from flask import Blueprint
import controllers
    
upload = Blueprint('upload', __name__)

upload.route('/static', methods=['POST'])(controllers.uploadControllers.static)
# upload.route('/dynamic', methods=['POST'])(controllers.uploadControllers.dynamic)

    