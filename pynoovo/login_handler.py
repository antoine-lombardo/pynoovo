import json, logging
from typing import Dict, List
from datetime import datetime, timedelta
import base64
from copy import deepcopy

from .common.login_handler import LoginHandler
from .consts import *

# Logger
logger = logging.getLogger(__name__)

class NoovoLoginHandler(LoginHandler):
    access_token: str = None
    refresh_token: str = None
    expiry: datetime = None

    scopes: List[str] = None
    subscriptions: List[str] = None
    packages: List[str] = None

    def __init__(self, cache_dir, session, username=None, password=None, site='bell'):
        super().__init__(cache_dir, session, username, password)
        if self.username is None or self.password is None or site is None:
            self._load_cache()
        else:
            self._load_cache()
            if self.username != username or self.password != password or self.site != site:
                self.access_token = None
                self.refresh_token = None
                self.expiry = None
                self.subscriptions = None
                self.scopes = None
                self.packages = None
                self.username = username
                self.password = password
                self.site = site
                self.profile_id = None
                self._save_cache()
        self.ensure_login(False)


    # ===================================================================
    #   LOGIN
    # ===================================================================

    def login(self, username: str, password: str) -> bool:
        logger.debug('Logging in...')
        # Set username and password
        self.username = username
        self.password = password
        self.access_token = None
        self.refresh_token = None
        self.expiry = None
        self.subscriptions = None
        # Make login
        return self.ensure_login()

    def logout(self) -> None:
        logger.debug('Logging out...')
        self.username = None
        self.password = None
        self.access_token = None
        self.refresh_token = None
        self.expiry = None
        self.subscriptions = None
        self._save_cache()

    def ensure_login(self, force_refresh: bool = False) -> bool:
        #===========================================================
        # Check credentials
        #===========================================================
        if self.username is None or self.password is None or self.site is None:
            self.access_token = None
            self.refresh_token = None
            self.site = None
            self.profile_id = None
            self.expiry = None
            self.subscriptions = None
            self._save_cache()
            if self.site is None:
                logger.info('Cannot ensure logging: No logging site provided')
            else:
                logger.info('Cannot ensure logging: No username or password provided')
            return False

        #===========================================================
        # Skip if current token is valid
        #===========================================================
        if not self._check_expiry() and not force_refresh:
            return True

        #===========================================================
        # Refresh token if possible
        #===========================================================
        response = None
        if self.refresh_token is not None and self.profile_id is not None:
            logger.debug('Refreshing token...')
            response = self._make_refresh_request()
            if response.status_code != 200:
                logger.debug('Refreshing token failed')
                response = None

        #===========================================================
        # Do a username/password login if required
        #===========================================================
        if response is None:
            try:
                # external site login
                logger.debug('Trying username/password login...')
                base_response = self._make_login_request()
                if base_response.status_code == 200:
                    base_access_token = json.loads(base_response.text)['access_token']
                    # generate magic token
                    magic_response = self._make_magic_request(base_access_token)
                    if magic_response.status_code == 200 or magic_response.status_code == 201:
                        magic_token = magic_response.text.replace('==', '')
                        # login using magic token
                        response = self._make_magic_login_request(magic_token)
            except:
                pass

        #===========================================================
        # Handle refresh + login failure
        #===========================================================
        if response is None or response.status_code != 200:
            logger.info('Login failed')
            # Reset attributes
            self.access_token = None
            self.refresh_token = None
            self.site = None
            self.profile_id = None
            self.expiry = None
            self.subscriptions = None
            self._save_cache()
            return False

        #===========================================================
        # Parse refresh/login response
        #===========================================================
        try:
            response_parsed = json.loads(response.text)
            self.access_token = response_parsed['access_token']
            self.refresh_token = response_parsed['refresh_token']
            self.profile_id = response_parsed['profile_id'] if 'profile_id' in response_parsed else None
            self.expiry = datetime.now() + timedelta(0,response_parsed['expires_in'])
            # Profile ID
            if self.profile_id is None:
                profile_response = self._make_profile_request()
                self.profile_id = json.loads(profile_response.text)[0]['id']
            # Scopes
            scopes = response_parsed['scope'].split(' ')
            for scope in scopes:
                if scope.startswith('subscription:'):
                    self.scopes = scope.replace('subscription:', '').split(',')
            # Subscriptions
            self.subscriptions = []
            for scope in self.scopes:
                if scope in SCOPE_TO_SUBSCRIPTION_NAME:
                    self.subscriptions.append(SCOPE_TO_SUBSCRIPTION_NAME[scope])
            # Packages
            self.packages = []
            for subscription in self.subscriptions:
                if subscription in SUBSCRIPTION_NAME_TO_PACKAGE_NAME:
                    self.packages.append(SUBSCRIPTION_NAME_TO_PACKAGE_NAME[subscription])
            self._save_cache()
            logger.debug('New token acquired. Valid until: {}'.format(self.expiry.strftime("%Y/%m/%d %H:%M:%S")))
            return True
        except:
            #===========================================================
            # Handle invalid refresh/login response
            #===========================================================
            logger.info('Refresh/login response invalid')
            self.access_token = None
            self.refresh_token = None
            self.site = None
            self.profile_id = None
            self.expiry = None
            self.subscriptions = None
            self._save_cache()
            return False

    # ===================================================================
    #   REQUESTS
    # ===================================================================

    def _make_refresh_request(self):
        logger.debug('Making a refresh request...')
        url = LOGIN_SITES[self.site]['refresh']['url']
        headers = deepcopy(LOGIN_SITES[self.site]['refresh']['headers'])
        body = LOGIN_SITES[self.site]['refresh']['body'].format(refresh_token=self.refresh_token, profile_id=self.profile_id)
        return self.session.post(url=url, headers=headers, data=body)

    def _make_login_request(self):
        logger.debug('Logging in user username and password...')
        url = LOGIN_SITES[self.site]['login']['url']
        headers = deepcopy(LOGIN_SITES[self.site]['login']['headers'])
        body = LOGIN_SITES[self.site]['login']['body'].format(username=self.username, password=self.password)
        return self.session.post(url=url, headers=headers, data=body)

    def _make_magic_request(self, access_token):
        logger.debug('Generating magic token...')
        url = LOGIN_SITES[self.site]['magic']['url']
        headers = deepcopy(LOGIN_SITES[self.site]['magic']['headers'])
        headers['authorization'] = 'Bearer {}'.format(access_token)
        return self.session.post(url=url, headers=headers)

    def _make_magic_login_request(self, magic_token):
        logger.debug('Logging in using magic token...')
        url = LOGIN_SITES[self.site]['magic_login']['url']
        headers = deepcopy(LOGIN_SITES[self.site]['magic_login']['headers'])
        body = LOGIN_SITES[self.site]['magic_login']['body'].format(magic_token=magic_token)
        return self.session.post(url=url, headers=headers, data=body)

    def _make_profile_request(self):
        logger.debug('Getting profile ID...')
        url = PROFILE_URL
        headers = deepcopy(BASE_HEADERS)
        headers['authorization'] = 'Bearer {}'.format(self.access_token)
        return self.session.get(url=url, headers=headers)

    # ===================================================================
    #   TOKEN EXPIRY HANDLER
    # ===================================================================

    def _check_expiry(self) -> bool:
        # Check if credentials are provided
        if self.expiry is None or self.access_token is None or self.refresh_token is None:
            return True
        if self.expiry < datetime.now() - timedelta(0, 3600):
            return True
        return False

    # ===================================================================
    #   OVERLOADS
    # ===================================================================

    def _process_cache_obj(self, cache_obj) -> bool:
        if cache_obj is not None:
            try:
                self.username = cache_obj['username']
                self.password = cache_obj['password']
                self.site = cache_obj['site']
                self.profile_id = cache_obj['profile_id']
                self.access_token = cache_obj['access_token']
                self.refresh_token = cache_obj['refresh_token']
                self.subscriptions = cache_obj['subscriptions']
                self.scopes = cache_obj['scopes']
                self.packages = cache_obj['packages']
                try:
                    self.expiry = datetime.strptime(cache_obj['expiry'], '%Y/%m/%d %H:%M:%S')
                except:
                    self.expiry = None
                return True
            except:
                pass
        self.username = None
        self.password = None
        self.site = None
        self.profile_id = None
        self.access_token = None
        self.refresh_token = None
        self.expiry = None
        self.subscriptions = None
        self.scopes = None
        self.packages = None
        return False

    def _create_cache_obj(self) -> Dict[str, str]:
        try:
            expiry = self.expiry.strftime("%Y/%m/%d %H:%M:%S")
        except:
            expiry = None
        return  {
        'username': self.username,
        'password': self.password,
        'site': self.site,
        'profile_id': self.profile_id,
        'access_token': self.access_token,
        'refresh_token': self.refresh_token,
        'expiry': expiry,
        'subscriptions': self.subscriptions,
        'scopes': self.scopes,
        'packages': self.packages
        }