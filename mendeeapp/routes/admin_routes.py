import random,string,json,requests,os
from flask import render_template,request,redirect,flash,url_for,make_response,session
from werkzeug.security import generate_password_hash, check_password_hash


from mendeeapp import app,csrf,db
#from mendeeapp.myforms import 
from mendeeapp.mymodels import Customer,Craftsperson,Category,Service,Bookings,Payment,Feedback,Bankdetails,Mybookings,Transaction
from mendeeapp import mail,Message

@app.route('/mender/signup',methods=['GET','POST']) 
def mendersignup():
    if request.method== 'GET':
        return render_template('admin/mendersignup.html')
    else:
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        bname = request.form.get('businessname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        pwd = request.form.get('password')
        address = request.form.get('address')
        desc = request.form.get('desc')
        role = request.form.get('role')
        converted = generate_password_hash(pwd)
        if fname =='' or lname=='' or bname=='' or email=='' or phone=='' or pwd=='' or address=='' or role=='' or desc=='':
            flash('All fileds are required')
            return redirect(url_for('mendersignup'))
        else:
            servicetbl = db.session.query(Service).filter(Service.service_name==role).first()
            serid = servicetbl.id
            cp = Craftsperson(craftsp_fname=fname,craftsp_lname=lname,craftsp_businessname=bname,craftsp_email=email,craftsp_phone=phone,craftsp_password=converted,craftsp_address=address,craftsp_role=role,service_id=serid,craftsp_desc=desc)
            db.session.add(cp)
            db.session.commit() 
            session['admin'] = cp.id 
            # servicetbl = db.session.query(Service).filter(Service.service_name==role).first()
            # servicetbl.id=session['serv']   
            Message()
            msg = Message(subject="Testing Mail", sender="ogunyemii@gmail.com", recipients=[email], body="Test Mail")
            msg.html= "<div><h1>Thank you for joining Mendee</h1><p>We are glad to have you </p><hr><span>CEO, Mendee</span><img src='https://brandlogos.net/wp-content/uploads/2015/09/Google-logo-1-512x512.png'></div>"
            mail.send(msg)
            return redirect(url_for('menderaccount'))

@app.route('/mender/login',methods=['GET','POST'])   
def menderlogin():      
    if request.method == 'GET':
        return render_template('admin/mendersignup.html')
    else:
        email= request.form.get('email')
        pwd = request.form.get('password')
        deets = db.session.query(Craftsperson).filter(Craftsperson.craftsp_email==email).first()
        if deets:
            loggedin_admin = deets.id
            hashedpass = deets.craftsp_password
            check = check_password_hash(hashedpass,pwd)
            if check:
                session['admin']=loggedin_admin
                return redirect(url_for('menderaccount')) 
            else:
                flash('invalid username or password')
                return redirect(url_for('menderlogin'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('menderlogin'))

@app.route('/mender/account/logout')
def menderlogout():
    session.pop('admin', None)
    return redirect('/') 

@app.route('/mender/account')
def menderaccount():
    loggedin_admin = session.get('admin') 
    if loggedin_admin :
        mydata = db.session.query(Craftsperson).get(loggedin_admin)
        records = db.session.query(Craftsperson).filter(Craftsperson.id==loggedin_admin).all()
        return render_template('admin/menderaccount.html', mydata=mydata,records=records)
    else:
        return redirect(url_for('menderlogin'))

@app.route('/mender/account/addprofilepic',methods=['GET','POST'])
def menderaddprofilepic():
    loggedin = session.get('admin')
    if loggedin:  
        if request.method == 'GET':
            records = db.session.query(Craftsperson).filter(Craftsperson.id==loggedin).all()
            return render_template('admin/menderaddprofilepic.html',records=records)
        else:
            fileobj = request.files['uploadpic']
            if fileobj.filename == '':
                flash('Please select a file')
                return redirect(url_for('menderaddprofilepic'))
            else:
                 #get the file extension,  #splits file into 2 parts on the extension
                name, ext = os.path.splitext(fileobj.filename)
                allowed_extensions=['.jpg','.jpeg','.png','.gif']
                if ext not in allowed_extensions:
                    flash(f'Extension {ext} is not allowed')  
                    return redirect(url_for('menderaddprofilepic'))
                else:
                    sample_xters = random.sample(string.ascii_lowercase,10) 
                    newname = ''.join(sample_xters) + ext
                    #original = str(random.random() * 10000) + fileobj.filename
                    destination = 'mendeeapp/static/menderprofilepicture/' +newname
                    fileobj.save(destination)
                    #save details into database
                    cpid = session.get('admin')
                    c = db.session.query(Craftsperson).get(cpid)
                    c.craftsp_profile_pic =newname
                    db.session.commit()
                    flash ('profile successfully updated')
                    return redirect(url_for('menderaccount'))
    else:
        return redirect('/user/menderlogin')   

@app.route('/mender/account/mendereditprofile',methods=['GET','POST']) 
def mendereditprofile():
    loggedin = session.get('admin') 
    if loggedin:
        if request.method == 'GET':
            records = db.session.query(Craftsperson).filter(Craftsperson.id==loggedin).all()
            cp = db.session.query(Craftsperson).get(loggedin)
            return render_template('admin/mendereditprofile.html',records=records, cp=cp)
        else:
            fname = request.form.get('firstname')
            lname = request.form.get('lastname')
            bname = request.form.get('businessname')
            email = request.form.get('email')
            phone = request.form.get('phone')
            address = request.form.get('address') 
            desc = request.form.get('desc')
            cpid = session.get('admin')
            cp = db.session.query(Craftsperson).get(cpid)
            cp.craftsp_fname = fname
            cp.craftsp_lname = lname
            cp.craftsp_businessname = bname
            cp.craftsp_email = email
            cp.craftsp_phone = phone
            cp.craftsp_address = address
            cp.craftsp_desc = desc
            db.session.commit() 
            flash ('profile successfully updated')
            return redirect(url_for('menderaccount'))
    else:
        return redirect('/user/mendersignup')
 

@app.route('/mender/account/menderresetpassword',methods=['GET','POST'])
def menderresetpassword():
    loggedin = session.get('admin')
    if loggedin:
        if request.method == 'GET':
            records = db.session.query(Craftsperson).filter(Craftsperson.id==loggedin).all()
            return render_template('admin/menderresetpassword.html',records=records)
        else:
            oldpwd = request.form.get('oldpassword')
            newpwd = request.form.get('newpassword')
            confirmnewpwd = request.form.get('confirmnewpassword')
            data = db.session.query(Craftsperson).get(loggedin)
            hashedpass = data.craftsp_password
            check = check_password_hash(hashedpass,oldpwd)
            if check:
                if newpwd == confirmnewpwd:
                    newhashedpass = generate_password_hash(newpwd)
                    data.craftsp_password = newhashedpass
                    db.session.commit()
                    flash('password successfully changed') 
                    #return 'changed'
                    return redirect(url_for('menderaccount'))
                else:
                    flash('Details do not match')
                    #return 'wrong new details'
                    return redirect(url_for('menderresetpassword'))
            else:
                flash('incorrect password')
                #return 'hasshed pass doesnt match old pass'
                return redirect(url_for('menderresetpassword'))
    else:
        return redirect(url_for('mendersignup'))


@app.route('/mender/account/menderpaymentdetails',methods=['GET','POST'])
def menderpaymentdetails():
    loggedin = session.get('admin')
    if loggedin:
        if request.method == 'GET':
            records = db.session.query(Craftsperson).filter(Craftsperson.id==loggedin).all()
            return render_template('admin/menderpaymentdetails.html',records=records)
        else:
            accname = request.form.get('accountname')
            accnumber = request.form.get('accountnumber')
            bkname = request.form.get('bankname')
            if accname=='' or accnumber=='' or bkname=='':
                flash('All fields are required')
                return redirect(url_for('menderpaymentdetails'))
            else:  
                bd = Bankdetails(account_name=accname,account_number=accnumber,bank_name=bkname,craftsp_id=loggedin)
                db.session.add(bd)
                db.session.commit()
                return redirect(url_for('menderaccount'))
    else:
        return redirect('/mender/mendersignup') 

@app.route('/mender/account/menderbookings')
def menderbookings():
    myref = session.get('trxref')
    loggedin = session.get('admin')
    if loggedin:
        records = db.session.query(Craftsperson).filter(Craftsperson.id==loggedin).all()
        mybookings = db.session.query(Mybookings).filter(Mybookings.craftsp_id==loggedin, Mybookings.btrx_ref != '' ).all()
        return render_template('admin/menderbookings.html',records=records,mybookings=mybookings)
    else:
        return redirect(url_for('menderlogin'))   
 




# @app.route('/servicepic')  
# def servicepic():
#     loggedin_ad = 
#     if loggedin_ad:
#         if request.method == 'GET':
#             #records = db.session.query(Customer).filter(Customer.id==loggedin_ad).all()
#             return render_template('user/addprofilepic.html')
#         else:
#             fileobj = request.files['uploadpic']
#             if fileobj.filename == '':
#                 flash('Please select a file')
#                 return redirect(url_for('addprofilepic'))
#             else:
#                  #get the file extension,  #splits file into 2 parts on the extension
#                 name, ext = os.path.splitext(fileobj.filename)
#                 allowed_extensions=['.jpg','.jpeg','.png','.gif']
#                 if ext not in allowed_extensions:                                                     
#                     flash(f'Extension {ext} is not allowed')
#                     return redirect(url_for('addprofilepic'))
#                 else:                                                                                   
#                     sample_xters = random.sample(string.ascii_lowercase,10) 
#                     newname = ''.join(sample_xters) + ext
#                     #original = str(random.random() * 10000) + fileobj.filename
#                     destination = 'mendeeapp/static/serviceimg/' +newname
#                     fileobj.save(destination)                   
#                     #save details into database                                                
#                     # custid = session.get('user')                                                             
#                     ad = db.session.query(Craftsperson).filter(Craftsperson.id==loggedin).all()
#                     c = db.session.query(Customer).get(custid)
#                     c.cust_profile_pic =newname
#                     db.session.commit()                                                     
#                     flash ('profile successfully updated')
#                     return redirect(url_for('account'))
#     else:
#         return redirect('/user/login') 