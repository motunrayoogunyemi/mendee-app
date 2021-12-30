import datetime

from mendeeapp import db

class Customer(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    cust_fname = db.Column(db.String(55),nullable=False)
    cust_lname = db.Column(db.String(55),nullable=False)
    cust_phone = db.Column(db.Integer(),nullable=False)
    cust_email = db.Column(db.String(60),nullable=False)
    cust_password = db.Column(db.String(255),nullable=False)
    cust_address = db.Column(db.String(150),nullable=False)
    cust_profile_pic = db.Column(db.String(100),nullable=True)
    cust_booking = db.relationship('Bookings', backref='customer')

class Craftsperson(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    craftsp_fname = db.Column(db.String(55),nullable=False)
    craftsp_lname = db.Column(db.String(55),nullable=False)
    craftsp_businessname = db.Column(db.String(55),nullable=False)
    craftsp_email = db.Column(db.String(60),nullable=False)
    craftsp_phone = db.Column(db.Integer(),nullable=False)
    craftsp_password = db.Column(db.String(255),nullable=False)
    craftsp_address = db.Column(db.String(55),nullable=False)
    craftsp_role = db.Column(db.String(60),nullable=False)
    craftsp_profile_pic = db.Column(db.String(100),nullable=True)
    craftsp_desc = db.Column(db.String(255),nullable=False)
    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'))
    serv_craftsperson = db.relationship('Service', backref='craftsperson')
    booking_scraftsperson = db.relationship('Bookings', backref='craftsperson')

class Bankdetails(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    account_name = db.Column(db.String(150),nullable=False)
    account_number = db.Column(db.String(20),nullable=False)
    bank_name = db.Column(db.String(100),nullable=False)
    craftsp_id = db.Column(db.Integer(), db.ForeignKey('craftsperson.id'))

class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    cat_name = db.Column(db.String(55),nullable=False)
    cat_description = db.Column(db.String(255),nullable=False)
    category_pic = db.Column(db.String(100),nullable=True)
    # serv_category = db.relationship('Service', backref='category')

class Service(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    service_name = db.Column(db.String(55),nullable=False)
    service_price = db.Column(db.Integer(),nullable=False)
    service_desc1 = db.Column(db.String(1000),nullable=False)
    service_desc2 = db.Column(db.String(5000),nullable=False)
    service_pic = db.Column(db.String(100),nullable=True)
    category_id = db.Column(db.Integer(), db.ForeignKey('category.id'))
    # craftsp_id = db.Column(db.Integer(), db.ForeignKey('craftsperson.id'))
    serv_booking = db.relationship('Bookings', backref='service')
    serv_category = db.relationship('Category', backref='myservice')

class Bookings(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'))
    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'))
    craftsp_id = db.Column(db.Integer(), db.ForeignKey('craftsperson.id'))
    bookings_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    bookings_delivery_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    bookings_delivery_status = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

class Payment(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'))
    bookings_id = db.Column(db.Integer(), db.ForeignKey('bookings.id'))
    date_paid = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    pay_serv = db.relationship('Service', backref='payment')
    pay_book = db.relationship('Bookings', backref='payment')

class Feedback(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'))
    craftsp_id = db.Column(db.Integer(), db.ForeignKey('craftsperson.id'))
    review = db.Column(db.String(1000),nullable=False)
    cust_feedb = db.relationship('Customer', backref='feedback')
    craftsp_feedb = db.relationship('Craftsperson', backref='feedback')

class Details1(db.Model):
    details1_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'))
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'))
    details1_location = db.Column(db.String(500),nullable=False)
    details1_time = db.Column(db.String(100),nullable=False)
    details1_service = db.Column(db.String(100),nullable=False)
    details1_details = db.Column(db.String(1000),nullable=True)
    dservice = db.relationship('Service', backref='details1')

class Timedate(db.Model):
    timedate_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'))
    timedate_month = db.Column(db.String(55),nullable=False)
    timedate_date = db.Column(db.String(20),nullable=False)
    timedate_time = db.Column(db.String(20),nullable=False)

class Transaction(db.Model):
    trx_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    trx_custid = db.Column(db.Integer(),db.ForeignKey('customer.id'), nullable=False)
    trx_amt = db.Column(db.Float(), nullable=False)
    trx_status = db.Column(db.String(40), nullable=False)
    trx_others = db.Column(db.String(255), nullable=True)
    trx_ref= db.Column(db.String(12), nullable=False)
    trx_ipaddress= db.Column(db.String(20), nullable=True)
    trx_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)    
    customer=db.relationship("Customer",backref="custtrx")

class Mybookings(db.Model):
    bid = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'))
    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'))
    craftsp_id = db.Column(db.Integer(), db.ForeignKey('craftsperson.id'))
    #trx_id = db.Column(db.Integer(), db.ForeignKey('transaction.trx_id'))
    btrx_ref= db.Column(db.String(12), nullable=True)
    bdetails1_service = db.Column(db.String(100),nullable=False)
    btimedate_month = db.Column(db.String(55),nullable=True)
    btimedate_date = db.Column(db.String(20),nullable=True)
    btimedate_time = db.Column(db.String(20),nullable=True)
    bdetails1_location = db.Column(db.String(500),nullable=False)
    bookings_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    bookings_status = db.Column(db.String(40), nullable=True)
    bookings_craftsp = db.relationship('Craftsperson', backref='bk')
    bookings_service = db.relationship('Service', backref='bksv')
    bookings_cust = db.relationship('Customer', backref='bkcust')