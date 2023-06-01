from twilio.rest import Client 
 
def sendMsg(msg,num):
    account_sid = 'ACbc71c51358e699c3f6e1baaa8d9bfbab' 
    auth_token = 'e65ac9d8944cddca8efb7fb84a91e38d' 
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create(  
                                messaging_service_sid='MG9935442b832e928a3170edae0f3aa8b6', 
                                body=f'{msg}',      
                                to=f'+91{num}' 
                            ) 
    print(msg,f'+91{num}')
    print(message.sid)