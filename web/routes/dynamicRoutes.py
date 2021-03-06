from flask import Blueprint
import controllers
    
dynamicBP = Blueprint('dynamic', __name__)

dynamicBP.route('/upload', methods=['POST'])(controllers.dynControllers.dyn)
dynamicBP.route('/ec2-on/<string:siteId>', methods=['GET'])(controllers.dynControllers.ec2_on)
dynamicBP.route('/toggleEC2/<string:siteId>/<string:instanceId>', methods=['GET'])(controllers.dynControllers.toggleEC2)
dynamicBP.route('/deploy/<string:siteId>/<string:instanceId>', methods=['GET'])(controllers.dynControllers.deploy)
dynamicBP.route('/visit/<string:siteId>/<string:instanceId>', methods=['GET'])(controllers.dynControllers.visit)
dynamicBP.route('/viewStats/<string:siteId>/<string:instanceId>', methods=['GET'])(controllers.dynControllers.visitStatsPage)
    