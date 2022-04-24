from flask import Blueprint
import controllers
    
dynamicBP = Blueprint('dynamic', __name__)

dynamicBP.route('/upload', methods=['POST'])(controllers.dynControllers.dyn)


    