class AuthorizationException(Exception):
    pass


class NotAuthorizedException(Exception):
    pass


class RedirectException(Exception):
    pass


class ServerException(Exception):
    pass

class DataIsNone(Exception):
    pass

class ParseException(DataIsNone):
    pass
