from flask import Blueprint
import controllers
    
s3RouteBP = Blueprint('upload', __name__)

s3RouteBP.route('/static', methods=['POST'])(controllers.s3Controllers.static)
s3RouteBP.route('/delete/<string:bucketName>', methods=['POST'])(controllers.s3Controllers.delete)

    