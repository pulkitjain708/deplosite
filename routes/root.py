from flask import Blueprint
from controllers.root import sendLogin,sendSlash,sendRegister

root = Blueprint('root', __name__)

root.route('/', methods=['GET'])(sendSlash)
root.route('/login', methods=['GET'])(sendLogin)
root.route('/register', methods=['GET'])(sendRegister)
