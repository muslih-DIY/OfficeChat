from passlib.context import CryptContext
from modules.Session.AuthManager  import (
    LoginManager,
    SessionTokenDB,Tokendb,
    UserInDB,User,Token)


class Manager(LoginManager):

    def get_userdb(self, user_id: str) -> UserInDB:
        user = fake_users_db.get(user_id)
        if not user:
            return False
        return UserInDB(**user)
    def get_user(self, user_id: str) -> UserInDB:
        user = self.get_userdb(user_id)
        return User(**user.dict())
    
    def save_session(self,session: SessionTokenDB):
        fake_session_db.update({session.session:session.dict()})

    def save_token(self,token: Tokendb):
        fake_token_db.update({token.access_token:token.dict()})        


    def get_session(self,user:str):
        'return cooies details against a user'
        for session in fake_session_db:
            if session.get('username') == user:
                return SessionTokenDB(**session)
        return None

    def get_token(self,username:str):
        'return token against the user'
        for token in fake_token_db:
            if token.get('username') == username:
                return Tokendb(**token)
        return None

    def get_token_against_session(self,session:str):
        'return token against a cookie' 
        for t,token in fake_token_db.items():
            if token.get('session') == session:
                return Tokendb(**token)
        return None
    

    def invalidate_cookie(self,cookies:str):
        """
        remove cookie from storage and invalidate a session
        remove all the token against the cookies

        """

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_session_db = {
    "session-key":{
        "session":"session-key",
        "user":"johndoe",
        "expiry":"123545673",
        "type":"3" # cookies session
    }
}
fake_token_db = {
    "token":{
        "token":"token",
        "username":"johndoe",
        "expiry":"123545673",
        "session":"token_generated_session"
    }
}

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password":pwd_context.hash('johndoe'),
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password":pwd_context.hash('alice'),
        "disabled": True,
    },
}




