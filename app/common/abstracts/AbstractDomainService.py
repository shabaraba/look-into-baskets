from datetime import datetime

import app.database as db

from app import logger
from app.config import AppConfig
from app.lib.Smaregi.config import config as SmaregiConfig

class AbstractDomainService():
    def __init__(self, account):
        self._appConfig = None
        self._apiConfig = None
        self._loginAccount = account
        self._logger = None

    def withSmaregiApi(self, _accessToken, _contractId):
        self._appConfig = AppConfig()
        self._apiConfig = SmaregiConfig(
            self._appConfig.ENV_DIVISION,
            self._appConfig.SMAREGI_CLIENT_ID,
            self._appConfig.SMAREGI_CLIENT_SECRET,
            self._logger
        )
        self._apiConfig.accessToken = _accessToken
        self._apiConfig.contractId = _contractId

        return self

