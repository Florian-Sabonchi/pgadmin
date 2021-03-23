.. _enabling_ldap_authentication:

**************************************************
`Enabling OAUTH Authentication`:index:
**************************************************


To enable OAUTH authentication for pgAdmin, you must configure the OAUTH
settings in the *config_local.py* or *config_system.py* file (see the
:ref:`config.py <config_py>` documentation) on the system where pgAdmin is
installed in Server mode. You can copy these settings from *config.py* file
and modify the values for the following parameters:


.. csv-table::
   :header: "**Parameter**", "**Description**"
   :class: longtable
   :widths: 35, 55

   "AUTHENTICATION_SOURCES","The default value for this parameter is *internal*.
   To enable LDAP authentication, you must include *oauth* in the list of values
   for this parameter. you can modify the value as follows:

   * [‘oauth’, ‘internal’]: pgAdmin will display an additional button for authenticating with oauth

    "OAUTH2_NAME", "The name of the of the oauth provider"
    "OAUTH2_CLIENT_ID","Oauth client id'
    "OAUTH2_CLIENT_SECRET", "Oauth secret"
    "OAUTH2_TOKEN_URL","This url is used to generate a token for OpenID Connect."
    "OAUTH2_AUTHORIZATION_URL", "This url is used for authentication"
    "OAUTH2_API_BASE_URL", "Oauth base url"
    "OAUTH2_USERINFO_ENDPOINT", "Endpoint for openid connect"
    "OAUTH_ENDPOINT_NAME", "Name of the Endpoint"

Important note: if you change the e-mail address stored in the account, the account will be lost.
Because the e-mail address is used to find a user.