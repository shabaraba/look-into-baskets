import responder
from app.controllers import *


def add_routers(api: responder.API):
    # api.add_route("/accounts/token", AuthController.getToken)
    api.add_route('/favicon.ico', HomeController.favicon)

    api.add_route('/accounts/login', AuthController.login)
    api.add_route('/accounts/logout', AuthController.logout)
    api.add_route('/accounts/authorize', AuthController.authorize)
    api.add_route('/baskets/associate', BasketController.Associate)
    api.add_route('/baskets/associate/result', BasketController.AssociateResult)

    api.add_route('/webhook', WebhookController.Webhook)
    api.add_route('/', HomeController.index)
