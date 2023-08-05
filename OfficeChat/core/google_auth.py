from fastapi import APIRouter,Request,Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth,OAuthError
from starlette.config import Config
from depends.database import  get_db_Session
from core.user import create_user,get_user_with_email_id
from core.config  import GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET


conf = Config(environ={'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET})
oauth = OAuth(conf)

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

router = APIRouter()



@router.get('/googleSignIn')
async def google_sign_in(
    request:Request
    ):
    user_id = request.session.get('id')
    authtype = request.session.get('auth')
    if authtype and authtype=='google' and user_id :
        return RedirectResponse('/',status_code=302)
    
    redirect_uri = request.url_for('authg')  # This creates the url for the /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/authg')
async def authg(
    request:Request,
    dbsession = Depends(get_db_Session),
    ):

    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:

        return RedirectResponse(url='/login')

    user_info = access_token['userinfo']

    email = user_info['email']
    if not email:
        return RedirectResponse('/login',status_code=302)
    
    user = get_user_with_email_id(dbsession,email)
    # create user if not available in the database using google mail as username and email
    # if available get the details 
    # set name,id,authentication_type in the session
    if not user:
       user = create_user(
            dbsession,email,user_info['name'],'',email,user_info['picture']
        )
    request.session['id']=user.id
    request.session['auth']='google'

    return RedirectResponse('/',status_code=302)


    


