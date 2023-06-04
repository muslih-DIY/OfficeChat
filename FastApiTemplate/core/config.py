from FastApiTemplate.AuthManager import SCookiesDB,Tokendb, UserInDB,User
from ..AuthManager import LoginManager,UserInDB

class Manager(LoginManager):

    def get_userdb(self, user_id: str) -> UserInDB:
        user = fake_users_db.get(user_id)
        if not user:
            return False
        return UserInDB(**user)
    def get_user(self, user_id: str) -> UserInDB:
        user = self.get_userdb(user_id)
        return User(**user.dict())
    
    def save_cookies(cookies: SCookiesDB):
        fake_session_db.update(cookies.cookies,{**cookies})

    def save_token(token: Tokendb):
        fake_session_db.update(token.cookies,{**token})        


    def get_cookies(username:str):
        'return cooies details against a user'
        for cookie in fake_session_db:
            if cookie.get('username') == username:
                return SCookiesDB(**cookie)
        return None

    def get_token(username:str):
        'return token against the user'
        for token in fake_token_db:
            if token.get('username') == username:
                return Tokendb(**token)
        return None

    def get_token_against_cookie(cookies:str):
        'return token against a cookie' 
        for token in fake_token_db:
            if token.get('session') == cookies:
                return Tokendb(**token)
        return None
    

    def invalidate_cookie(cookies:str):
        """
        remove cookie from storage and invalidate a session
        remove all the token against the cookies

        """


Session_manager = Manager('auths')

fake_session_db = {
    "session-key":{
        "cookies":"session-key",
        "username":"johndoe",
        "expiry":"123545673"
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
        "hashed_password":Session_manager.pwd_context.hash('johndoe'),
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password":Session_manager.pwd_context.hash('alice'),
        "disabled": True,
    },
}






