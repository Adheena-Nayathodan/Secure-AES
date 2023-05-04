
from flask import *


from src.dbconnection import *
import os

from werkzeug.utils import secure_filename


from src.samp import *

app=Flask(__name__)
app.secret_key = "27254254"




import functools

def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return render_template('login_index.html')
        return func()

    return secure_function


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@app.route('/')
def log():
    return render_template('login_index.html')

@app.route('/login',methods=['post'])
def login():
    uname = request.form['textfield']
    password = request.form['textfield2']
    qry="SELECT * FROM `login`WHERE `username`=%s AND `password`=%s"
    val=(uname,password)
    r=selectone(qry,val)
    if r is None:
        return '''<script>alert("invalid");window.location="/"</script>'''
    elif r ['type'] =='admin':
        session['lid'] = r['lid']
        return '''<script>alert("logined");window.location="/adminhome"</script>'''
    elif r ['type'] =='user':
        session['lid'] = r['lid']
        print("eeeeeeeeee")
        return redirect('/userhome')
        # return '''<script>alert("logined");window location="/managerhome"</script>'''
    else:
        return '''<script>alert("invalid");window.location="/"</script>'''




@app.route('/adminhome')
@login_required
def adminhome():
    return  render_template('adminindex.html')


@app.route('/doubt_reply')
@login_required
def doubt_reply():
    id=request.args.get('id')
    session['did']=id
    return  render_template('reply.html')


@app.route('/doubt_reply1',methods=['post'])
@login_required
def doubt_reply1():
    reply=request.form['textarea']
    qry="UPDATE `doubt` SET  `reply`=%s WHERE `did`=%s"
    val=(reply,session['did'])
    iud(qry,val)
    return '''<script>alert("Successfull");window.location="/view_doubt"</script>'''




@app.route('/view_doubt')
@login_required
def view_doubt():
    q='SELECT * FROM `user` JOIN `doubt`ON `user`.lid=`doubt`.lid'
    r=selectall(q)
    return  render_template('viewdoubt.html',val=r)



@app.route('/doubt', methods=['post'])
def doubt():
    doubt = request.form['textarea']
    qry = "insert into doubt values(null,%s,%s,curdate(),'pending')"
    val = (session['lid'], doubt)
    iud(qry, val)
    return '''<script>alert("Successfull");window.location="/viewreply"</script>'''







@app.route('/verify', methods=['get'])
def verify():

    qry = "SELECT * FROM user join login on user.lid=login.lid where type='pending'"
    res = selectall(qry)
    return render_template("verify users.html",val=res)


@app.route('/reject', methods=['post','get'])
def reject():
    id=request.args.get('id')
    qry="UPDATE `login` SET type='Rejected' WHERE lid=%s"

    iud(qry,id)
    return '''<script>alert("Rejected");window.location="/verify"</script>'''



@app.route('/accept', methods=['post', 'get'])
def accept():
    id = request.args.get('id')
    qry = "UPDATE `login` SET type='user' WHERE lid=%s"
    iud(qry, id)
    return '''<script>alert("Accepted");window.location="/verify"</script>'''



@app.route('/viewfeed')
@login_required
def viewfeed():
    q='SELECT * FROM `user` JOIN `feedback` ON `user`.lid=`feedback`.lid'
    r=selectall(q)
    return  render_template('viewfeedback.html',val=r)

@app.route('/mngecls')
@login_required
def mngecls():
    q='SELECT * FROM `class`'
    r=selectall(q)
    return  render_template('managecls.html',val=r)


@app.route('/addcls')
@login_required
def addcls():
    return  render_template('addclass.html')


@app.route('/editcls')
@login_required
def editcls():
    id=request.args.get('id')
    session['cidd']=id
    qry="select * from class where cid=%s"
    res=selectone(qry,id)
    return  render_template('editcls.html',val=res)



@app.route('/addcl',methods=['post'])
@login_required
def addcl():
    fromtime=request.form['textfield']
    totime=request.form['textfield2']
    date = request.form['textfield3']
    subject = request.form['textfield4']
    qry="insert into class values(null,%s,%s,%s,%s)"
    val=(fromtime,totime,date,subject)
    iud(qry,val)
    return '''<script>alert("ADDED");window.location="/mngecls"</script>'''


@app.route('/editcl',methods=['post'])
@login_required
def editcl():
    fromtime=request.form['textfield']
    totime=request.form['textfield2']
    date = request.form['textfield3']
    subject = request.form['textfield4']
    qry="update class set from_time=%s,to_time=%s,date=%s,subject=%s where cid=%s"
    val=(fromtime,totime,date,subject,session['cidd'])
    iud(qry,val)
    return '''<script>alert("Edited");window.location="/mngecls"</script>'''



@app.route('/dltcl')
@login_required
def dltcl():
    id=request.args.get('id')
    qry="delete from class where cid=%s"
    iud(qry,id)
    return '''<script>alert("Deleted");window.location="/mngecls"</script>'''




@app.route('/userhome')
@login_required
def userhome():
    return  render_template('user/userindex.html')


@app.route('/sendfeed')
@login_required
def sendfeed():
    return  render_template('user/sendfeed.html')



@app.route('/sendf',methods=['get','post'])
@login_required
def sendf():
   feed=request.form['textarea']
   qry="insert into feedback values(null,%s,%s,curdate())"
   val=(session['lid'],feed)
   iud(qry,val)
   return '''<script>alert("Sended");window.location="/userhome"</script>'''


@app.route('/viewclass')
@login_required
def viewclass():
    q='SELECT * FROM `class`'
    r=selectall(q)
    return  render_template('user/viewclass.html',val=r)


@app.route('/viewreply', methods=['post','get'])
def viewreply():

    qry = "SELECT * FROM doubt WHERE lid=%s"
    r = selectall2(qry,session['lid'])

    return  render_template('user/viewreply.html',val=r)


@app.route('/adddoubt')
@login_required
def adddoubt():
    return  render_template('user/senddoubt.html')



# =======================


@app.route('/uploadnote')
def uploadnote():

    return (render_template("uploadnotes.html"))
def kwygen():
    import string
    import random

    # initializing size of string
    N = 7

    # using random.choices()
    # generating random strings
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))

    # print result
    print("The generated random string : " + str(res))
    return str(res)


@app.route('/add_note', methods=['post'])
def add_note():
        qp = request.files['file']
        fname = secure_filename(qp.filename)
        qp.save('static/notes/' + fname)
        f = open("static/notes/" + fname, "rb")
        fileread = f.read()
        key = kwygen()

        key = str(key)
        path=r"C:\Users\KRISHNAN K V\PycharmProjects44\secure_aes\src\static\notes\\"+fname
        pth=r"C:\Users\KRISHNAN K V\PycharmProjects44\secure_aes\src\static\encrypted\\"+fname
        with open(path, "rb") as imageFile:
            stri = base64.b64encode(imageFile.read()).decode('utf-8')
            enc1 = encrypt(stri,key ).decode('utf-8')
            fh = open(pth, "wb")
            fh.write(base64.b64decode(enc1))
            fh.close()
        # pdata = base64.b64encode(fileread)
        # print("enc start")
        # et = encrypt(pdata.decode('ascii'), key)
        # with open('static/encrypted/'  + fname, "wb") as file:
        #  file.write(et)
        #  encfile =  fname
        qry2 = "INSERT INTO `notes` VALUES(NULL,%s,%s)"
        val = (fname, str(key))
        iud(qry2, val)
        return '''<script> alert("success"); window.location="/adminhome"</script>'''

@app.route('/notewdw')
@login_required
def notewdw():
    qr="SELECT * FROM `fees`  WHERE user_id=%s"
    re=selectone(qr,session['lid'])
    if re is not None:
        qry="select * from notes"
        res=selectall(qry)
        return  render_template('user/viewnote.html',val=res)
    else:
        return render_template("user/payfee.html")

@app.route('/dwnld')
@login_required
def dwnld():
    id=request.args.get('id')
    qry="SELECT * FROM notes WHERE nid=%s "
    dataa = selectone(qry,id)
    print(dataa)
    img=dataa['name']
    key=dataa['amstrong_no']
    password="#34^%%$w5454"
    print(img)
    # input_file = 'input/sample.pdf'
    pth1=r"C:\Users\KRISHNAN K V\PycharmProjects44\secure_aes\src\static\encrypted\\"+img
    pth2=r"C:\Users\KRISHNAN K V\PycharmProjects44\secure_aes\src\static\downloads\\"+img
    with open(pth1, "rb") as imageFile:
        stri = base64.b64encode(imageFile.read()).decode('utf-8')
        dec2 = decrypt1(stri, key).decode('utf-8')
        fh1 = open(pth2, "wb")
        fh1.write(base64.b64decode(dec2))
        fh1.close()
    return render_template("user/download.html",val=dataa)

@app.route('/view_details')
@login_required
def view_details():
    qry = "select * from user where lid=%s"
    res = selectone(qry, session['lid'])
    return render_template("user/details.html", val=res)




# @app.route('/user_pay_proceed', methods=['post'])
# @login_required
# def user_pay_proceed():
#     import razorpay
#     amount = request.form['textfield']
#     session['pay_amount'] = amount
#
#     client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
#     print(client)
#     payment = client.order.create({'amount': amount+"00", 'currency': "INR", 'payment_capture': '1'})
#
#     return render_template('UserPayProceed.html', p=payment)


@app.route('/user_pay_proceed', methods=['post','get'])
@login_required
def user_pay_proceed():
    import razorpay
    amount = request.form['textfield']
    session['pay_amount'] = amount
    client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    print(client)
    payment = client.order.create({'amount': amount+"00", 'currency': "INR", 'payment_capture': '1'})
    qry = "select * from user where lid=%s"
    res = selectone(qry, session['lid'])
    return render_template('user/UserPayProceed.html', p=payment,val=res)



@app.route('/on_payment_success', methods=['post'])
@login_required
def on_payment_success():
    amt = session['pay_amount']
    qry = "INSERT INTO `fees` VALUES(NULL,%s,%s,CURDATE())"
    iud(qry, ( session['lid'], amt))

    # qry = "UPDATE `charity_information` SET `amount`=`amount`-%s WHERE `id`=%s"
    # iud(qry, (amt,charity))

    return '''<script>alert("Success! Thank you for your Contribution");window.location="userhome"</script>'''


@app.route('/viewpayment')
@login_required
def viewpayment():
    qry = "select * from user join fees on user.lid=fees.user_id"
    res = selectall(qry)
    return render_template("viewpayment.html", val=res)





@app.route('/register')
def register():
         return render_template('user/register.html')

@app.route('/registerindex')
def registerindex():
         return render_template('user/regindex.html')


@app.route('/regm',methods=['post'])
def regm():
    name = request.form['textfield']
    lname = request.form['textfield2']
    email = request.form['textfield3']
    phone = request.form['textfield4']
    place = request.form['textfield5']
    post = request.form['textfield6']
    pin = request.form['textfield7']

    username=request.form['textfield8']
    password = request.form['textfield9']
    qry="INSERT INTO login VALUES(NULL,%s,%s,'pending')"
    va=(username,password)
    id=iud(qry,va)
    q="INSERT INTO `user` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(name,lname,place,post,pin,phone,email,str(id))
    iud(q,val)
    return '''<script>alert("Registration suucessfull");window.location="/"</script>'''



app.run(debug=True)
