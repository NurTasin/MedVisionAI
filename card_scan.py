from flask import Flask,request
from flask_cors import CORS,cross_origin


app=Flask(__name__)
app_cors=CORS(app)

user_dict={
    "41633126":"Tasin",
    "2d751ed3":"Neon",
    "3d9c29d3":"Angkon"
}

@app.route("/card",methods=["POST"])
@cross_origin()
def HandleCards():
    card_uid=request.form.get("card_uid")
    if card_uid in user_dict:
        print(f"Welcome {user_dict[card_uid]}")
    else:
        print(f"Unallocated User with UID={card_uid}")
    return "OK"

if __name__=="__main__":
    app.run("0.0.0.0",8080,True)