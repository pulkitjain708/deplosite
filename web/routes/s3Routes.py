from flask import Blueprint
import controllers
    
s3RouteBP = Blueprint('upload', __name__)

s3RouteBP.route('/static', methods=['POST'])(controllers.s3Controllers.static)
s3RouteBP.route('/delete/<string:bucketName>', methods=['GET'])(controllers.s3Controllers.delete)
s3RouteBP.route('/getLogs', methods=['GET'])(controllers.s3Controllers.getLogs)


    