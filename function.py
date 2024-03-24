from supabase import create_client
import re
import random,string
supabase=create_client("https://pfqzttjlsddtblhlkdmn.supabase.co","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBmcXp0dGpsc2RkdGJsaGxrZG1uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTEyMDMzNDksImV4cCI6MjAyNjc3OTM0OX0.JW0IMN0bdMjHHqsrrBl_dvuOv0en1YkKLp6wwdqgbIQ")

def checkvalidity(data):
    # VALIDATING WRT TO USERNAME
    username=data['username']
    if(len(username)<3):
        return 1
    suparesponse=supabase.table('mydata').select("*").eq('username',username).execute().data
    if(len(suparesponse)!=0):
        return 1
    # VALIDATING WRT TO EMAIL
    email=data['email']
    emailpattern= r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if(re.match(emailpattern,email)):
        pass
    else:
         return 2
    suparesponse=supabase.table('mydata').select("*").eq('email',email).execute().data
    if(len(suparesponse)!=0):
        return 2
    return 3

def checkpinandbalancevalidity(pin,cpin,bal):
    charpattern=r'[a-zA-Z!@#$%^&*()_+={}\[\]:;"\'|<,>.?/~`]'
    if(re.match(charpattern,pin)):
        return 'Invalid'
    elif(re.match(charpattern,cpin)):
        return 'Invalid'
    elif(len(pin)>5 or len(cpin)>5):
        return 'Invalid'
    elif(re.match(charpattern,bal)):
        return 'Invalid'
    return 'Valid'

def createaccount(data,pin,bal):
    username=data['username']
    fname=data['firstname']
    lname=data['lastname']
    email=data['email']
    balance=int(bal)
    supabase.table('mydata').insert({"username": username,"pin": pin,"firstname": fname, "lastname": lname,"email": email,"balance":balance}).execute()

def login(data):
    username=data['username']
    email=data['email']
    pin=data['pin']
    # CHECKING WRT TO USERNAME
    suparesponse=supabase.table('mydata').select("*").eq('username',username).execute().data
    if(suparesponse):
        temp=suparesponse[0]
        if(username==temp['username'] and pin==temp['pin']):
            return 3
        elif(email==temp['email'] and pin==temp['pin']):
            return 3
        else:
            return 2
    else:
        return 1

def getspecificuserdetails(username):
    suparesponse=supabase.table('mydata').select("*").eq('username',username).execute().data
    temp=suparesponse[0]

    return temp

def makepayment(sendto,amount,pin,username):
    receiverdetails=supabase.table('mydata').select("*").eq('username',sendto).execute().data
    if(len(receiverdetails)==0):
        return 1
    else:
        receiverdetails=getspecificuserdetails(sendto)
        if(amount<=0):
            return 2
        else:
            senderdetails=getspecificuserdetails(username)
            if(pin==senderdetails['pin']):
                if(amount>senderdetails['balance']):
                    return 3
                else:
                    print('update initiated')
                    sendernewbal=senderdetails['balance']-amount
                    print(sendernewbal)
                    supabase.table('mydata').update({'balance':sendernewbal}).eq('username',username).execute()
                    receivernewbal=receiverdetails['balance']+amount
                    print(receivernewbal)
                    supabase.table('mydata').update({'balance':receivernewbal}).eq('username',sendto).execute()
                    return 5
            else:
                return 4

def updatesentlist(sentlist,username):
    sentlist=str(sentlist)
    supabase.table('mydata').update({'sentlist':sentlist}).eq('username',username).execute()
    

# data=getspecificuserdetails('aryachawan12')
# print('Initial')
# print(type(data['sentlist']))
# print(data)
# data['sentlist']=eval(data['sentlist'])
# print(type(data['sentlist']))
# print(data)