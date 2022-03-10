from flask import Blueprint
import controllers
    
slash = Blueprint('root', __name__)

slash.route('/', methods=['GET'])(controllers.rootControllers.sendSlash)
slash.route('/login', methods=['GET'])(controllers.rootControllers.sendLogin)
slash.route('/register', methods=['GET'])(controllers.rootControllers.sendRegister)
slash.route('/signUpUser', methods=['POST'])(controllers.rootControllers.registerUser)
slash.route('/signInUser', methods=['POST'])(controllers.rootControllers.loginUser)

    