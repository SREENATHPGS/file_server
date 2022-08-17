from . import DB_URL, POSTGRES_DB, engine, Base, session, InvalidUpdate, UserDetailsNotProvided, getApiKey, validationError, CategoryDetailsNotProvided, CategoryDoesNotExists, ProductDetailsNotProvided, InvalidName
from sqlalchemy import Column, String, Integer,JSON

class ManagementUser(Base):
    __tablename__ = "management_user"
    id = Column(Integer, primary_key = True)
    uid = Column(String(64), nullable=False, unique= True, default = getApiKey(16))
    username = Column(String(32), index = True, nullable = False, unique = True)
    password_hash = Column(String(128))
    email = Column(String(100), nullable = False, unique =  True)
    apikey = Column(String(64), unique = True, default = getApiKey(32))

    def create(self):
        session.add(self)
        session.commit()
        uid = self.uid
        return uid
        
    @staticmethod
    def update(uid, attribute_name, value):
        if not uid:
            raise UserDetailsNotProvided("Uid needed for patch.")

        if not attribute_name:
            raise UserDetailsNotProvided("Atlease one attribute name is needed for patching.")

        if attribute_name == "uid":
            raise InvalidUpdate("Uid cannot be modified.")

        if attribute_name == "username" and value is None:        
            raise InvalidUpdate("Usename cannot be none.")
        
        if attribute_name == "email" and value is None:
            raise InvalidUpdate("Email cannot be none.")

        user = ManagementUser.get("single", uid)
        setattr(user, attribute_name, value)
        session.commit()


    @staticmethod
    def get(get_type = "all", uid = None):
        if get_type == "single":
            if uid:
                pass
            else:
                raise UserDetailsNotProvided("Uid needed for quering user data.")
        
            user = session.query(ManagementUser).filter(ManagementUser.uid == uid).first()
            return user
        else:
            return session.query(ManagementUser).all()

    @staticmethod
    def delete(uid):
        user = ManagementUser.get("single",uid)
        session.delete(user)
        session.commit()
    
    @staticmethod
    def exists(username, apikey):
        user = session.query(ManagementUser).filter(ManagementUser.username == username, ManagementUser.apikey == apikey).first()
        if user:
            return True
        return False
    
    @staticmethod
    def login(username, password):
        print(f"Authorizing: {username}, {password}")
        user = session.query(ManagementUser).filter(ManagementUser.username == username, ManagementUser.password_hash ==password).first()
        if user:
            return {"username":user.username, "apiKey" : user.apikey}
        return None


class ServiceUser(Base):
    __tablename__ = "service_user"
    id = Column(Integer, primary_key = True)
    uid = Column(String(64), nullable=False, unique= True, default = getApiKey(16))
    username = Column(String(32), index = True, nullable = False, unique = True)
    password_hash = Column(String(128))
    email = Column(String(100), nullable = False, unique =  True)
    apikey = Column(String(64), unique = True, default = getApiKey(32))

    def create(self):
        session.add(self)
        session.commit()
        uid = self.uid
        return uid
        
    @staticmethod
    def update(uid, attribute_name, value):
        if not uid:
            raise UserDetailsNotProvided("Uid needed for patch.")

        if not attribute_name:
            raise UserDetailsNotProvided("Atlease one attribute name is needed for patching.")

        if attribute_name == "uid":
            raise InvalidUpdate("Uid cannot be modified.")

        if attribute_name == "username" and value is None:        
            raise InvalidUpdate("Usename cannot be none.")
        
        if attribute_name == "email" and value is None:
            raise InvalidUpdate("Email cannot be none.")

        user = ManagementUser.get("single", uid)
        setattr(user, attribute_name, value)
        session.commit()


    @staticmethod
    def get(get_type = "all", uid = None):
        if get_type == "single":
            if uid:
                pass
            else:
                raise UserDetailsNotProvided("Uid needed for quering user data.")
        
            user = session.query(ServiceUser).filter(ServiceUser.uid == uid).first()
            return user
        else:
            return session.query(ServiceUser).all()

    @staticmethod
    def delete(uid):
        user = ServiceUser.get("single",uid)
        session.delete(user)
        session.commit()
    
    @staticmethod
    def exists(username, apikey):
        user = session.query(ServiceUser).filter(ServiceUser.username == username, ServiceUser.apikey == apikey).first()
        if user:
            return True
        return False
    
    @staticmethod
    def login(username, password):
        print(f"Authorizing: {username}, {password}")
        user = session.query(ServiceUser).filter(ServiceUser.username == username, ServiceUser.password_hash ==password).first()
        if user:
            return {"username":user.username, "apiKey" : user.apikey}
        return None