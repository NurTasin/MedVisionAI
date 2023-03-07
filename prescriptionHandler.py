import pytesseract
from PIL import  Image, ImageEnhance
import requests as req
from urllib.parse import quote
from logger import LOG

# pytesseract.pytesseract.tesseract_cmd ="C:\\Program Files\\Tesseract-OCR\\tesseract"
pytesseract.pytesseract.tesseract_cmd ="/usr/bin/tesseract"




def getText(imagePath:str):
    img = Image.open(imagePath)
    # Increase the brightness
    enhancer = ImageEnhance.Brightness(img)
    bright_img = enhancer.enhance(1.5) # increase brightness by a factor of 1.5
    # Increase the contrast
    enhancer = ImageEnhance.Contrast(bright_img)
    final_img = enhancer.enhance(1.5) # increase contrast by a factor of 1.5
    final_img.save("img.jpg")
    txt=pytesseract.image_to_string(Image.open("img.jpg"),lang="eng+ben")
    LOG(txt)
    return txt

def in2in(arr1,string:str):
    for i in arr1:
        if i.lower() in string.lower():
            return True,string.lower().find(i.lower())
    return False,-1

def getMedicines(text:str):
    medicines=[]
    text_arr=text.split("\n")
    for i in text_arr:
        isMed=in2in(["CAP.","TAB.","SYR."],i)
        if isMed[0]:
            medicines.append(i[isMed[1]+4::])
    return medicines

def getMedicineDetails(name):
    res=req.get("https://api.arogga.com/v1/medicines/",params={
        "search":name
    })
    LOG(res.url)
    if res.json()["status"]=="success":
        return res.json()["data"][0]
    else:
        return {}

def getAllMedicineDetails(medlist):
    res=[]
    for med in medlist:
        res.append(getMedicineDetails(med))
    return res

if __name__=="__main__":
    print(getText("./uploads/e-5b8.jpg"))
