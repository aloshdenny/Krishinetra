from twilio.rest import Client 
 
account_sid = 'ACfb6fac470000fc9d3470b4b7a60f7097' 
auth_token = '2e932bca2e61a577a1026d683d12759b' 
client = Client(account_sid, auth_token) 
 
num_list = ['']

for i in num_list:

    message = client.messages.create(  
                              messaging_service_sid='MG5ff4754c295f9c1e1f128684c9dc78ab', 
                              body= 'You have requested booking for PWS.'
                          ) 
 
    print(message.sid)