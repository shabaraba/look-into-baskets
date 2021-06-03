import datetime
from logging import getLogger

from app.models import Accounts as models

"""TODO: lib.Smaregiをpip installでimportできるようにする"""
from app.lib.Smaregi.config import config as SmaregiConfig
from app.lib.Smaregi.API.Authorize import AuthorizeApi


from app.common.managers import SessionManager
from app.common.utils import DictionaryUtil
from app.domains.AccountDomainService import AccountDomainService

from app.config import AppConfig, templates

appConfig = AppConfig()

apiConfig = SmaregiConfig(
    appConfig.ENV_DIVISION,
    appConfig.SMAREGI_CLIENT_ID,
    appConfig.SMAREGI_CLIENT_SECRET
)
authorizeApi = AuthorizeApi(apiConfig, appConfig.APP_URI + '/accounts/login')

logger = getLogger('flask.app')


def authorize(req, resp):
    logger.debug('authorize')
    resp.redirect(authorizeApi.authorize())

async def login(req, resp):
    logger.info('login!!!')
    code = DictionaryUtil.getByKey('code', req.params)
    state = DictionaryUtil.getByKey('state', req.params)

    logger.info('code: {code}, state: {state}')
    if (code is None or state is None):
        resp.redirect('/accounts/authorize', status_code=303)
        return

    accountDomainService = AccountDomainService(req.session).withSmaregiApi(None, None)
    try:
        account = await accountDomainService.loginByCodeAndState(code, state)
    except Exception as e:
        resp.redirect('/', status_code=302)
        return
    
    SessionManager.set(resp.session, SessionManager.KEY_CONTRACT_ID, account.contractId)
    if account.loginStatus == account.LoginStatusEnum.SIGN_UP:
        SessionManager.set(resp.session, SessionManager.KEY_SIGN_UP, True)
    resp.redirect('/baskets', status_code=303)
    return

async def support_login(req, resp):
    if req.params.get("contract_id") is None:
        resp.html = templates.render("home/support_login.pug")
        return
    contract_id = req.params.get("contract_id")
    client_id = req.params.get("client_id")
    secret_id = req.params.get("secret_id")
    accountDomainService = AccountDomainService(req.session)
    account = await accountDomainService.login_for_support_login(
        contract_id,
        client_id,
        secret_id
    )
    if account is None:
        resp.html = templates.render("home/support_login.pug")
        return

    SessionManager.set(resp.session, SessionManager.KEY_CONTRACT_ID, account.contractId)
    if account.loginStatus == account.LoginStatusEnum.SIGN_UP:
        SessionManager.set(resp.session, SessionManager.KEY_SIGN_UP, True)
    resp.redirect('/baskets', status_code=303)
    return

async def logout(req, resp):
    resp.session.clear()
    resp.redirect('/', status_code=303)
    return

