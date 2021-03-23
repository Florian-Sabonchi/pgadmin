import config
from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask import current_app, url_for, session
from flask_babelex import gettext
from flask_security import login_user
from pgadmin.authenticate.internal import BaseAuthentication
from pgadmin.model import User
from pgadmin.tools import user_management
from pgadmin.utils.constants import OAUTH

from web.pgadmin.model import db

oauth_obj = OAuth(Flask(__name__))


def get_redirect_uri():
    return url_for('authenticate.oauth_authorize',
                   _external=True)


class OAuthAuthentication(BaseAuthentication):
    """OAuth Authentication Class"""

    def get_source_name(self):
        return OAUTH

    def get_friendly_name(self):
        return gettext("oauth2")

    def validate(self, form):
        return True

    def login(self, auth_obj):
        session['token'] = session['provider'].authorize_access_token()
        resp = session['provider'].get(config.OAUTH_ENDPOINT_NAME).json()

        if 'email' not in resp or not resp['email']:
            current_app.logger.exception(
                'An email is required for authentication'
            )
            return False

        if self.__auto_create_user(resp):
            user = db.session.query(User).filter_by(email=resp['email']).first()
            if user.username != resp['name']:
                try:
                    user.username = resp['name']
                    db.session.commit()
                except Exception as e:
                    current_app.logger.exception(e)
                    return False
            auth_obj.set_source_friendly_name(self.get_friendly_name())
            auth_obj.set_current_source(self.get_source_name())
            return login_user(user)
        return False

    def authenticate(self, form):
        session['provider'] = oauth_obj.register(
            name=config.OAUTH2_NAME,
            client_id=config.OAUTH2_CLIENT_ID,
            client_secret=config.OAUTH2_CLIENT_SECRET,
            access_token_url=config.OAUTH2_TOKEN_URL,
            authorize_url=config.OAUTH2_AUTHORIZATION_URL,
            api_base_url=config.OAUTH2_API_BASE_URL,
            userinfo_endpoint=config.OAUTH2_USERINFO_ENDPOINT,
            client_kwargs={'scope': 'email profile'},
        )
        return True, get_redirect_uri()

    def __auto_create_user(self, resp):
        user = User.query.filter_by(email=resp['email']).first()
        if not user:

            if 'name' in resp and resp['name']:
                name = resp['name']
            elif 'preferred_username' in resp and resp['preferred_username']:
                name = resp['preferred_username']
            else:
                current_app.logger.exception(
                    'Missing username ("name" or "preferred_username")'
                )
                return False

            return user_management.create_user({
                'username': name,
                'email': resp['email'],
                'role': 2,
                'active': True,
                'auth_source': OAUTH
            })
        return True
