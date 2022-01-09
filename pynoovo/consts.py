from base64 import b64encode

# ===================================================================
#
#   LOGIN HANDLER CONFIG
#
# ===================================================================

PROFILE_URL = 'https://account.bellmedia.ca/api/profile/v1.1'

LOGIN_SITES = {
    'bell': {
        'login': {
            'url': 'https://account.bellmedia.ca/api/login/v2.1',
            'body': 'username={username}&password={password}&grant_type=bdu_password&provider_id=urn:bell:ca:idp:prod',
            'headers': {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate',
                'accept-language': 'fr-CA,en-US;q=0.9',
                'authorization': 'Basic ' + b64encode('usermgt:default'.encode()).decode(),
                'connection': 'keep-alive',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'origin': 'https://account.bellmedia.ca',
                'referer': 'https://account.bellmedia.ca/bdu/?loginUrl=https://account.bellmedia.ca/api/login/v2.1?grant_type=bdu_password&provider_id=urn:bell:ca:idp:prod',
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; LG-US998 Build/OPR1.170623.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.137 Mobile Safari/537.36',
                'x-requested-with': 'com.vmediagroup.noovo'
            }
        },
        'magic': {
            'url': 'https://account.bellmedia.ca/api/magic-link/v2.1/generate',
            'headers': {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate',
                'accept-language': 'fr-CA,en-US;q=0.9',
                'authorization': 'TO FILL',
                'connection': 'keep-alive',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'origin': 'https://account.bellmedia.ca',
                'referer': 'https://account.bellmedia.ca/bdu/?loginUrl=https://account.bellmedia.ca/api/login/v2.1?grant_type=bdu_password&provider_id=urn:bell:ca:idp:prod',
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; LG-US998 Build/OPR1.170623.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.137 Mobile Safari/537.36',
                'x-requested-with': 'com.vmediagroup.noovo'
            }
        },
        'magic_login': {
            'url': 'https://account.bellmedia.ca/api/login/v2.1?grant_type=magic_link_token',
            'body': 'magic_link_token={magic_token}',
            'headers': {
                'accept-encoding': 'gzip',
                'authorization': 'Basic ' + b64encode('noovo-android:default'.encode()).decode(),
                'connection': 'keep-alive',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'okhttp/4.9.0'
            }
        },
        'refresh': {
            'url': 'https://account.bellmedia.ca/api/login/v2.1?grant_type=refresh_token',
            'body': 'refresh_token={refresh_token}&profile_id={profile_id}',
            'headers': {
                'accept-encoding': 'gzip',
                'authorization': 'Basic ' + b64encode('noovo-android:default'.encode()).decode(),
                'connection': 'keep-alive',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'okhttp/4.9.0'
            }
        }
    }
}





# ===================================================================
#
#   GRAPHQL CONFIG
#
# ===================================================================

GRAPHQL_URL = 'https://www.crave.ca/space-graphql/graphql/'





# ===================================================================
#
#   SUBSCRIPTIONS CONFIG
#
# ===================================================================

DESTINATION_TO_SUBSCRIPTION = {
  'starz_atexace': 'starz',
  'crave_atexace': 'crave',
  'se_atexace':    'superecran'
}

SUBSCRIPTION_NAME_TO_PACKAGE_NAME = {
  'Z':          'z_hub',
  'CANAL_D':    'canald_hub',
  'CANAL_VIE':  'canalvie_hub'
}

SCOPE_TO_SUBSCRIPTION_NAME = {
  'cand':       'CANAL_D',
  'canv':       'CANAL_VIE',
  'noovo':      'NOOVO',
  'ztele':      'Z',
}



# ===================================================================
#
#   HEADERS
#
# ===================================================================

BASE_HEADERS = {
  'accept-encoding': 'gzip',
  'connection': 'Keep-Alive',
  'user-agent': 'okhttp/4.9.0'
}

CAPI_HEADERS = {
  'accept-encoding': 'identity',
  'connection': 'Keep-Alive',
  'user-agent': 'okhttp/4.9.0'
}

HEADERS = {
  'accept': 'application/json',
  'accept-encoding': 'gzip',
  'connection': 'Keep-Alive',
  'content-type': 'application/json; charset=utf-8',
  'graphql-client-platform': 'entpay_android',
  'user-agent': 'okhttp/4.9.0'
}