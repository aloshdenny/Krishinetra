# KRISHINETRA

<p align=center><img src="icon.png" width=20% height=20%></p>

A website for Forest Department of India to tracking all individual sapling by taking benefit Social Media 

### Working Screenshots

| <img src="soildemo.gif">             | <img src="plantdemo.gif">              |  <img src="pictures/leaderboarddemo.gif">                                      |
| :----------------------------------: | :------------------------------------: | :----------------------------------------------------------------------------: |
|          _Crop prediction_           |      _Plant health Detection_          |                                 _Web Application_                              |

### Problem Statement

In India, people show interest in planting saplings, but most of them are left unattended and either grow out or wither away.
This calls for a unified system intended to distribute saplings to the people and track their status. 

### Research

<p align=left><img src="pictures/table1.jpg" width=60% height=60%></p>
<p align=left><img src="pictures/table2.jpg" width=60% height=60%></p>


### Conclusion
Sapling survival rates in India are low because:

1.People lose interest in taking care of sapling</br>

2.Individual level monitoring is difficult</br>

3.Variable Climatic conditions and soil profile</br>

     AIM :Right Person Right Place
     

### Key Features 



1. Documented log of users and saplings distributed using Instagram</br>
2. Crop prediction using location and image</br>
3. Weekly and monthly user reports via Instagram stories/post</br>
4. Disease and growth detection using ML</br>
5. Social credit system to boost engagement</br>
6. POI algorithm minimizes loss of saplings</br>
7. Validation via Captcha</br>

### ML Prebuild Models used

CROP PREDICTION ML MODEL (Random Forest Algorithm) - https://github.com/Phantom-Studiosad/Intelligent_CropPrediction_System

PLANT DISEASE DETECTION (CNN) - https://github.com/manthan89-py/Plant-Disease-Detection.git


### Setup

##How to use the software

1.Installing on libraries

      pip install -r requirements.txt
2.Running the website

    uvicorn backend:app --reload
3.Running the instagram Bot server

    python -u "instagram_bot\Instagram_checker.py"
    


