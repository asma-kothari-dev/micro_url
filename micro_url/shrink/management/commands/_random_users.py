import datetime
import requests


class RandomUserMixin(object):
    """ Random User Generator """

    def __get_datetime_from_timestamp(self, timestamp):
        """ Initialize a datetime object with seconds since epoch """

        return datetime.datetime.utcfromtimestamp(timestamp)
    #_______________________________End of __get_datetime_from_timestamp


    # @caller: <_get_random_users>
    def __fetch_random_users(self, count):
        """ Fetches random user using API of randomuser.me.
        :param count: Number of users to be fetched :int:
        :return: :class: `Response <Response>` object
        :rtype: requests.Response        
        """

        response = None
        url = 'http://api.randomuser.me/'
        params = {'results': count}

        try:
            response = requests.get(url, params=params)
        except requests.RequestException, exception_message:
            raise Exception(exception_message)

        if not response.ok:
            exception_message = 'Bad response from randomuser.me'
            raise Exception(exception_message)

        try:
            response = response.json()
        except ValueError, exception_message:
            raise Exception(exception_message)

        return response
    #________________________________________End of __fetch_random_users

    # @caller: <_get_random_users>
    def __organize_random_users(self, response):
        """ Extracts necessary fields from the response """

        results = response.get('results', [])
 
        if not results:
            exception_message = 'No users found in the response from ' \
                'randomusers.me'
            raise Exception(exception_message)

        if not isinstance(results, list):
            exception_message = 'Invalid results received from ' \
                'randomusers.me'
            raise Exception(exception_message)

        users = []

        for result in results:
            # >>> result.keys()
            # [u'picture', u'name', u'dob', u'gender', u'registered',
            #  u'id', u'cell', u'phone', u'location', u'nat', u'login',
            #  u'email']

            # >>> result['name']
            # {u'first': u'fatma', u'last': u'balaban', u'title': u'ms'}
            name = result.get('name', {})

            # >>> result['login']
            # {u'username': u'greenwolf127',
            #  u'sha1': u'ef7f02198adcac7b59ca521efeb36b2216830c7e',
            #  u'sha256': u'b785ef979350149f5dfdef25b9dd3db64f7bdfc7178b2ce9280d0d61e40c3c3d',
            #  u'password': u'hhhhhhhh', u'salt': u'pmLL6D2n',
            #  u'md5': u'd2baa30839836cd60c1d23d29cb3d736'}
            login = result.get('login', {})

            # >>> result['registered']
            # 1144478725
            registered = result.get('registered', None)

            # Extract the required information for user object
            email = result.get('email', None)
            password = login.get('md5', None)
            last_name = name.get('last', None)
            first_name = name.get('first', None)
            username =  login.get('username', None)
            date_joined = self.__get_datetime_from_timestamp(registered)

            user = {'email': email,
                    'username': username,
                    'password': password,
                    'last_name': last_name,
                    'first_name': first_name,
                    'date_joined': date_joined
                    }
            users.append(user)

        return users
    #_____________________________________End of __organize_random_users

    def _get_random_users(self, count):
        """ Gets the random users equal to the count provided.
        :param count: Number of users to be fetched :int:
        :return: List of users, where each user is a dict
        :rtype: list
        """

        try:
            response = self.__fetch_random_users(count)
            users = self.__organize_random_users(response)
            return users
        except Exception, exception_message:
            raise Exception(exception_message)
    #___________________________________________End of _get_random_users

