from flask import Blueprint
from controllers.rootControllers import (sendSlash,sendLogin,sendRegister,registerUser)

main_route = Blueprint('root', __name__)

main_route.route('/', methods=['GET'])(sendSlash)
main_route.route('/login', methods=['GET'])(sendLogin)
main_route.route('/register', methods=['GET'])(sendRegister)
main_route.route('/signUpUser', methods=['POST'])(registerUser)
