from mysql.connector import connect, cursor
from os import urandom
from hashlib import pbkdf2_hmac
from auth import authUser,authHost,authPasswd,authDb
from random import randint, sample
import json
from datetime import date

#==================================================Hashing Password================================
def hashPasswd(passwd):
	salt = urandom(64)
	return pbkdf2_hmac(
		'sha256',
		passwd.encode('utf-8'),
		salt,
		100000),salt
def hashPasswdCheck(passwd,salt):
	return pbkdf2_hmac(
		'sha256',
		passwd.encode('utf-8'),
		salt,
		100000)
#===================================================Existence=====================
def checkExistence(email):
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return
	try:
		cur = conn.cursor()
		cur.execute('Select email from userLogin where email=%s',(email,))
		if cur.fetchall():
			cur.close()
			conn.close()
			return True
		else: 
			cur.close()
			conn.close()
			return False

	except:
		return
#===================================================Password Settings=============================
def changePasswd(oldPasswd,newPasswd):
	query = ('SELECT * FROM userLogin WHERE userId = %s','UPDATE userLogin SET passwd= %s,salt=%s WHERE userId=%s')
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return False

	try:
		cur = conn.cursor()

		#Validating Record	
		cur.execute(query[0],(userId,))
		record = cur.fetchone()
		
		passwdSalt = hashPasswd(newPasswd)

		if hashPasswdCheck(oldPasswd,record[3]) == record[2]:
			cur.execute(query[1],(passwdSalt[0],passwdSalt[1],userId))

			conn.commit()
			cur.close()	
			conn.close()

			return True

		else:
			return False

	except:
		return False
def deleteAccount(passwd):
	query = ('SELECT * FROM userLogin WHERE userId = %s','DELETE FROM userLogin WHERE userId=%s')

	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return False

	try:
		cur = conn.cursor()

		#Validating Record	
		cur.execute(query[0],(userId,))
		record = cur.fetchone()
		

		if hashPasswdCheck(passwd,record[3]) == record[2]:
			refreshRemove(cur, conn)
			cur.execute(query[1],(userId,))

			conn.commit()
			cur.close()	
			conn.close()

			return True

		else:
			return False

	except:
		return False
#===================================================Credits===============
def selectQuiz():
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return

	try:
		cur = conn.cursor()
		cur.execute('SELECT type FROM creditQuiz')
		data = cur.fetchall()
		cur.close()
		conn.close()
		return [x[0] for x in data]
	except:
		return
def earnCredit(quizType):
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return

	try:
		cur = conn.cursor()
		cur.execute('SELECT quiz FROM creditQuiz WHERE type=%s',(quizType,))
		quizJson = json.loads(cur.fetchone()[0])

		qPrompt = []
		tmp = 1
		#rendering json
		for q in quizJson:
			qPrompt.append({
	        'type': 'rawlist',
	        'name': q,
	        'message': q,
	        'choices': quizJson[q][:-1]
	    })
		return sample(qPrompt, 3), quizJson
		cur.close()
		conn.close()
	
	except:
		return
def addCredit(amount):

	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return
	try:
		cur = conn.cursor()
		cur.execute('UPDATE credits SET custCredit=custCredit+%s WHERE userID=%s',(amount, userId))
		conn.commit()
		cur.close()
		conn.close()
		return True
	except:
		return	
#==================================================Help============================================
def help():
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return

	cur = conn.cursor()
	try:
		cur.execute('SELECT type FROM help')
		data = cur.fetchall()
		cur.close()
		conn.close()
		return [x[0] for x in data]
	except:
		return
def helpType(typ):
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return

	cur = conn.cursor()
	try:
		cur.execute('SELECT note FROM help WHERE type=%s',(typ,))
		data = cur.fetchone()[0]
		cur.close()
		conn.close()
		return data
	except:
		return
def frq():
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return

	cur = conn.cursor()
	try:
		cur.execute('SELECT ques,reply FROM reports')
		data = cur.fetchall()
		cur.close()
		conn.close()
		return data
	except:
		return
def report(question):
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return

	cur = conn.cursor()
	try:
		cur.execute('INSERT INTO reports(reportId,ques) VALUES(%s,%s)',(userId, question))
		conn.commit()
		cur.close()
		conn.close()
		return True
	except:
		return
def reply():
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return

	cur = conn.cursor()
	try:
		cur.execute('SELECT ques,reply FROM reports WHERE reportId=%s',(userId,))
		data = cur.fetchall()
		cur.close()
		conn.close()
		return data
	except:
		return
#==================================================Options=========================================
def showRooms():
	query = 'SELECT * FROM roomCategory'

	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return False

	cur = conn.cursor()
	try:
		cur.execute(query)
		rooms = cur.fetchall()
		for room in rooms:
			print('Room Type: ',room[1])
			print('Room Price(per Night): Rs.',room[2])
			print('Room Description: ',room[3])
			print('Votes: ',room[4])
			print('\n')
		print('\n')

		cur.close()
		conn.close()
	except:
		return False
def showReviews():
	query = 'SELECT name,custReview FROM customer,reviews WHERE customer.custId=reviews.custId'
	
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return False

	cur = conn.cursor()
	try:
		cur.execute(query)
		reviews = cur.fetchall()
		if not(bool(reviews)):
			print('\nNo Reviews Found\n')
			return
		print('\nCustomer Reviews\n\n')
		for review in reviews:
			print(review[0],review[1],sep='\n')
			print('\n')
		print('\n')
		cur.close()
		conn.close()
	except:
		return False
def showWallet():
	query = 'SELECT custCredit FROM credits WHERE userId=%s'
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return False

	cur = conn.cursor()
	try:
		cur.execute(query,(userId,))
		credits = cur.fetchone()
		print('Credit Balance: Rs.',credits[0])
		print('\n')

		cur.close()
		conn.close()
	except:
		return False
def listOfServices():
	query = 'SELECT serviceName,serviceCost FROM serviceCategory'
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return False

	cur = conn.cursor()
	tmpdict = {}
	try:
		cur.execute(query)
		for service in cur.fetchall():
			tmpdict[service[0]] = service[1]
			
		cur.close()
		conn.close()
		return tmpdict
	except:
		return False	
def listOfRooms():
	query = 'SELECT roomType,roomPrice FROM roomCategory'
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return False

	cur = conn.cursor()
	tmpdict = {}
	try:
		cur.execute(query)
		rooms = cur.fetchall()
		for room in rooms:
			tmpdict[room[0]] = room[1]

		cur.close()
		conn.close()
		return tmpdict
	except:
		return False
#===================================================My Activity=====================================
def myBills():
	query = 'SELECT billId,serviceCost,roomCost,type,name,phoneNo,checkIn,checkOut,roomsCount,roomInitial,roomFinal FROM bill,customer WHERE userId=%s and bill.billId=customer.custId'

	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return False

	cur = conn.cursor()
	try:
		cur.execute(query, (userId,))
		
		records = cur.fetchall()
		if not(bool(records)):
			print('\nYOU HAVE NO BILLS\n')
			return
		print("\nYour Bills\n")
		for record in records:
			print('\n')

			print('Bill Id: ',record[0],'\tAmount: ',record[1]+record[2],'\tTransaction Type: ',record[3])
			print('Customer Specifications: ')
			print('Name: ',record[4],'\tPhone: ',record[5])
			print('Check In: ',record[6],'\tCheck Out: ',record[7])
			print('Rooms Specifications: ')
			print('Rooms Count: ',record[8],'\tRooms Stayed: ',record[9],'-',record[10])
			print('\n')

		cur.close()
		conn.close()
	except:
		return False
def myReviews():
	query = 'SELECT reviews.custId,custReview FROM reviews,customer WHERE userId=%s and customer.custId=reviews.custId' 
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return False
	cur = conn.cursor()
	try:
	
		cur.execute(query, (userId,))
		reviews = cur.fetchall()
		if not(bool(reviews)):
			print('\nYOU HAVE NO REVIEWS')
			return

		print('\nYour Reviews')
		for review in reviews:
			print('\n')
			print(review[0],'. ',review[1])

		cur.close()
		conn.close()

		return
	except:
		return False
def refresh(cur,conn):
	#Removing old 
	
	cur.execute('SELECT roomInitial,roomsCount FROM customer WHERE checkOut<%s',(str(date.today()),))
	data = cur.fetchall()
	if data:
		for d in data:
			cur.execute('UPDATE roomDistribution SET availableRooms=availableRooms+%s WHERE %s<=roomFinal and %s>=roomInitial',(d[1], d[0], d[0]))
			conn.commit()
def refreshRemove(cur, conn):
	cur.execute('SELECT roomInitial,roomsCount FROM customer WHERE userId=%s',(userId, ))
	data = cur.fetchall()
	if data:
		for d in data:
			cur.execute('UPDATE roomDistribution SET availableRooms=availableRooms+%s WHERE %s<=roomFinal and %s>=roomInitial',(d[1], d[0], d[0]))
			conn.commit()
def bookNow(name,phoneNo,checkIn,checkOut,roomsCount,roomCost,serviceCost,btype,rtype):
	

	queries={
		'lastCustId': 'SELECT custId FROM customer ORDER BY custId DESC LIMIT 1',
		'balance': 'SELECT custCredit FROM credits WHERE userId=%s',
		'insertRecord': 'INSERT INTO customer VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
		'useCredits': 'UPDATE credits SET custCredit=custCredit-%s',
		'bill': 'INSERT INTO bill values(%s,%s,%s,%s)', 
		'roomDist': 'SELECT roomFinal,availableRooms FROM roomDistribution,roomCategory WHERE roomDistribution.roomId=roomCategory.roomId and roomType=%s',		
		'roomUpdate':'UPDATE roomDistribution SET availableRooms=availableRooms-%s WHERE roomId=(SELECT roomId from roomCategory WHERE roomType=%s)'}

	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		print("Check Your Internet Connection")
		return
	try:
		cur = conn.cursor()
		refresh(cur, conn)

		#Fetching the lastCustId
		global lastCustId
		cur.execute(queries['lastCustId'])
		try:
			lastCustId = cur.fetchone()[0]+1
		except:
			lastCustId = 1
		
		cur.execute(queries['balance'],(userId,))
		if cur.fetchone()[0]<(roomCost+serviceCost):
			print("Insufficient Balance")
			return
		
		cur.execute(queries['roomDist'],(rtype,))
		roomDist = cur.fetchone()
		if roomsCount > roomDist[-1]:
			print(f"Sorry Can't book now {roomDist[-1]} rooms are available")
			return
			
		roomInitial = (roomDist[0]- roomDist[-1])+1
			
		cur.execute(queries['insertRecord'],(lastCustId, userId, name, roomInitial,roomInitial+roomsCount-1, phoneNo, checkIn, checkOut, roomsCount))
		#Inserting the customer
		cur.execute(queries["useCredits"],((serviceCost+roomCost),))#Using the Credits
		cur.execute(queries['roomUpdate'],(roomsCount,rtype))
		cur.execute(queries['bill'],(lastCustId,btype,serviceCost,roomCost))#bill entry
		
		global roomType
		roomType = rtype
		conn.commit()
		cur.close()
		conn.close()
		return True
	except:
		print("Check Your Internet Connection")
		return		
def reviewRate(review,vote):
	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return False
	try:
		cur = conn.cursor()
		cur.execute('INSERT INTO reviews values(%s,%s)',(lastCustId,review))
		if vote:
			cur.execute('UPDATE roomCategory SET vote=vote+1 WHERE roomType=%s',(roomType,))

		conn.commit()
		cur.close()
		conn.close()

		return True

	except:
		return False		
#==================================================SignUp/Login======================================
def signup(email,password,salt):

	queries = {
		'lastId': 'SELECT userId FROM userLogin ORDER BY userId DESC LIMIT 1',
		'insertRecord': 'INSERT INTO userLogin VALUES(%s,%s,%s,%s)',
		'insertCredit': 'INSERT INTO credits VALUES(%s,%s)'
		}
	

	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return

	try:
		cur = conn.cursor()
		#Fetching the lastId
		cur.execute(queries['lastId'])
		try:
			lastId = cur.fetchone()[0]+1
		except:
			lastId = 1

		hashPassword,salt = hashPasswd(password)
		#Inserting the record
		cur.execute(queries['insertRecord'],(lastId,email,hashPassword,salt))
		cur.execute(queries['insertCredit'],(lastId,10000))

		conn.commit()
		cur.close()	
		conn.close()
		return True
	except:
		return		
def login(email,passwd):
	query = 'SELECT * FROM userLogin WHERE email = %s'

	try:
		conn = connect(host=authHost,user=authUser,passwd=authPasswd,database=authDb)
	except:
		return

	try:
		cur = conn.cursor()

		#Validating Record

		cur.execute(query,(email,))
		record = cur.fetchone()

		
		if bool(record) and (hashPasswdCheck(passwd,record[3]) == record[2]):
			cur.close()	
			conn.close()

			global userId
			userId = record[0]
			return True,record[0]
		else:
			return False

	except:
		return

		