from flask import Blueprint
import controllers
    
dash = Blueprint('dash', __name__)

dash.route('/', methods=['GET'])(controllers.dashControllers.sendDash)
dash.route('/list-sites', methods=['GET'])(controllers.dashControllers.sendListSites)
dash.route('/new-site', methods=['GET'])(controllers.dashControllers.sendNewSite)
dash.route('/stats/<string:bucketName>', methods=['GET'])(controllers.dashControllers.individualStats)
dash.route('/changeEmail/<string:username>', methods=['POST'])(controllers.dashControllers.changeEmail)
dash.route('/changePassword/<string:username>', methods=['POST'])(controllers.dashControllers.changePassword)
dash.route('/dynamic-sites', methods=['GET'])(controllers.dashControllers.sendDynamicSites)


    