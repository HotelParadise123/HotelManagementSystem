from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from email_validator import validate_email, EmailNotValidError
from prompt_toolkit.validation import Validator, ValidationError
from re import search, match
import requests
import sqlmain
from socket import gethostbyname,gethostname
from datetime import date
from random import randint
import mail

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#7ecc54 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


#=====================Validators=======================================
class confirmPassword(Validator):
    def validate(self, document):
        if not(document.text == password):
            raise ValidationError(
                message="Password doesn't match",
                cursor_position=len(document.text))
class validateEmail(Validator):
    def validate(self, document):
        regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        exist = sqlmain.checkExistence(document.text)
        if exist == None:
            raise ValidationError(
                message="NO INTERNET CONNECTION",
                cursor_position=len(document.text))
        elif exist:
            raise ValidationError(
                message="Already Exists",
                cursor_position=len(document.text))

        if(search(regex,document.text)):
            api_key = '8fd9cca5-1a40-4215-8206-73185444da4b'
            try:
                response = requests.get("https://isitarealemail.com/api/email/validate",params = {'email': document.text},headers = {'Authorization': "Bearer " + api_key })
            except:
                raise ValidationError(
                message="NO INTERNET CONNECTION",
                cursor_position=len(document.text))

            if response.json()['status'] == "valid":
                del regex,response,api_key
                return sendOtp(document.text)
            else:
                raise ValidationError(
                message="Invalid Gmail ID",
                cursor_position=len(document.text))
        else:
            raise ValidationError(
                message="Invalid Gmail ID",
                cursor_position=len(document.text))
class validateLogin(Validator):
    def validate(self, document):
        regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if not(search(regex,document.text)):
            raise ValidationError(
                message="Invalid Gmail ID",
                cursor_position=len(document.text))    
class greaterThanToday(Validator):
    def validate(self, document):
        if (match('^20[0-2][0-9]-((0[1-9])|(1[0-2]))-([0-2][1-9]|3[0-1])$',document.text)) and document.text>=str(date.today()):
            global checked
            checked=document.text
        else:
            raise ValidationError(
                message="Date doesn't exist after",
                cursor_position=len(document.text))    
class checkOut(Validator):
    def validate(self, document):
        if (match('^20[0-2][0-9]-((0[1-9])|(1[0-2]))-([0-2][1-9]|3[0-1])$',document.text)) and document.text>=checked:
            pass
        else:
            raise ValidationError(
                message="Check Out date before Check In Date",
                cursor_position=len(document.text)) 
class phoneValidator(Validator):
    def validate(self, document):
        if match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text) and (len(document.text)==10): pass
        else:
            raise ValidationError(
                message="Invalid Phone Number",
                cursor_position=len(document.text))    

def checkConnection():
    if gethostbyname(gethostname()) == "127.0.0.1":
        promptTryExit()
        
    else: promptSignInSignUp()
def sendOtp(email):
    otpGen = randint(100000,999999)
    print('\nSending Verification mail')
    sent = mail.sendOtp(otpGen, email)
    if sent:
        print("To continue, first verify it's you - An otp has been sent to your gmail\n")
        answer = prompt([{
            'type': 'input',
            'name': 'Otp',
            'message': 'EnterOtp: ',
            'validate': lambda otp: True if (otp.isdigit() and len(otp)==6) else False
            }],style=style)

        if int(answer['Otp'])==otpGen:            
            return True
        else:
            print('\nInvalid Otp\n')
            promptSignInSignUp()
    else: 
        print('\nVerification was not completed!!!')
        promptSignInSignUp()
def checkpass(passwd):
    global password
    if len(passwd)>=8:
        password = passwd
        return True
    else: return False
def promptTryExit():
    print('\n\n')
    questions = [
    {
        'type': 'list',
        'name': 'tryExit',
        'message': 'NO INTERNET CONNECTION',
        'choices': [
            'Try Again',
            'Exit',
            ]
    }]
    answers = prompt(questions, style=style)

    if answers['tryExit'] == 'Exit':
        quit()
    elif answers['tryExit'] == 'Try Again':
        if gethostbyname(gethostname()) == "127.0.0.1":
            promptTryExit()

        else: promptSignInSignUp()
def promptLogin():
    print('\n\n')
    print('LOGIN')

    questions = [
    {
        'type': 'input',
        'name': 'email',
        'message': 'EmailId: ',
        'validate': validateLogin
    },
    {
        'type': 'password',
        'name': 'passwd',
        'message': 'Password:',
        'validate': lambda passwd: True if len(passwd)>=8 else False

    }
    ]
    answers = prompt(questions, style=style)
    #SQL goes here
    boolId = sqlmain.login(answers.get('email'),answers.get('passwd'))

    if boolId == None:
        print("NO INTERNET CONNECTION")
        promptSignInSignUp()
    elif boolId == False:
        print("Invalid Username or Password")
        promptSignInSignUp()
    else:
        global userId
        userId = boolId[1]
        print('Successfully Logged In')
        promptOptions()
def promptSignUp():
    print('\n\n')
    print('SIGNUP')


    questions = [
    {
        'type': 'input',
        'name': 'email',
        'message': 'EmailId: ',
        'validate': validateEmail
    },
    {
        'type': 'password',
        'name': 'passwd',
        'message': 'Password:',
        'validate': lambda passwd: checkpass(passwd)

    },
    {
        'type': 'password',
        'name': 'confirmPasswd',
        'message': 'Confirm Password: ',
        'validate': confirmPassword
    },
    {
        'type': 'confirm',
        'message': 'Do you want to continue?',
        'name': 'continue',
        'default': True,
    }
    ]
    answers = prompt(questions, style=style)
    if answers['continue'] == False:
        promptSignInSignUp()
    else:
        if (sqlmain.signup(answers.get('email'),answers.get('passwd'),answers.get('confirmPasswd'))):
            print('Successfully Signed Up(Please Login to continue)')
            mail.sendWelcome(answers.get('email'),answers.get('passwd'))
            promptLogin()
        else:
            print("NO INTERNET CONNECTION")
            promptSignInSignUp()
def promptSignInSignUp():
    print('\n\n')
  
    questions = [
    {
        'type': 'list',
        'name': 'signinup', 
        'message': 'LOGIN/SIGNUP',
        'choices': [
            'Login In',
            'Sign Up',
            'Exit'
            ]
    }]

    answers = prompt(questions, style=style)
    
    if answers['signinup'] == 'Exit':
        quit()
    elif answers['signinup'] == 'Sign Up':
        promptSignUp()

    elif answers['signinup'] == 'Login In':
        promptLogin()

#=====================================================Logged IN==========================================
def homeExit(tmp):
    if tmp == None:
        questions = [
        {
            'type': 'list',
            'name': 'homeExit',
            'message': 'RETURN',
            'choices': [
                'Home',
                'Exit',
                ]
        }]

        answers = prompt(questions, style=style)
        if answers['homeExit']=='Home':
            promptOptions()
        elif answers['homeExit']=='Exit':
            quit()
    else:
        print("\nCouldn't Load Results--Redirecting Back to Home--")
        promptOptions()
def listOfRooms():
    tmplist=[]
    #SQL goes here
    global rooms
    rooms = sqlmain.listOfRooms()
    if  rooms== False:
        print("\nCouldn't Connect--Check Your INTERNET CONNECTION")
        promptOptions()
        return
    tmplist = [x+'    Rs.'+str(rooms[x]) for x in rooms]
    return tmplist
def listOfServices():
    tmplist=[]
    #SQL goes here
    global services
    services = sqlmain.listOfServices()
    if services == False:
        print("\nCouldn't Connect--Check Your INTERNET CONNECTION")
        promptOptions()
        return
    tmplist = [{'name':x+('    Rs.'+str(services[x]))} for x in services]
    return tmplist
def promptMyActivity():
    print('\n\n')

    questions = [
    {
        'type': 'list',
        'name': 'myActivity',
        'message': '\nMY ACTIVITY\n',
        'choices': [
            'My Bills',
            'My Reviews',
            'My Queries',
            'Home',
            'Exit'
            ]
    }
    ]

    answers = prompt(questions, style=style)

    if answers['myActivity'] == 'Exit':
        quit()

    elif answers['myActivity'] == 'Home':
        promptOptions()

    elif answers['myActivity'] == 'My Bills':
        print('\n\n')
        tmp = sqlmain.myBills()
        homeExit(tmp)

    elif answers['myActivity'] == 'My Reviews':
        print('\n\n')
        tmp = sqlmain.myReviews()
        homeExit(tmp)
    elif answers['myActivity'] == 'My Queries':
        print('\n')
        qreply = sqlmain.reply()
        if qreply==None:
            print('Check Your Internet Connection')
            promptOptions()
        else:
            if bool(qreply):
                for qr in qreply:
                    print('Question: ',qr[0],'\nReply: ',qr[1])
                    print('\n')
                print('\n')
                homeExit(None)
            else:
                print('You have no queries\n')
                promptOptions()
def promptSettings():
    questions = [
    {
        'type': 'list',
        'name': 'settingType',
        'message': '\nSETTINGS\n',
        'choices': [
        'Change Password',
        'Delete My Account',
        'Home',
        'Exit']
    }
    ]
    answers = prompt(questions,style=style)
    if answers['settingType']=='Change Password':
        questions = [
        {
            'type': 'password',
            'name': 'oldPasswd',
            'message': 'Old Password',
            'validate': lambda oldPasswd: True if len(oldPasswd)>=8 else False

        },
        {
            'type': 'password',
            'name': 'newPasswd',
            'message': 'New Password',
            'validate': lambda passwd: checkpass(passwd)

        },
        {
            'type': 'password',
            'name': 'confirmNewPasswd',
            'message': 'Confirm New Password',
            'validate': lambda newPasswd: newPasswd == password
        },
        {
            'type': 'confirm',
            'message': 'Do you want to continue?',
            'name': 'continue',
            'default': True,
        }
        ]
        answers = prompt(questions,style=style)
        if answers['continue']==False:
            promptSettings()
        else:
            #SQL goes here
            booltmp = sqlmain.changePasswd(answers['oldPasswd'],answers['newPasswd'])
            if booltmp:
                print('Password Successfully Changed--Please Login Again to Continue')
                promptLogin()
            else:
                print('Invalid Password or Internet Connection Problem')
                promptSettings()

    elif answers['settingType']=='Delete My Account':

        questions = [
        {
            'type': 'password',
            'name': 'passwd',
            'message': 'Password',
            'validate': lambda passwd: True if len(passwd)>=8 else True

        },
        {
            'type': 'confirm',
            'message': 'Do you want to continue?',
            'name': 'continue',
            'default': True,
        }
        ]
        answers = prompt(questions,style=style)
        if answers['continue']==False:
            promptSettings()
        else:
            #SQL goes here
            booltmp = sqlmain.deleteAccount(answers['passwd'])
            if booltmp:
                print('Successfully Deleted Your Account')
                promptSignInSignUp()
            else:
                print('Invalid Password or Internet Connection Problem')
                promptSettings()

    elif answers['settingType']=='Exit':
        quit()
    elif answers['settingType']=='Home':
        promptOptions()
def promptBookNow():
    print('\n')

    questions = [
    {
        'type': 'input',
        'name': 'name',
        'message': 'Name',
        'validate':lambda name: True if len(name)>=0 else False

    },
    {
        'type': 'input',
        'name': 'phone',
        'message': 'Phone No.',
        'validate': phoneValidator

    },
    {
        'type': 'input',
        'name': 'checkIn',
        'message': 'Check In Date(YYYY-MM-DD)',
        'validate': greaterThanToday

    },
    {
        'type': 'input',
        'name': 'checkOut',
        'message': 'Check Out Date(YYYY-MM-DD)',
        'validate': checkOut

    },
    {
        'type': 'list',
        'name': 'roomType',
        'message': '\nSelect Room\n',
        'choices': listOfRooms()
    },
    {
        'type': 'input',
        'name': 'rooms',
        'message': 'Number of Rooms',
        'validate': lambda roomsCount: True if (roomsCount.isdigit() and int(roomsCount)<=50) else False

    },
    {
        'type': 'checkbox',
        'qmark': '?',
        'message': 'Select Services',
        'name': 'services',
        'choices': listOfServices(),
    },
    {
        'type': 'list',
        'name': 'paymentMethod',
        'message': '\nPayment Method\n',
        'choices': [
        'Credits',
        {
            'name': 'Online Banking',
            'disabled': 'Unavailable'
        },
        {
            'name': 'Credit Card',
            'disabled': 'Unavailable'
        }
        ]
    },
    {
        'type': 'confirm',
        'message': 'Do you want to continue?',
        'name': 'continue',
        'default': True,
    }

    ]
    answers = prompt(questions, style=style)

    tmp = answers['roomType'].find(' ')
    inTmp = answers['checkIn'].split('-')
    ouTmp = answers['checkOut'].split('-')
    days = (((date(int(ouTmp[0]),int(ouTmp[1]),int(ouTmp[2])))-(date(int(inTmp[0]),int(inTmp[1]),int(inTmp[2])))).days)+1
    


    if answers['continue']==False:
        promptOptions()
    else:
    	rtmp = answers['roomType'].find('Rs.')+3
    	roomCost = int(answers['roomType'][rtmp:])*int(answers['rooms'])*days
    	serviceCost = 0
    	if bool(answers['services']):
    	   	for x in answers['services']:
    	   		stmp = (x.find(' '))
    	   		serviceCost += int(services.get(x[:stmp]))*int(answers['rooms'])*days
    	else:
    		serviceCost=0
    	booltmp = sqlmain.bookNow(answers['name'],int(answers['phone']),answers['checkIn'],answers['checkOut'],int(answers['rooms']),roomCost,serviceCost,answers['paymentMethod'],answers['roomType'][:tmp])

    	if booltmp==None:
            promptOptions()
    	elif booltmp==True:
    		print('\n')
    		print('Successfully Booked')
	    	print('Bill Amount: ',serviceCost+roomCost)
	    	print('\n')
	    	questions = [
	    	{
                'type': 'confirm',
                'message': 'Do you liked the room?',
                'name': 'vote',
                'default': True
            },
    		{
    	    	'type':'input',
    	    	'name':'review',
    	    	'message':'Write a review',
    	    	'validate': lambda rev: True if len(rev)>0 else False
	    	}]
	    	answers = prompt(questions,style=style)
	    	booltmp = sqlmain.reviewRate(answers['review'],answers['vote'])
	    	if booltmp==False:
	    		print('Couldnt Add Reviews-Poor Network Connection')
	    	else:
	    		print('\nReviews Added')
	    	promptOptions()
def promptOptions():
    print('\n\n')
    questions = [
    {
        'type': 'list',
        'name': 'options',
        'message': 'HOME',
        'choices': [
            'Book Now',
            'Wallet',
            'Earn Credits',
            'Reviews',
            'View Rooms',
            'My Actvity',
            'Help',
            'Report(Ask)',
            'Settings',
            'Exit'
            ]
    }]

    answers = prompt(questions, style=style)
    if answers['options']=='Exit':
        quit()
    elif answers['options']=='Book Now':
        promptBookNow()
    elif answers['options']=='Wallet':
        print('\n')
        tmp = sqlmain.showWallet()
        homeExit(tmp)
    elif answers['options']=='Reviews':
        print('\n')
        tmp = sqlmain.showReviews()
        homeExit(tmp)
    elif answers['options']=='View Rooms':
        print('\n')
        tmp = sqlmain.showRooms()
        homeExit(tmp)
    elif answers['options']=='Settings':
        promptSettings()
    elif answers['options']=='My Actvity':
        promptMyActivity()
    elif answers['options']=='Earn Credits':
        interests = sqlmain.selectQuiz()
        
        if interests==None:
            print("Check Your Internet Connection")
            promptOptions()
        else:
            print('\n')
            question = [
            {
                'type': 'list',
                'name': 'interest',
                'message': 'What is your Interest?',
                'choices': interests
            }]
            answer = prompt(question, style=style)
            earn = sqlmain.earnCredit(answer['interest'])

            if earn==None:
                print("\nCheck Your Internet Connection")
                promptOptions()   
            else:
                print('\n')
                answers = prompt(earn[0], style=style)
                #Fetching Scores
                print('\nProcessing Credits...')
                tmpScore=0
                for a in answers:
                    if answers.get(a)==earn[1].get(a)[-1]:
                        tmpScore+=100
                booltmp = sqlmain.addCredit(tmpScore)
                if booltmp==None:
                    print('\nCheck Your Internet Connection')
                    promptOptions()
                else:
                    print('You earned: ',tmpScore)
                    print('Check Your available balance in Wallet\n')
                    promptOptions()
    elif answers['options']=='Help':
        print("\n")
        helpChoice = sqlmain.help()
        if helpChoice==None:
            print('Check Your Internet Connection')
            promptOptions()
        else:
            questions = [
            {
                'type': 'list',
                'name': 'help',
                'message': 'What do you want to know?',
                'choices': helpChoice+['Frequently Asked Questions']
            }]
            answer=prompt(questions, style=style)
            if answer['help']=='Frequently Asked Questions':
                frq = sqlmain.frq()
                if frq==None:
                    print('Check Your Internet Connection\n')
                    promptOptions()
                else:
                    print('\n')
                    if not(bool(frq)):
                        print('No queries till now!\n')
                        promptOptions()

                    else:
                        for qr in frq:
                            print('Question: ',qr[0],'\nReply: ',qr[1])
                            print('\n')
                        print('\n')
                        homeExit(None)
            else:
                helpType = sqlmain.helpType(answer['help'])
                if helpType==None:
                    print('Check Your Internet Connection\n')
                    promptOptions()
                else:
                    print('Description:')
                    print(helpType,'\n')
                    homeExit(None)

    elif answers['options']=='Report(Ask)':
        print('\n\n')
        questions = [
        {
            'type': 'input',
            'name': 'question',
            'message': 'Ask Your Query?\n',
            'validate': lambda q: True if len(q)!=0 else False
        },
        {
            'type': 'confirm',
            'name': 'confirm',
            'message': 'Do you want to Continue?',
            'default': True
        }]

        answers =prompt(questions, style=style)
        if answers['confirm']==False:
            print('\nNo Response Submitted!')
            promptOptions()
        else:
            booltmp = sqlmain.report(answers['question'])
            if booltmp==None:
                print('Check Your Internet Connection\n')
                promptOptions()
            else:
                print('\nWe will get in touch with you later!')
                print('Please check your report in My Activity Section next time you Login In\n')
                promptOptions()

#___main___
print("==PARADISE==\n")
checkConnection()
