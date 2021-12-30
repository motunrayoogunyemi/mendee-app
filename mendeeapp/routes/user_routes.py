import random,string,json,requests,os,mysql.connector
from datetime import time
from flask import render_template,request,redirect,flash,url_for,make_response,session,abort,jsonify
from werkzeug.security import generate_password_hash, check_password_hash


from mendeeapp import app,csrf,db
#from mendeeapp.myforms import 
from mendeeapp.mymodels import Customer,Craftsperson,Category,Service,Bookings,Payment,Feedback,Details1,Timedate,Transaction,Mybookings
from mendeeapp import mail,Message

# @app.route('/test')
# def test():
#     loggedin = session.get('user') 
#     if loggedin:
#         if request.method=='GET':
#             myservice_id = session['service']
#             sers = db.session.query(Service).all()
#             menders = db.session.query(Craftsperson).all()
#             deets1 = db.session.query(Details1).filter(Details1.service_id==myservice_id).first()
#             return render_template('user/getmenders.html',sers=sers,menders=menders,deets1=deets1)
#         else:
#             mymonth = request.form.get('monthbox')
#             mydate = request.form.get('datebox')
#             mytime = request.form.get('timebox') 
#             t = Timedate(customer_id=loggedin,timedate_month=mymonth,timedate_date=mydate,timedate_time=mytime)
#             db.session.add(t)
#             db.session.commit()
#             return redirect()
#     return redirect(url_for('login'))
    #return render_template('user/test.html')

@app.route('/',methods=['POST','GET'])
def home():
    # searchdata = request.form.get('text')
    # allservices = db.session.query(Service).filter(Service.service_name==searchdata).all()
    # x = jsonify(allservices)
    #if request.method=='GET':  
    return render_template('user/index.html') 
    #else:
        #searchdata = request.form.get('text')
        # db = mysql.connector.connect(host='localhost',user='root',password='',database='mendee') 
        # mycursor = db.cursor()
        # mycursor.execute('select service_name from service where service_name LIKE "{}"'.format(searchdata))
        # allservices = mycursor.fetchall()    
        #allservices = db.session.query(Service).filter(Service.service_name.like(f'%{searchdata}%')).all()
        #allservices = db.session.query(Service).filter(Service.service_name==searchdata).all()
        #return jsonify(allservices)    
        #return       

# app.route('/search',methods=['POST','GET'])
# def search():
#     searchdata = request.form.get('text')
#     allservices = db.session.query(Service).filter(Service.service_name==searchdata).all()
    #allservices = db.session.query(Service).filter(Service.service_name.like(f'%{searchdata}%')).all()
    #return jsonify(allservices)           
    #allservices = mycursor.execute("INSERT INTO users SET fullname='%s',username='%s',pwd='%s'"%(fullname,username,password))

@app.route('/live')
def live():
    searchdata = request.args.get('mytext')
    #allservices = db.session.query(Service).filter(Service.service_name==searchdata).all()
    allservices = db.session.query(Service).filter(Service.service_name.like(f'%{searchdata}%')).all()
    tosend = "<ul>"      
    for t in allservices:
        tosend = tosend + f"<li style='list-style-type: none; margin-bottom: 10px;'><a href='/eachmending/{t.id}'>{t.service_name}</a></li>" 
    tosend= tosend+"</ul>"
    return tosend
    

@app.route('/about')
def about():
    return render_template('user/about.html')

# @app.route('/services')
# def services():
#     return render_template('user/services.html')

@app.route('/services')
def services():
    cat = db.session.query(Category).all()
    sers = db.session.query(Service).all()
    # cat1 = db.session.query(Category).get(1)
    # cat2 = db.session.query(Category).get(2)
    # cat3 = db.session.query(Category).get(3) 
    #sers = db.session.query(Service).filter(Service.category_id==cat.id).all()
    #recs = db.session.query(Service,Category).filter(Service.category_id==Category.id).all()
    #servic = db.session.query(Service).filter(Service.category_id==Service.serv_category.id).all()
    # cat1.id = session['cat1']
    # cat2.id = session['cat2']
    # cat3.id = session['cat3']
    return render_template('user/services.html',cat=cat,sers=sers)


@app.route('/eachservice/<int:id>')
def eachservice(id):
    deets = db.session.query(Category).get(id)
    #session['cat'] = deets.id
    serv = db.session.query(Service).limit(5).all()
    mys = db.session.query(Service).filter(Service.category_id==id).all()
    return render_template('user/eachservice.html', deets=deets, mys=mys,serv=serv)
    # deets = db.session.query(Service).get(id)
    # return render_template('user/eachservice.html', deets=deets)   

@app.route('/eachmending/<int:id>')
def eachmending(id):
    #records = db.session.query(Service).filter(Service.category_id==id).all()
    records = db.session.query(Service).get(id)
    session['service'] = records.id
    return render_template('user/eachmending.html', records=records)

@app.route('/bookings',methods=['GET','POST'])
def bookings():
    loggedin = session.get('user')
    if loggedin:
        if request.method=='GET':
            return render_template('user/bookings.html')
        else:
            mylocation = request.form.get('location')
            mytime = request.form.get('time')
            myservice = request.form.get('service')
            mydetails = request.form.get('details')
            myservice_id = session['service']
            if mylocation=='' or myservice=='' or mydetails=='':
                flash('All fields are required')
                return redirect(url_for('bookings'))
            else:
                d1 = Details1(customer_id=loggedin,details1_location=mylocation,details1_time=mytime,details1_service=myservice,details1_details=mydetails,service_id=myservice_id)
                db.session.add(d1)
                db.session.commit()
                bookings = Mybookings(customer_id=loggedin,service_id=myservice_id,bdetails1_service=myservice,bdetails1_location=mylocation)
                db.session.add(bookings)
                db.session.commit()
                session['book']=bookings.bid
                session['details1']= d1.details1_id

                # fkserv = db.session.query(Details1).get(loggedin)
                # fkserv.customer_id = loggedin 
                # db.session.commit()
                return redirect('/bookings/getmenders')
                #return redirect(url_for('getmenders(id)'))
                #return render_template('user/getmenders.html')
    else:
        return redirect(url_for('login'))

@app.route('/bookings/getmenders',methods=['GET','POST'])
def getmenders():
    loggedin = session.get('user')
    if loggedin:
        if request.method=='GET':
            myservice_id = session['service']
            sers = db.session.query(Service).all()
            menders = db.session.query(Craftsperson).all() 
            #menders = db.session.query(Craftsperson).get(id)
            deets1 = db.session.query(Details1).filter(Details1.service_id==myservice_id).first()
            return render_template('user/getmenders.html',sers=sers,menders=menders,deets1=deets1)
        else: 
            #actual = db.session.query(Craftsperson).all()
           # menders = db.session.query(Craftsperson).get(actual.id)
            mymonth = request.form.get('monthbox')
            mydate = request.form.get('datebox')
            mytime = request.form.get('timebox')
            mymenderid = request.form.get('menderid')
            if mymonth=='' or mydate=='' or mytime=='':
                flash('All fields are required')
                return redirect(url_for('getmenders'))
            else:
                t = Timedate(customer_id=loggedin,timedate_month=mymonth,timedate_date=mydate,timedate_time=mytime)
                db.session.add(t)      
                db.session.commit()     
                #bookings = Mybookings(customer_id=loggedin,service_id=myservice_id,bdetails1_service=myservice,bdetails1_location=mylocation)
                bookingid = session['book'] 
                b = db.session.query(Mybookings).get(bookingid)
                b.btimedate_month=mymonth
                b.btimedate_date=mydate
                b.btimedate_time=mytime
                b.craftsp_id=mymenderid
                db.session.commit()   
                session['timedate']=t.timedate_id
                session['craftsp']=b.craftsp_id
                return redirect('/bookings/confirmation')
    return redirect(url_for('login'))

def refno(): 
    sample_xters = random.sample(string.digits,10)
    newname = ''.join(sample_xters)
    return newname

@app.route('/bookings/confirmation',methods=['GET','POST'])
def confirmation():
    loggedin = session.get('user')
    bookingid = session['book']
    if loggedin:
        if request.method == 'GET':
            myservice_id = session['service']
            sers = db.session.query(Service).all()
            menders = db.session.query(Craftsperson).all()
            deets1 = db.session.query(Details1).filter(Details1.service_id==myservice_id).first()
            timedeets = db.session.query(Timedate).get(loggedin)
            data = db.session.query(Customer).get(loggedin)
            bookingstbl = db.session.query(Mybookings).filter(Mybookings.bid==bookingid).first()
            return render_template('user/confirmation.html',timedeets=timedeets,deets1=deets1,menders=menders,data=data,bookingstbl=bookingstbl)
        else:
            #retrieve form data
            amount = request.form.get('amount',0)   
            ref = refno()
            session['trxref'] = ref
            tran = Transaction(trx_custid=loggedin,trx_amt=amount,trx_status='pending',trx_ref=ref)
            db.session.add(tran)
            db.session.commit()
            bookingid = session['book']
            b = db.session.query(Mybookings).get(bookingid)
            b.btrx_ref = ref
            db.session.commit()
            #return 'next route'
            return redirect(url_for("paymentconfirmation"))
    else:
        return redirect(url_for('login'))

@app.route('/bookings/paymentconfirmation',methods=['GET','POST'])
def paymentconfirmation():
    if session.get('user') !=None and session.get('trxref') !=None:
        ref = session.get('trxref')
        deets = db.session.query(Transaction).filter(Transaction.trx_ref==ref).first()

        if request.method=='GET':
            return render_template('user/paymentconfirmation.html',deets=deets)  
        else:
            #connect to paystack endpoint
            amount = deets.trx_amt * 100
            email=deets.customer.cust_email
            headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_fa3151af8a36aea0eb83b7a1a83bb6e348f056ce"}            
            data = {"reference": ref, "amount": amount, "email": email}
            
            response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, data=json.dumps(data))

            rsp = json.loads(response.text) 	
            if rsp.get('status') == True:
                payurl = rsp['data']['authorization_url'] 
                return redirect(payurl)
            else:
                return redirect(url_for('confirmation'))
    else:     
        return redirect(url_for('login'))

@app.route('/bookings/paymentverification')
def paystack():
    loggedin = session.get('user')
    refsession = session.get('trxref')
    if loggedin and refsession:
        #receive response from Payment Company and inform user of the transaction status
        ref=request.args.get('reference')

        headers = {'Authorization': 'Bearer sk_test_fa3151af8a36aea0eb83b7a1a83bb6e348f056ce',}

        #urlverify = "https://api.paystack.co/transaction/verify/"+ref

        response = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers=headers)
        
        rsp =response.json()#in json format
        #return render_template('user/test.html',rsp=rsp)

        if rsp['data']['status'] =='success':
            amt = rsp['data']['amount']
            ipaddress = rsp['data']['ip_address']
            t = Transaction.query.filter(Transaction.trx_ref==refsession).first()
            t.trx_status = 'Paid'
            db.session.commit()
            bookingid = session['book']
            b = db.session.query(Mybookings).get(bookingid)
            b.bookings_status = 'Success'
            db.session.commit()
            cpemail = b.bookings_craftsp.craftsp_email
            Message()
            msg = Message(subject="Testing Mail", sender="ogunyemii@gmail.com", recipients=[cpemail], body="Test Mail")
            msg.html= "<div><h1>You have a mendee booking</h1><p>Log into your dashboard to view booking details </p><hr><span>Officer, Mendee</span></div>"
            mail.send(msg)
            return render_template('user/success.html')
            #return 'update database and redirect them to the feedback page'
        else:
            t = Transaction.query.filter(Transaction.trx_ref==refsession).first()
            t.trx_status = 'Failed'
            db.session.commit()
            return render_template('user/failed.html') 
    else:
        abort(403)


@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template('user/signup.html')
    else:
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        pwd = request.form.get('password')
        address = request.form.get('address')
        converted = generate_password_hash(pwd)
        if fname =='' or lname=='' or email=='' or phone=='' or pwd=='' or address=='':
            flash('All fileds are required')
            return redirect(url_for('signup'))
        else:
            c = Customer(cust_fname=fname,cust_lname=lname,cust_email=email,cust_phone=phone,cust_password=converted,cust_address=address)
            db.session.add(c)
            db.session.commit() 
            session['user'] = c.id
            Message()
            msg = Message(subject="Testing Mail", sender="ogunyemii@gmail.com", recipients=[email], body="Test Mail")
            msg.html= "<div><h1>Thank you for signing up to Mendee</h1><p>We are glad to have you </p><hr><span>CEO, Mendee</span><img src='https://brandlogos.net/wp-content/uploads/2015/09/Google-logo-1-512x512.png'></div>"
            mail.send(msg)
            #return redirect(url_for('testmail'))
            return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    else:
        email= request.form.get('email')
        pwd = request.form.get('password')
        details = db.session.query(Customer).filter(Customer.cust_email==email).first()
        if details:
            loggedin_user = details.id
            hashedpass = details.cust_password
            check = check_password_hash(hashedpass,pwd)
            if check:
                session['user']=loggedin_user
                return redirect(url_for('account'))
            else:
                flash('invalid username or password')
                return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login')) 
        
@app.route('/user/account/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/user/account')
def account():
    loggedin_user = session['user']
    if loggedin_user !=None :
        mydata = db.session.query(Customer).get(loggedin_user)
        records = db.session.query(Customer).filter(Customer.id==loggedin_user).all()
        return render_template('user/dashboard.html', mydata=mydata,records=records)
    else:
        return redirect(url_for('login'))

# @app.route('/user/account/profile/editprofile')
# def editprofile():
#     return render_template('user/editprofile.html')

@app.route('/user/account/resetpassword',methods=['GET','POST'])
def resetpassword():
    loggedin = session.get('user')
    if loggedin:
        if request.method == 'GET':
            records = db.session.query(Customer).filter(Customer.id==loggedin).all()
            return render_template('user/resetpassword.html',records=records)
        else:
            oldpwd = request.form.get('oldpassword')
            newpwd = request.form.get('newpassword')
            confirmnewpwd = request.form.get('confirmnewpassword')
            data = db.session.query(Customer).get(loggedin)
            hashedpass = data.cust_password
            check = check_password_hash(hashedpass,oldpwd)
            if check:
                if newpwd == confirmnewpwd:
                    newhashedpass = generate_password_hash(newpwd)
                    data.cust_password = newhashedpass
                    db.session.commit()
                    flash('password successfully changed') 
                    #return 'changed'
                    return redirect(url_for('account'))
                else:
                    flash('Details do not match')
                    #return 'wrong new details'
                    return redirect(url_for('resetpassword'))
            else:
                flash('incorrect password')
                #return 'hasshed pass doesnt match old pass'
                return redirect(url_for('resetpassword'))
    else:
        return redirect(url_for('login'))

@app.route('/user/account/addprofilepic',methods=['GET','POST'])
def addprofilepic():
    loggedin = session.get('user')
    if loggedin:
        if request.method == 'GET':
            records = db.session.query(Customer).filter(Customer.id==loggedin).all()
            return render_template('user/addprofilepic.html',records=records)
        else:
            fileobj = request.files['uploadpic']
            if fileobj.filename == '':
                flash('Please select a file')
                return redirect(url_for('addprofilepic'))
            else:
                 #get the file extension,  #splits file into 2 parts on the extension
                name, ext = os.path.splitext(fileobj.filename)
                allowed_extensions=['.jpg','.jpeg','.png','.gif']
                if ext not in allowed_extensions:
                    flash(f'Extension {ext} is not allowed')
                    return redirect(url_for('addprofilepic'))  
                else:
                    sample_xters = random.sample(string.ascii_lowercase,10) 
                    newname = ''.join(sample_xters) + ext
                    #original = str(random.random() * 10000) + fileobj.filename
                    destination = 'mendeeapp/static/customerprofilepictures/' +newname
                    fileobj.save(destination)
                    #save details into database
                    custid = session.get('user')
                    c = db.session.query(Customer).get(custid)
                    c.cust_profile_pic =newname
                    db.session.commit()
                    flash ('profile successfully updated')
                    return redirect(url_for('account'))
    else:
        return redirect('/user/login') 
    
            
# @app.route('/user/editprofile',methods=['GET','POST'])
# def editprofile():
#     loggedin = session.get('user')
#     if loggedin:
#         if request.method == 'GET':
#             records = db.session.query(Customer).filter(Customer.id==loggedin).all()
#             return render_template('user/editprofile.html',records=records)
#         else:
#             fname = request.form.get('firstname')
#             lname = request.form.get('lastname')
#             email = request.form.get('email')
#             phone = request.form.get('phone')
#             address = request.form.get('address') 
#             custid = session.get('user')
#             c = db.session.query(Customer).get(custid)
#             c.cust_fname = fname
#             c.cust_lname = lname
#             c.cust_email = email
#             c.cust_phone = phone
#             c.cust_address = address
#             db.session.commit()
#             flash ('profile successfully updated')
#             return redirect(url_for('account'))
#     else:
#         return redirect('/user/login')

@app.route('/user/editprofile',methods=['GET','POST'])
def editprofile():
    loggedin = session.get('user')
    if loggedin:
        if request.method == 'GET':
            records = db.session.query(Customer).filter(Customer.id==loggedin).all()
            c = db.session.query(Customer).get(loggedin)
            return render_template('user/editprofile.html',records=records, c=c)
        else:
            fname = request.form.get('firstname')
            lname = request.form.get('lastname')
            email = request.form.get('email')
            phone = request.form.get('phone')
            address = request.form.get('address') 
            custid = session.get('user')
            c = db.session.query(Customer).get(custid)
            c.cust_fname = fname
            c.cust_lname = lname
            c.cust_email = email
            c.cust_phone = phone
            c.cust_address = address
            db.session.commit()
            flash ('profile successfully updated')
            return redirect(url_for('account'))
    else:
        return redirect('/user/login')

# @app.route('/user/editprofile',methods=['GET','POST'])            
# def editprofile():      
#     loggedin = session.get('user') 
#     if loggedin:
#         if request.method == 'GET':
#             records = db.session.query(Customer).filter(Customer.id==loggedin).all()
#             return render_template('user/editprofile.html',records=records)
#         else:
#             fileobj = request.files['uploadpic']
#             fname = request.form.get('firstname')
#             lname = request.form.get('lastname')
#             email = request.form.get('email')
#             phone = request.form.get('phone')
#             address = request.form.get('address') 
#             if fileobj.filename == '':
#                 flash('Please select a file')
#                 return redirect(url_for('editprofile'))
#             else:
#                  #get the file extension,  #splits file into 2 parts on the extension
#                 name, ext = os.path.splitext(fileobj.filename)
#                 allowed_extensions=['.jpg','.jpeg','.png','.gif']
#                 if ext not in allowed_extensions:
#                     flash(f'Extension {ext} is not allowed')
#                     return redirect(url_for('editprofile'))
#                 else:
#                     sample_xters = random.sample(string.ascii_lowercase,10) 
#                     newname = ''.join(sample_xters) + ext
#                     #original = str(random.random() * 10000) + fileobj.filename
#                     destination = 'mendeeapp/static/customerprofilepictures/' +newname
#                     fileobj.save(destination)
#                     #save details into database
#                     custid = session.get('user')
#                     c = db.session.query(Customer).get(custid)
#                     c.cust_profile_pic =newname
#                     c.cust_fname = fname
#                     c.cust_lname = lname
#                     c.cust_email = email
#                     c.cust_phone = phone
#                     c.cust_address = address
#                     db.session.commit()
#                     flash ('profile successfully updated')
#                     return redirect(url_for('account'))
#     else:
#         return redirect('/user/login')
            
@app.route('/lay')
def lay():
    loggedin_user = session['user']
    if loggedin_user !=None :
        #data = db.session.query(Customer).get(loggedin_user)
        records = db.session.query(Customer).filter(Customer.id==loggedin_user).all()
        return render_template('user/dashboardlayout.html',records=records)
    else:
        return redirect(url_for('login'))
    #return render_template('user/dashboardlayout.html')

@app.route('/user/account/payment')
def payment():
    loggedin = session.get('user')
    if loggedin:
            records = db.session.query(Customer).filter(Customer.id==loggedin).all()
            return render_template('user/payment.html',records=records) 

@app.route('/user/account/mymendeebookings',methods=['GET','POST'])
def mymendeebookings():
    loggedin = session.get('user')
    myref = session.get('trxref')
    bookingid = session['book']
    if loggedin:
        if request.method == 'GET':
            timedeets = session.get('timedate')
            deets = session.get('details1')  
            onetimedeet = db.session.query(Timedate).filter(Timedate.timedate_id==timedeets).first()
            onedeet = db.session.query(Details1).filter(Details1.details1_id==deets).first()
            records = db.session.query(Customer).filter(Customer.id==loggedin).all()
            bookingdeets = db.session.query(Mybookings).filter(Mybookings.customer_id==loggedin,Mybookings.btrx_ref!=None).all()
            #details = db.session.query(Details1).join(Timedate).join(Craftsperson).join(Transaction).order_by(Details1.customer_id).filter(Transaction==myref).all()
            #d = session.query(Details1, Timedate).select_from(join(Details1, Timedate)).filter(Details1.customer_id==Timedate.customer_id).all()
            #rec = db.session.query(Details1).join(Transaction).join(Timedate).order_by(Transaction.trx_custid).all()
            return render_template('user/mymendeeorder.html',records=records,onedeet=onedeet,onetimedeet=onetimedeet,timedeets=timedeets,deets=deets,bookingdeets=bookingdeets)
        else:
            # cancel = db.session.query(Mybookings).get(bookingid)  
            # cancel.bookings_status = 'cancelled' 
            # db.session.commit()
            can = Mybookings.query.filter(Mybookings.customer_id==loggedin, Mybookings.bid==bookingid).first()
            can.bookings_status = 'cancelled'
            db.session.commit()
            #cpemail = can.bookings_craftsp.craftsp_email
            #cpe3 = session['craftsp']
            #cpe2 = can.craftsp_id
            mend = db.session.query(Craftsperson).filter(Craftsperson.id==Mybookings.craftsp_id).first()
            mendmail = mend.craftsp_email      
            Message()
            msg = Message(subject="Testing Mail", sender="ogunyemii@gmail.com", recipients=[mendmail], body="Test Mail")
            msg.html= "<div><h1>Your booking with a customer has been cancelled</h1><p>Log in to your dashboard for more details </p><hr><span>Head Bookings, Mendee</span></div>"
            mail.send(msg)
            return redirect(url_for('mymendeebookings'))
    else:
        return redirect(url_for('login'))  

@app.route('/user/bookamender')
def bookamender():
    return render_template('user/bookamender.html')

@app.route('/testmail')
def testmail():
    Message()
    msg = Message(subject="Testing Mail", sender="ogunyemii@gmail.com", recipients=['cutymotunrayo@gmail.com'], body="Test Mail")
    msg.html= "<div><h1>Thank you for subscribing to Mendee</h1><p>You are among the lucky people to get first hand information on juicy offers </p><hr><span>CEO, Mendee</span><img src='https://brandlogos.net/wp-content/uploads/2015/09/Google-logo-1-512x512.png'></div>"
    mail.send(msg)
    return "Mail was sent"

@app.route('/catxx',methods=['GET','POST'])
def catxx():
    loggedin = 12
    if loggedin:
        if request.method=='GET':
            cat = db.session.query(Category).all()
            return render_template('/user/index.html')
        else:
            fileobj = request.files['cat']
            if fileobj.filename == '':
                flash('Please select a file')
                return redirect(url_for('home'))
            else:
                 #get the file extension,  #splits file into 2 parts on the extension
                name, ext = os.path.splitext(fileobj.filename)
                allowed_extensions=['.jpg','.jpeg','.png','.gif']
                if ext not in allowed_extensions:
                    flash('not allowed')  
                    return redirect(url_for('home'))
                else:
                    sample_xters = random.sample(string.ascii_lowercase,10) 
                    newname = ''.join(sample_xters) + ext
                    #original = str(random.random() * 10000) + fileobj.filename
                    destination = 'mendeeapp/static/categorypic/' +newname
                    fileobj.save(destination)
                    #save details into database
                    #cpid = session.get('admin')  
                    #catid = session['cat']                    
                    #c = db.session.query(Craftsperson).get(cpid)
                    cate = db.session.query(Service).get(13) 
                    cate.service_pic =newname
                    db.session.commit()
                    flash ('profile successfully updated')
                    return 'in db now'


