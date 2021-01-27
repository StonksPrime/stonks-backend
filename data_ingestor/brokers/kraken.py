import broker_interface
import requests
import urllib.parse
import hashlib
import hmac
import base64
import time

class KrakenAPI(broker_interface.BrokerInterface):
    """ Loads a session for a given user with the broker
    """


    def __init__(self, user='', password=''):
        """ Create an object with authentication information.
        :param user: (optional)
        :type password: str
        :param password: (optional) 
        :type password: str
        :returns: None
        """
        self.key = user
        self.secret = password
        self.uri = 'https://api.kraken.com'
        self.apiversion = '0'
        self.session = requests.Session()
        self.response = None
        self._json_options = {}
        return

    def login(self, user, password):
        """ Load user session with broker
        :param user: user or key 
        :type user: str
        :param password: (optional) actual private key used to sign messages
        :type secret: str
        :returns: None
        """
        self.key = user
        self.secret = password


    def logout(self):
        """ Close this session.
        :returns: None
        """
        self.session.close()

    def getCurrentPositions(self):
        
        data = self.query_private('Balance')
        print(data)


    def getAssetByISIN(self, isin):
        products = self.degiroClient.search_products(isin)
        productId = Product(products[0]).id

        info = self.degiroClient.product_info(productId)
        print(info["id"], info["name"], info["currency"], info["closePrice"])


    def _query(self, urlpath, data, headers=None, timeout=None):
        """ Low-level query handling.
        .. note::
           Use :py:meth:`query_private` or :py:meth:`query_public`
           unless you have a good reason not to.
        :param urlpath: API URL path sans host
        :type urlpath: str
        :param data: API request parameters
        :type data: dict
        :param headers: (optional) HTTPS headers
        :type headers: dict
        :param timeout: (optional) if not ``None``, a :py:exc:`requests.HTTPError`
                        will be thrown after ``timeout`` seconds if a response
                        has not been received
        :type timeout: int or float
        :returns: :py:meth:`requests.Response.json`-deserialised Python object
        :raises: :py:exc:`requests.HTTPError`: if response status not successful
        """
        if data is None:
            data = {}
        if headers is None:
            headers = {}

        url = self.uri + urlpath

        self.response = self.session.post(url, data = data, headers = headers,
                                          timeout = timeout)

        if self.response.status_code not in (200, 201, 202):
            self.response.raise_for_status()

        return self.response.json(**self._json_options)

    def query_private(self, method, data=None, timeout=None):
        """ Performs an API query that requires a valid key/secret pair.
        :param method: API method name
        :type method: str
        :param data: (optional) API request parameters
        :type data: dict
        :param timeout: (optional) if not ``None``, a :py:exc:`requests.HTTPError`
                        will be thrown after ``timeout`` seconds if a response
                        has not been received
        :type timeout: int or float
        :returns: :py:meth:`requests.Response.json`-deserialised Python object
        """
        if data is None:
            data = {}

        if not self.key or not self.secret:
            raise Exception('Either key or secret is not set! (Use `load_key()`.')

        data['nonce'] = int(1000*time.time())

        urlpath = '/' + self.apiversion + '/private/' + method

        headers = {
            'API-Key': self.key,
            'API-Sign': self._sign(data, urlpath)
        }

        return self._query(urlpath, data, headers, timeout = timeout)


    def _sign(self, data, urlpath):
        """ Sign request data according to Kraken's scheme.
        :param data: API request parameters
        :type data: dict
        :param urlpath: API URL path sans host
        :type urlpath: str
        :returns: signature digest
        """
        postdata = urllib.parse.urlencode(data)

        # Unicode-objects must be encoded before hashing
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
        sigdigest = base64.b64encode(signature.digest())

        return sigdigest.decode()