from fastapi import APIRouter,Request,Depends
from fastapi.responses import HTMLResponse
from markdown import markdown
from core import config
from core.auth import get_user_from_session

templates = config.templates
router = APIRouter()

@router.get("/documents/",tags=["index"])
def docsindex(
   request:Request,
   user=Depends(get_user_from_session)
   ):
   try:
      with open(config.DOCS / 'index.md') as mdfile:
         docs_string = mdfile.read()
         html = markdown(docs_string)  
      context = {'request':request,'docs':html,'title':'home'}           
      return templates.TemplateResponse('base/docs_base.html',context)
   except:
      return page404(request)


@router.get("/documents/{docfile}",response_class=HTMLResponse)
async def docs(
   request:Request,
   docfile:str='index',
   user=Depends(get_user_from_session)
   ):
   try:
       
      with open(config.DOCS / f"{docfile}.md") as mdfile:
         docs_string = mdfile.read()
         html = markdown(docs_string)
      context = {'request':request,'docs':html,'title':'home'}              
      return templates.TemplateResponse('base/docs_base.html',context)
   except:
      return page404(request)


def page404(request:Request):
   html = """
   <div id="main">
    	<div class="fof">
        		<h1>Error 404</h1>
    	</div>
   </div>
   """
   context = {'request':request,'docs':html,'title':'404'}           
   return templates.TemplateResponse('base/docs_base.html',context,status_code=404)
