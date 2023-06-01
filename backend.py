from fastapi import FastAPI,Form,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import starlette.status as status
import database
from typing import Union
import message
app = FastAPI()

app.mount("/static", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="ODISHA1")


global id 
id=0
global flag
flag = 0




@app.get("/", response_class=HTMLResponse)
async def home(request : Request):
    global flag
    flag = 0
    print(id)
    return templates.TemplateResponse("index.html",{"request" : request,"id" : id})


@app.get("/saplingLocation",response_class=HTMLResponse)
async def reg(request :Request):
    print(flag)
    return templates.TemplateResponse("page1.html",{"request": request,"flag" : flag})


@app.get("/userStats")
async def user_stats(request : Request):
    
    q1 = f'select phone from state'
    r1 = database.getDataValue(q1).fetchall()
    print("phone",r1[0][0])
    
    query = f'select point,free_sap,phone,name from user where phone = "{r1[0][0]}"'
    data = database.getDataValue(query).fetchall()  
    print(data)
    return templates.TemplateResponse("page2.html",{"request" : request,"data" : data})


@app.get("/userManual/")
def getManual(request : Request,pws: Union[int,None] = None):
    return templates.TemplateResponse("page3.html",{"request" : request,"pws" : pws})



@app.get("/userScoreBoard")
def getUserScoreBoard(request : Request):
    query = f'select name,point from user where institute = 0 order by point desc'
    a = database.getDataValue(query).fetchall()
    print(a)
    if len(a)>9 and a[0][1]!=0:
        b=10
        per=0
    elif len(a)<10 and a[0][1]!=0:
        b=len(a)
        per=0
    else:
        b=len(a)
        per=1
    return templates.TemplateResponse("page4.html",{"request" : request,"data" : a,"len" : b,"per" : per})

@app.get("/institutionScoreBoard")
def getInstitutionScoreBoard(request : Request) :
    query = f'select name,point from user  where institute = 1 order by point desc'
    a = database.getDataValue(query).fetchall()
    print(a)
    
    if len(a)>9 and a[0][1]!=0:
        b=10
        per=0
    elif len(a)<10 and a[0][1]!=0:
        b=len(a)
        per=0
    else:
        b=len(a)
        per=1
    return templates.TemplateResponse("page5.html",{"request" : request,"data" : a,"len" : b,"per" : per})
   

@app.post("/postUserData")
async def get_userData(name: str = Form(...),email: str = Form(...),phone: str = Form(...),address: str = Form(...),insta: str = Form(...)):
    query = f'insert into user(name,email,phone,insta) values("{name}","{email}","{phone}","{insta}")'
    print(query)
    res =  database.inputData(query)
    # print(type(res))
    if res == None :
        response = RedirectResponse("/saplingLocation",status_code=302)
        print( {"username": name,"email" : email, "phonenumber":phone,"address" : address,"insta" : insta})
        global id
        print(id)
        id =0
        return response
    else :
        id = -1
        response = RedirectResponse(f"/#form5-e",status_code=302)
        return response



@app.post("/postSaplingLocation")
async def get_userData(address: str = Form(...),phone: str = Form(...)):
    query1 = f'insert into sapling(sap_loc,phone) values("{address}","{phone}")'
    query2 = f'select phone from user where phone = "{phone}" '
    print(query1)
    print(query2)
    res2 = database.getData(query2)
    # res1 =  database.inputData(query1)
    print(res2)
    if res2 > 0 :
        res1 =  database.inputData(query1)
        response = RedirectResponse(f"/userStats",status_code=302)
        print( {"phone" : phone, "address" : address})
        
        q1 = f'update state set phone = "{phone}" where id = "1"'
        print(q1)
        database.inputData(q1)
        return response
    else :
        global flag
        flag = -1
        response = RedirectResponse(f"/saplingLocation",status_code=302)
        return response
 
@app.post("/postSapRequest")
async def getSapRequset(saplingNumber : int = Form(...),phone : str = Form(...)):
    print(int(saplingNumber))
    query = f'update user set req_sap = "{saplingNumber}" where phone ="{phone}" '
    print(query)
    res = database.inputData(query)

    return RedirectResponse(f"/userStats",status_code=302)


@app.post("/postPWS")
async def get_pwsData(phone: str = Form(...)):
    
    query2 = f'select phone from user where phone = "{phone}" '
    
    print(query2)
    res2 = database.getData(query2)
    
    print(res2)
    if res2 > 0 :
        pws = 0
        response = RedirectResponse(f"/userManual/?pws={pws}",status_code=302)
        message.sendMsg("Hello! This message is from EagleEye to inform you that your request for PWS is initiated",int(phone))
        return response
    else :
        pws = -1
        response = RedirectResponse(f"/userManual/?pws={pws}",status_code=302)
        return response