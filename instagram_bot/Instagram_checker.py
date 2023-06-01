from instagrapi import Client
import time
import os,cv2
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
import database


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



model = load_model('instagram_bot\weights.h5')

# Display progress and text
progress = st.text("Crunching Image")
my_bar = st.progress(0)
i = 0



while(True):
    li=cl.hashtag_medias_recent("eagle_eye_soh", 27)
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
                print(pk)
                
            if(con==2):
                print("id number")
                global idd
                idd=h[1].split("_")[1]
                print(idd)

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
                
                global final_username
                final_username=h[1]
                
                
                
            if(con==8):
                print("The location ")
                print(h[1])
        try:
            count=count+1
            if(os.path.exists("DATA/"+str(naaame)+"/"+str(pk)+".jpg")==False):
                response=wget.download(final_username,"DATA/"+str(naaame)+"/"+str(pk)+".jpg")
  
             
               
                
                dir_list = os.listdir("DATA")
                for i in dir_list:
                    in_list = os.listdir("DATA/"+str(i))
                    for j in in_list:
                        print(j)
                        # Reading the uploaded image
                        image = Image.open("DATA/"+i+"/"+j)
                        st.image(np.array(Image.fromarray(
                            np.array(image)).resize((700, 400), Image.ANTIALIAS)), width=None)

                        image = clean_image(image)

                        # Making the predictions
                        predictions, predictions_arr = get_prediction(model, image)

                        result = make_results(predictions, predictions_arr)



                        # Show the results
                print("---------------------------- ")
                print("---------------------------- ")
                print("USING MACHINE LEARNING MODEL ")
                print("---------------------------- ")
                print("---------------------------- ")
                print(f"The plant {result['status']} with {result['prediction']} prediction.")
                
               
                mess="Hello "+naaame+"!👋"+"\n We recently got your sapling status 🌱 "+"\n We have used ML Model 🖥️  to detect any disease in the plant and we have found out :"+"\n The plant "+str(result['status'])+" with "+str(result['prediction'])+" accuracy in prediction."
                q1 = f'update user set point = point + 15 where insta = "{naaame}"'
                print(q1)
                database.inputData(q1)
                cl.photo_upload_to_story("DATA/"+str(naaame)+"/"+str(pk)+".jpg")
                cl.direct_send(mess,[idd])
            #img=Image.open(BytesIO(requests.get(final_username).content)).convert("RGB")
            #img = img.save("DATA/"+str(naaame)+"/pic"+str(count)+".jpg")



         






            

        except:
            NameError