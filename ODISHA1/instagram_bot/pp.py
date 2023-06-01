"""
    instabot example
    Workflow:
        Download media photos with hashtag.
"""

import argparse
import os
import sys
import time
import cv2 as cv

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402

parser = argparse.ArgumentParser(add_help=True)


ig_username=["a_o_x_o","isuckmemes2","dop_cusat","kyloren.x"]
    
hashtag="aloshin"

bot = Bot(max_likes_to_like=0,
        max_followers_to_follow=10000,
        min_followers_to_follow=0,
        max_following_to_follow=10000,
        min_following_to_follow=0,
        max_followers_to_following_ratio=10,
        max_following_to_followers_ratio=1,
        min_media_count_to_follow=1,
        stop_words=['shop', 'store', 'free'])
bot.login(username="eagle_eye_odisha", password="angelogay")

#follow them
name=[]
for ig_name_indi in ig_username:
    print(ig_name_indi)
    name.append(bot.get_user_id_from_username(ig_name_indi))





change_const=len(ig_username)
while(True):

    
    change_const1=len(ig_username)
    if(change_const==change_const1):
        
        medias = bot.get_hashtag_medias(hashtag)
        users=bot.get_hashtag_users(hashtag)
        bot.send_message("Hey there "+ig_username[len(name)-1]+"! , We are from SAPLY glad to see you signed up for planting a sapling and securing future, you will be getting constant updates here and please use #SAPLING_ODISHA for submitting status of you sapling ",ig_username[len(name)-1])
        bot.follow_users(name)
        namess=[]
        for a in users:
            namess.append(bot.get_username_from_user_id(a))
            
        print(namess)
        
            
        