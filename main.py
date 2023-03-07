from flask import Flask,jsonify,request,render_template,redirect,url_for,make_response
from flask_cors import CORS, cross_origin
from dbms import DBMS
from logger import *
from os import path
import uuid
from prescriptionHandler import getMedicines,getText,getAllMedicineDetails
import json
import time
import threading
# import serialIO
from lcdinterface import LCD



LCD_IP="192.168.24.96"
Display=LCD(LCD_IP)
UPLOAD_FOLDER = path.abspath('./uploads')

app=Flask(__name__)
app_cors=CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

user_db=DBMS("./db/users.json")


def DisplayToLCD(string1,string2):
    delay=(len(string2)+32)*0.55
    Display.scrollFormatted(string1,False,string2,True)
    time.sleep(delay)
    Display.scrollFormatted("   MedVisionAI  ",False,"Artificial Intelligence Based Medicine Vending Machine With OCR",True)




@app.route("/",methods=["GET"])
@cross_origin()
def landingPage():
    userdata=user_db.read()
    try:
        if request.cookies.get("usr") in userdata: 
            return render_template("index.html",data=userdata[request.cookies.get("usr")])
        else:
            return redirect(url_for("loginPageHandler"))
    except Exception as e:
        ERROR(e)
        return redirect(url_for("loginFormHandler"))


@app.route("/login",methods=["GET","POST"])
@cross_origin()
def loginPageHandler():
    if request.method=="GET":
        return render_template("login.html",msg="Login Here")
    else:
        uname="USR_"+request.form.get("username")
        pw=request.form.get("passw")
        userdata=user_db.read()
        if uname in userdata:
            if pw==userdata[uname]["pw"]:
                res=make_response(redirect(url_for("landingPage")))
                res.set_cookie("usr",uname)
                return res
            else:
                return render_template("login.html",msg="Wrong Username or Password")
        else:
            return render_template("login.html",msg="Wrong Username or Password")

@app.route("/logout",methods=["GET"])
@cross_origin()
def logoutPageHandler():
    res=make_response(redirect(url_for("loginPageHandler")))
    res.delete_cookie("usr")
    return res

@app.route('/medicine_list', methods = ['GET', 'POST'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
      f = request.files['prescription']
      file_path=path.join(app.config["UPLOAD_FOLDER"],str(uuid.uuid4())[0::8]+"."+f.filename.split(".")[-1])
      f.save(file_path)
      INFO(f"New image uploaded. path: {file_path}")
      INFO(f"Running OCR on {file_path}")
      pres_text=getText(file_path)
      medicines=getMedicines(pres_text)
      INFO(f"Found {len(medicines)} medicines in {file_path}")
      INFO(f"Searching for details in Arogga API")
      medDetails=getAllMedicineDetails(medicines)
      INFO("Rendering and serving template")
      return render_template("medicine_details.html",details_group=medDetails)
    else:
        return redirect(url_for("landingPage"))
        
@app.route("/confirm_order",methods=["GET","POST"])
@cross_origin()
def ConfirmOrder():
    if request.method=="POST":
        medicines=json.loads(request.form.get("names"))
        cost=float(request.form.get("cost"))
        userid=str(request.form.get("usrid"))

        userdata=user_db.read()
        if userdata[userid]["token"] >= cost:
            userdata[userid]["token"]=float("%.2lf"%(userdata[userid]["token"]-cost))
            user_db.write(userdata)
            #Do the hardwear magic!!
            # serialIO.dropMed(medicines)
            otherThread=threading.Thread(target=DisplayToLCD,args=("Purchased Items:",", ".join(medicines)))
            otherThread.start()
            LOG(f"User `{userdata[userid]['name']}` bought {medicines} in exchange of {cost}. New Baalance: {userdata[userid]['token']}")
            return render_template("thanks.html",details={
                "username":userdata[userid]['name'],
                'new_bal':userdata[userid]['token'],
                "cost":cost
            })
        else:
            return "Insufficient Ballance"


@app.route("/buy_from_machine",methods=["GET"])
@cross_origin()
def SelectFromMachine():
    return render_template("medicine_details.html",details_group=getAllMedicineDetails(["ace xr","maxpro 20","amodis 40","ciprocin 500","alatrol 10"]))

@app.route("/call_doc")
@cross_origin()
def callDoc():
    return render_template("doctor_call.html")
@app.route("/usr/<usrid>",methods=["GET","POST"])
@cross_origin()
def getUserDetails(usrid):
    usrid="USR_"+usrid
    if request.method=="GET":
        data=user_db.read()
        if usrid in data:
            return render_template("user.html",usr=data[usrid])
        else:
            return jsonify({"msg":"User not found!"}),404
    else:
        return jsonify({"msg":"For Security reasons we don't allow tresspassing"}),403

@app.route("/servon",methods=["GET"])
@cross_origin()
def servoOn():
    print("Servo Open")
    return "OK",200

@app.route("/servoff",methods=["GET"])
@cross_origin()
def servoOff():
    print("Servo Closed")
    return "OK",200

@app.route("/mask",methods=["GET"])
@cross_origin()
def ServeMaskDetector():
    return render_template("mask.html")


server_frontend_sync_pack={
    "username":"",
    "balance":"",
    "avatar":"",
    "pw":"",
    "code":200,
    "changed":True
}

data_changed=False
@app.route("/card",methods=["POST"])
@cross_origin()
def handleCardScans():
    global data_changed
    card_uid=request.form.get("card_uid")
    server_frontend_sync_pack["code"]=400
    server_frontend_sync_pack["username"]=""
    server_frontend_sync_pack["balance"]=""
    server_frontend_sync_pack["avatar"]=""
    server_frontend_sync_pack["pw"]=""
    current_data=user_db.read()
    for id in current_data.keys():
        if current_data[id]["card_uid"]==card_uid:
            server_frontend_sync_pack["username"]=current_data[id]["name"]
            server_frontend_sync_pack["balance"]=current_data[id]["token"]
            server_frontend_sync_pack["avatar"]=url_for("static",filename=current_data[id]["avatar"])
            server_frontend_sync_pack["pw"]=current_data[id]["pw"]
            server_frontend_sync_pack["code"]=200
            data_changed=True
    
    return "OK"

@app.route("/syncfrontend",methods=["GET"])
@cross_origin()
def syncFronted():
    global data_changed
    if data_changed:
        data_changed=False
        return jsonify(server_frontend_sync_pack)
    else:
        return jsonify({"changed":False})

@app.route("/frontend")
@cross_origin()
def serveFrontend():
    return render_template("frontend.html")

if __name__=="__main__":
    app.run("0.0.0.0",80)