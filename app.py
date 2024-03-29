#IMPORTING ACCOUNT CREATION-SIGNIN RELATED FUNCTIONS
from function import checkvalidity,checkpinandbalancevalidity,createaccount,login
#IMPORTING FUNCTIONS FOR GETTING SPECIFIC USER DETAILS
from function import getspecificuserdetails,updatesentlist
#IMPORTING PAYMENT FUNCTION
from function import makepayment
from supabase import create_client
supabase=create_client("https://pfqzttjlsddtblhlkdmn.supabase.co","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBmcXp0dGpsc2RkdGJsaGxrZG1uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTEyMDMzNDksImV4cCI6MjAyNjc3OTM0OX0.JW0IMN0bdMjHHqsrrBl_dvuOv0en1YkKLp6wwdqgbIQ")

# username=''
# sentlist=[]
# global tempdata,pin

from flask import Flask,render_template,request,jsonify,session
app=Flask(__name__)
app.secret_key = 'HardikSharma3345'
app.config['SESSION_TYPE'] = 'redis' 
# FLAG VALUES FOR SIGNUP:
# 0 FOR SIGNUP FORM RENDER
# 1 FOR USERNAME ERROR
# 2 FOR EMAIL ERROR
# 3 FOR PASSING USERNAME AND EMAIL VALIDITY
# 69 FOR PIN ERROR
# 29 FOR PASSING VALDITY AND ACCOUNT CREATION
@app.route("/",methods=['GET','POST'])
def signup():
    flag=0
    if request.method=='POST':
        data=request.form
        if(data['flag']=='signuprequest'):

            session['tempdata']=data #STORING TEMPDATA IN SESSION

            flag=checkvalidity(data)
        elif(data['flag']=='createpinrequest'):
            pin=(data['pin'])
            cpin=(data['confirmpin'])
            bal=(data['bal'])
            jhanda=checkpinandbalancevalidity(pin,cpin,bal)
            if(jhanda=='Valid'):
                bal=int(data['bal'])
                session['pin']=cpin #STORING PIN IN SESSION
                cpin=session.get['pin'] 
                createaccount(tempdata,cpin,bal)

                #RELOADING TEMPDATA WITH SESSION FOR PASSING INITIALLY ENETERED USERNAME
                tempdata=session.get('tempdata')
                tempdata=getspecificuserdetails(tempdata['username'])
                session['username']=tempdata['username']
                session['tempdaata']=tempdata
                flag=29
                return render_template('signup.html',flag=flag,data=tempdata)
            else:
                flag=69
        elif(data['flag']=='signoutrequest'):
            session.pop('tempdata')
            session.pop('pin')
            session.pop('username')
            session.pop('sentlist')

    return render_template('signup.html',flag=flag)

# FLAGS FOR SIGN IN
# 0 TO VIEW SIGNIN FORM
# 1 USER DOESNT EXIST
# 2 PIN ERROR
# 3 LOGIN CONFIRMED
@app.route('/signin',methods=['GET','POST'])
def signin():
    flag=0
    if request.method=='POST':
        data=request.form
        if(data['flag']=='signinrequest'):
            flag=login(data)
            if(flag==3):
                tempdata=getspecificuserdetails(data['username'])
                session['username']=tempdata['username']
                session['tempdata']=tempdata
                if(tempdata['sentlist']):
                    session['sentlist']=eval(tempdata['sentlist'])
    
    return render_template('signin.html',flag=flag)

@app.route("/home",methods=['GET','POST'])
def home():
    username=session.get('username')
    sentlist=session.get('sentlist')
    tempdata=session.get('tempdata')
    flag=0#FOR INDIVIDUAL ERRORS
    megaflag=0#FOR ERROR DIV
    if request.method=='POST':
        data=request.form
        if(data['flag']=='viewhome'):
            pass
        elif(data['flag']=='payrequest'):
            sendto=data['username']
            amount=int(data['amount'])
            pin=data['pin']
            flag=makepayment(sendto,amount,pin,username)
            if(flag!=5):
                megaflag=1
            else:
                if(sendto in sentlist):
                    pass
                else:
                    sentlist.append(sendto)
                    updatesentlist(sentlist,username)
            tempdata=getspecificuserdetails(username)

    return render_template('index.html',data=tempdata,flag=flag,megaflag=megaflag,sentlist=sentlist)


if __name__=="__main__":
    app.run(debug=True)
