class validationError(Exception):
    pass

class UserDetailsNotProvided(Exception):
    pass

class UserAlreadyExists(Exception):
    pass

class NoSearchParamGiven(Exception):
    pass

class UserDoesNotExist(Exception):
    pass

class NoDataBaseSession(Exception):
    pass

class InvalidUpdate(Exception):
    pass

class CategoryDetailsNotProvided(Exception):
    pass

class CategoryDoesNotExists(Exception):
    pass

class ProductDetailsNotProvided(Exception):
    pass

class InvalidName(Exception):
    pass