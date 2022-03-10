from flask import Blueprint
import controllers
    
dash = Blueprint('dash', __name__)

dash.route('/', methods=['GET'])(controllers.dashControllers.sendDash)


    