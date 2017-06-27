from app import app
from flask import Flask,flash,redirect,render_template,request,session
from flask import jsonify
import psycopg2

   

#set homepage to index.html
@app.route('/')
def index():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return home()

@app.route('/login', methods = ['POST'])
def login():
	if request.form['password'] == 'password' and request.form['user_id'] == 'admin':
		global user_id
		user_id = 12338295#12309459#request.form['user_id']
		session['logged_in'] = True
		y = get_info()
		x = get_trades()
	
		return render_template('home.html',y = y,x = x)

	else:
		flash('wrong password')
	return index()
		

@app.route('/home', methods = ['GET','POST'])
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
        else:
		if request.method == 'POST':
			update_funds(request.form['funds'])
			update_buy(request.form['buy'])
			update_sell(request.form['sell'])
		y = get_info()
		x = get_trades()
	
		return render_template('home.html',y = y,x = x)


		
def get_trades():
	conn = connect_slave_db()
	cur = conn.cursor()
	#cur.execute("select name,buy,sell,funds  from user_settings where uid = %s",(user_id,))
	cur.execute("select price,type,stock,transactions.Qty,Time from transactions where uid = %s;",(user_id,))
	res = cur.fetchall()
	response_list = []
	for val in res:

		response_list.append(val)
		
	#json_data = [{"Name":x[0],"Buy" : x[1],"Sell" : x[2], "Funds" : x[3]} for x in res]
	json_data = [{"Price":x[0],"Type": x[1],"Stock":x[2],"Qty":x[3],"Time":x[4]} for x in response_list]
	return json_data


def get_info():
	conn = connect_slave_db()
	cur = conn.cursor()
	cur.execute("select name,buy,sell,funds  from user_settings where uid = %s;",(user_id,))
	res = cur.fetchall()
	response_list = []
	for val in res:
		
		response_list.append(val)
	json_data = [{"name":x[0],"buy":x[1],"sell":x[2],"funds":x[3]} for x in response_list]
	return json_data
	

def connect_master_db():

	try:
		conn = psycopg2.connect("dbname='transactions' user = 'postgres' host = 'transactions-trades.ca4vkhzfvza0.us-east-1.rds.amazonaws.com' password = 'kakarala'") 
		return conn
	except:
		print "Not Connected"

def connect_slave_db():

        try:
                conn = psycopg2.connect("dbname='transactions' user = 'postgres' host = 'replica1.ca4vkhzfvza0.us-east-1.rds.amazonaws.com' password = 'kakarala'")
                return conn
        except:
                print "Not Connected"	
def update_funds(funds):
	ins_funds = str(funds)
	if funds == '':
		print("None")
		return None
	else:
		conn = connect_master_db()
		cursor = conn.cursor()
		cursor.execute("update user_settings set funds =cast(%s as double precision)  where uid = %s;",(ins_funds,user_id,))
		print(cursor.rowcount)
		conn.commit()
		cursor.close()
		

def update_buy(buy):
	ins_buy = str(buy)
	if buy == '':
		print("None")
		return None
	else:
		conn = connect_master_db()
		cursor = conn.cursor()
		cursor.execute("update user_settings set buy =%s  where uid = %s",(ins_buy,user_id,))
		conn.commit()
		cursor.close()
	

def update_sell(sell):
	ins_sell = str(sell)
	if sell =='':
		print("None")
		return None
	else:	
		conn = connect_master_db()
		cursor = conn.cursor()
		cursor.execute("update user_settings set sell =%s  where uid = %s;",(ins_sell,user_id,))
		conn.commit()
		cursor.close()
		



	
