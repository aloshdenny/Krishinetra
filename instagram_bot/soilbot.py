from instagrapi import Client
import time
import os
import wget,glob
from io import BytesIO
from PIL import Image
import requests
import streamlit as st
from PIL import Image
import io,os,csv
import pandas as pd
import streamlit as st
from PIL import Image
import io,os
import numpy as np
import tensorflow as tf
from utils import clean_image, get_prediction, make_results
import pandas as pd

cl = Client()
cl.login("Eagle_Eye_SOH", "sohhack")
count=0


def load_model(path):
    
    # Xception Model
    xception_model = tf.keras.models.Sequential([
    tf.keras.applications.xception.Xception(include_top=False, weights='imagenet', input_shape=(512, 512, 3)),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(4,activation='softmax')
    ])


    # DenseNet Model
    densenet_model = tf.keras.models.Sequential([
        tf.keras.applications.densenet.DenseNet121(include_top=False, weights='imagenet',input_shape=(512, 512, 3)),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(4,activation='softmax')
    ])

    # Ensembling the Models
    inputs = tf.keras.Input(shape=(512, 512, 3))

    xception_output = xception_model(inputs)
    densenet_output = densenet_model(inputs)

    outputs = tf.keras.layers.average([densenet_output, xception_output])


    model = tf.keras.Model(inputs=inputs, outputs=outputs)

    # Loading the Weights of Model
    model.load_weights(path)
    
    return model



def predict(img_add):                                      #defining prediction function
                  #requesting data from client
                         #reading the image received from client
    img = image.load_img(img_add)
    img = img.resize((150,150))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x/255.0
    #print('Input image shape:', x.shape)
    #my_image = imageio.imread(image_path)
    #imshow(my_image)
    #print("class prediction vector [Alluvial, Black, Clayey, Latterite, Red, Sandy] = ")
    json_file = open('Saved Model\SoilNET model.json', 'r')                 #loading the model
    loaded_model_json = json_file.read()
    #json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    prediction=(loaded_model.predict(x))*100       #predicting soil type based on SoilNET
    max_i = np.argmax(prediction) 
    if max_i==0:                                    #categorizing soil type based on highest probability obtained using SoilNET prediction
        soil="Alluvial"
    elif max_i==1:
        soil="Black"
    elif max_i==2:
        soil="Clayey"
    elif max_i==3:
        soil="Latterite"
    elif max_i==4:
        soil="Red"
    elif max_i==5:
        soil="Sandy"
        
    types = soil
    
    if types=="Alluvial":                           #Restructuring soil type to specific codes according to model input
        soil_type = 1
    elif types == "Red":
        soil_type = 2
    elif types == "Clayey":
        soil_type = 3
    elif types == "Latterite":
        soil_type = 4
    elif types == "Red":
        soil_type = 5
    elif types == "Sandy":
       soil_type = 6
    
    coordinates = "20.2376,84.2700"     #extracting location coordinates
    coordinates = str(coordinates)                  
    locator = Nominatim(user_agent="myGeocoder")    #retrieving name of the state based on coordinates
    location = locator.reverse(coordinates)
    loc_dict=location.raw
    state=(loc_dict.get('address').get('state'))
    
    state_code=0                

    if state=="Andhra Pradesh":                     #converting state name to specific code according to the model input
        state_code=1
    elif state=="Arunachal Pradesh":
        state_code=2 
    elif state=="Assam":
        state_code=3 
    elif state=="Bihar":
        state_code=4 
    elif state=="Chhatisgarh":
        state_code=5 
    elif state=="Goa":
        state_code=6 
    elif state=="Gujarat":
        state_code=7 
    elif state=="Haryana":
        state_code=8 
    elif state=="Himachal Pradesh":
        state_code=9 
    elif state=="Jharkhand":
        state_code=10
    elif state=="Karnataka":
        state_code=11 
    elif state=="Kerela":
        state_code=12
    elif state=="Madhya Pradesh":
        state_code=13
    elif state=="Maharashtra":
        state_code=14
    elif state=="Manipur":
        state_code=15
    elif state=="Meghalaya":
        state_code=16
    elif state=="Mizoram":
        state_code=17
    elif state=="Nagaland":
        state_code=18 
    elif state=="Odisha":
        state_code=19 
    elif state=="Punjab":
        state_code=20
    elif state=="Rajasthan":
        state_code=21
    elif state=="Sikkim":
        state_code=22 
    elif state=="Tamil Nadu":
        state_code=23 
    elif state=="Telangana":
        state_code=24 
    elif state=="Tripura":
        state_code=25 
    elif state=="Uttar Pradesh":
        state_code=26 
    elif state=="Uttarakhand":
        state_code=27 
    elif state=="West Bengal":
        state_code=28 
    elif state=="Andaman and Nicobar Island":
        state_code=29 
    elif state=="Dadra Nagar Haveli and Daman and Diu":
        state_code=30 
    elif state=="Chandigarh":
        state_code=31 
    elif state=="Delhi":
        state_code=32 
    elif state=="Jammu and Kashmir":
        state_code=33 
    elif state=="Lakshadweep":
        state_code=34 
    elif state=="Pudducherry":
        state_code=35 
    elif state=="Ladakh":
        state_code=36
    
    state = state_code
    
    file = pd.read_csv("Datasets/Cat_Crop.csv")                          #reading csv file into dataframe
    data_frame = file.loc[file["States"]==state, "Rainfall"]    #extracting average rainfall data according to state code
    rain = float(data_frame.unique())
    
    df = file.loc[file["States"]==state,"Ground Water"]         #extracting ground water availability according to state code
    ground_water = float(df.unique())
    
    url = "https://api.ambeedata.com/weather/latest/by-lat-lng"
    lat=coordinates.split(",")[0]
    lng=coordinates.split(",")[1]
    querystring = {"lat":str(lat),"lng":str(lng)}
    headers = {
        'x-api-key': "00ae33b916c884679a1567583fd82b16acd3a77c00b51b5d0c7c66a3823164c0",
        'Content-type': "application/json"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print("hhhhhhhhhhhhhhhhhhhh")
    tempp=response.text.split("temperature")[1]
    temp=5/9*(float((tempp.split(",")[0]).split(":")[1])-32)
    
                                  #extracting temperature from data received from the client
    #print(type(temp))
    temp = float(temp)
    
    date = "01/12/2021"                                         #extracting date from data received from the client                                    
    #print(type(date))
    date = str(date)
    month=int(date[3:5])                                        #extracting month from the data received
    print(month)
    #month=5
    season=4
    if month == 11 or month == 12 or month==1 or month==2:      #converting months to specific code according to the model input
        season=2
        
    elif month==6 or month==7 or month==8 or month==9:
        season=1
    elif month==3 or month==4:
        season=3
    else:
        season = 4
    
    
    input_dict={}                                               #creating  a dictionary of all the data extracted to be fed to the model for crop predictions
    
    input_dict["States"] = state_code
    input_dict["Rainfall"] = rain
    input_dict["Ground Water"] = ground_water
    input_dict["Temperature"] = temp
    input_dict["Soil_type"] = soil_type
    input_dict["Season"] = season
    
    output = json.dumps(input_dict)
    with open("input.json","w") as sout:
        sout.write(output)
    filename = "Saved Model\CRSML.sav"
    loaded_model = joblib.load(filename)
    
    file_path = "input.json"
    with open(file_path) as f:
      data = json.load(f)
    temp=list(data.values())
    
    
    inp_array=np.array(temp)                                    #restructing data according to model input
    inp_array=inp_array.reshape(1,-1)
    #print(inp_array)
    prediction=loaded_model.predict(inp_array)
    #print(prediction)
    prediction = list(prediction)
    print(prediction)
    pred_crop_name = prediction[0]
   
    jsonFilePath = "Datasets/Prediction.json"                            #Extracting information related to predicted crop            
    with open (jsonFilePath) as fp:
        Final_rec = json.load(fp)
    final_pred = Final_rec[pred_crop_name]
    #print(final_pred)
    
    Final_dict = {
        "Data" : final_pred
        }
    
    
    output=json.dumps(Final_dict)                               #Exporting the final JSON File back to the client
    with open("final.json","w") as sout:
        sout.write(output)
    return output



while(True):
    li=cl.hashtag_medias_recent("eagle_eye_soh1", 27)
    #print(li)
    #print(len(li))
    for j in li:
        con=0
        
        for h in j:
            #print(h)
            
            con=con+1
            if(con==1):
                print("pk number")
                global pk
                pk=h[1]
                
            if(con==2):
                print("id number")
                global idd
                idd=h[1].split("_")[1]
                #print(idd)

            if(con==9):
                con1=0
                print("The insta account")
                #print((h[1]))
                for k in h[1]:
                    con1=con1+1
                    if(con1==2):
                        print(k[1])
                        global naaame
                        naaame=k[1]
                        if(os.path.exists("DATA/"+str(k[1]))==False):
                            os.makedirs("DATA/"+str(k[1]))
            if(con==7):
                print("Image tagged ")
                print(h[1])
                global final_username
                final_username=h[1]
                
                
                
            if(con==8):
                print("The location ")
                print(h[1])
        try:
            count=count+1
            if(os.path.exists("DATA/"+str(naaame)+"/"+str(pk)+".jpg")==False):
                response=wget.download(final_username,"DATA/"+str(naaame)+"/"+str(pk)+".jpg")
                value_data = pd.read_csv('value.csv')
                status=value_data['Value'][0]
                acc=value_data['Value'][1]
                mess="The plant "+status+"with "+acc+"prediction"
                print(mess)
                dir_list = os.listdir("DATA")
                for i in dir_list:
                    in_list = os.listdir("DATA/"+str(i))
                    for j in in_list:
                        print(j)
                        # Reading the uploaded image
                        image = Image.open("DATA/"+i+"/"+j)
                        print(predict("image.jpg"))



                        # Show the results
                
                
               
                        mess=
                        cl.photo_upload_to_story("DATA/"+str(naaame)+"/"+str(pk)+".jpg")
                        cl.direct_send(mess,[idd])
            #img=Image.open(BytesIO(requests.get(final_username).content)).convert("RGB")
            #img = img.save("DATA/"+str(naaame)+"/pic"+str(count)+".jpg")



         






            

        except:
            NameError