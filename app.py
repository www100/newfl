##############################################################
#           CLASSES
##############################################################
from app_classes import *

##############################################################
#           VIRTUAL ENVIRONMENT
##############################################################
import os, subprocess, json

# define virtual environment and start using a bat file
#dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\'
#startenv_filename = "startvenv.bat"
#subprocess.call([rf'{dir_path}{startenv_filename}'])


##############################################################
#           FLASK
##############################################################
from flask import Flask, session,redirect, render_template, jsonify, request, url_for

# define flask app
app = Flask(__name__)

##############################################################
#           DATABASE
##############################################################
import psycopg2
import psycopg2.extras
from app_db import *
#Establishing the connection
db_connect = psycopg2.connect(
   database=dbname, user=dbuser, password=dbpass, host=dbhost, port= ''
)
#Creating a cursor object using the cursor() method
cursor = db_connect.cursor()

#Doping EMPLOYEE table if already exists.
cursor.execute("DROP TABLE IF EXISTS CLIENT")

#Creating table as per requirement
sql ='''
CREATE TABLE
client (
	id serial PRIMARY KEY,
	name VARCHAR ( 100 ) NOT NULL,
	email VARCHAR ( 100 ) UNIQUE,
	telephone VARCHAR ( 100 ) NOT NULL,
	address VARCHAR ( 100 ) NOT NULL,
	leaving VARCHAR ( 100 ) NOT NULL,
	arriving VARCHAR ( 100 ) NOT NULL,
	dateleaving VARCHAR ( 100 ) NOT NULL,
	datearriving VARCHAR ( 100 ) NOT NULL,
	flexible VARCHAR ( 100 ) NOT NULL,	
	connections VARCHAR ( 100 ) NOT NULL,
	bags VARCHAR ( 100 ) NOT NULL,
	insurance VARCHAR ( 100 ) NOT NULL,
	totalprice VARCHAR ( 100 ) NOT NULL,
	totalpaid VARCHAR ( 100 ) NOT NULL,
	paymentstatus VARCHAR ( 100 ) NOT NULL
)
'''
cursor.execute(sql)
print("Table created successfully........")


sql = '''
INSERT INTO
client(name, email, telephone, address, leaving, arriving, dateleaving, datearriving, flexible, connections, bags, insurance, totalprice, totalpaid, paymentstatus)
VALUES
	('Tiger Wood','rpd096709@uniaotrafego.com','1231231231231','','','','','','','','','','10000','',''),
	('Mark Oto Ednalan','titoon@crossfitcoastal.com','24112412411424124','','','','','','','','','','20000','',''),
	('Jacob thompson','duane4180@rackabzar.com','12313212312323','','','','','','','','','','12312','',''),
	('cylde Ednalan','kjhgfd@wuupr.com','1234551512','','','','','','','','','','24214','',''),
	('Rhona Davidson','jose213v18@dmxs8.com','545352352354','','','','','','','','','','13123','',''),
	('Quinn Flynn','apclark@kenvanharen.com','123124352235','','','','','','','','','','42141','',''),
	('Tiger Nixon','joha1207@uniaotrafego.com','123564745745','','','','','','','','','','12331','',''),
	('Airi Satou','mats1996@sahabatasas.com','1243523532523','','','','','','','','','','5213','',''),
	('Angelica Ramos','sdwoody@casanovalar.com','214124124124','','','','','','','','','','3214','',''),
	('Ashton updated','dreamhot11@adsensekorea.com','2464364634634','','','','','','','','','','4213','',''),
	('Bradley Greer','ulakoshelaeva@naverapp.com','21412412412','','','','','','','','','','3123','',''),
	('Brenden Wagner','samerelhimani@pianoxltd.com','1231231551515','','','','','','','','','','2121','',''),
	('Brielle Williamson','putinrussia77@digimexplus.com','12312312455','','','','','','','','','','1232','',''),
	('Bruno Nash','jenchikfef@whymustyarz.com','12312312552121','','','','','','','','','','32131','',''),
	('cairocoders','dzynspb@vspiderf.com','2131241251251','','','','','','','','','','3214','',''),
	('Zorita Serrano','adriane@badaxitem.host','1231241521251','','','','','','','','','','4123','',''),
	('Zenaida Frank','holgateyoung@chantellegribbon.com','12412412412412','','','','','','','','','','12324','',''),
	('Sakura Yamamoto','crutches13@arshopshop.xyz','21312521512','','','','','','','','','','5212','',''),
	('Serge Baldwin','furnok316@netmon.ir','2141242141414','','','','','','','','','','5213','',''),
	('Shad Decker','rostislavgogol@badaxitem.host','12412412412521','','','','','','','','','','6412','','');
'''
cursor.execute(sql)
print("Executed successfully........")
cursor.execute(""" SELECT * FROM client LIMIT 1000000 """)
data = cursor.fetchall()
print('\n'.join(str(e) for e in data)) 

db_connect.commit()



##############################################################
#           STRIPE
##############################################################
import stripe

# define stripe api keys.
stripe_sk = 'sk_test_51LvT0PAe4l2zMN3LVsDeUG5l7CyCHCjFnjf9Z8dD8IqUXeVHFw4vlg4DTE811M3bjyn7FL8vZdSw7Cvfmo2E7zek00enwYiTuO'
stripe_pk = 'pk_test_51LvT0PAe4l2zMN3LfO9dK28m2XtNPaOOrkOIZARCLz1M16WpFzsYwJarGUBbNQ2MYPbtPoWPdrqPWaKAZXltVZGU00K6qPjnMG'
stripe_wh = 'whsec_Mnci6T2VIO4Rw29amsEZ5tbQXjI15stb'
# define server apikey
stripe.api_key = stripe_sk



##############################################################
#           ROUTES
##############################################################
@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')

@app.route('/add-to-db', methods=['GET', 'POST'])
def add_to_db():
  return render_template('db.html')

@app.route("/ajaxlivesearch",methods=["POST","GET"])
def ajaxlivesearch():
    cur = db_connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        search_word = request.form['query']
        print(search_word)
        if search_word == '':
            query = "SELECT * from client ORDER BY id"
            cur.execute(query)
            c_client = cur.fetchall()
        else:    
            cur.execute('SELECT * FROM client WHERE UPPER(name) LIKE UPPER(%(name)s)',{ 'name': '{}%'.format(search_word)})
            numrows = int(cur.rowcount)
            c_client = cur.fetchall()
            print(numrows)
    return jsonify({'htmlresponse': render_template('response.html', client=c_client, numrows=numrows)})


@app.route('/pay/<int:value>', methods=['GET', 'POST'])
def pay(value):
  intent = stripe.PaymentIntent.create(
    amount=value * 100,
    currency="brl",
    payment_method_types=['card', 'boleto'],
    payment_method_options={
      'boleto' : {
        'expires_after_days': 1
      }
    },
  )
  return render_template('checkout.html', CLIENT_SECRET=intent.client_secret, STRIPE_PKEY=stripe_pk)

@app.route('/cotação/<int:value>/<string:description>', methods=['GET', 'POST'])
def cotação_total(value,description):
  session = stripe.checkout.Session.create(
    line_items=[{
      'price_data': {
        'currency': 'brl',
        'unit_amount': value * 100,
        'product_data': {
          'name': 'A sua cotação para '+description+' falta um pagamento de',
          "images": ["https://www100.github.io/sisviagens/assets/img/Logo.png"],
        },
      },
      'quantity': 1,
    }],
    locale = 'pt-BR',
    payment_method_types=['card', 'boleto'],
    payment_method_options={
      'boleto' : {
        'expires_after_days': 7
      }
    },
    mode='payment',
    success_url='https://example.com/success',
    cancel_url='https://example.com/cancel',
  )
  return redirect(session.url, code=303)


@app.route('/cotação/<int:value>/<int:months>', methods=['GET', 'POST'])
def cotação_months(value,months):
  session = stripe.checkout.Session.create(
    line_items=[{
      'price_data': {
        'currency': 'brl',
        'unit_amount': int(((value / months) * 100)*1.15),
        'recurring' : {'interval': 'month',
                       'interval_count': 1,},
        'product_data': {
          'name': ' e pagar facílmente com SIS Viagens. A sua cotação de '+str("R${:,.2f}".format(value))+' parcelada pela '+str(months)+' meses incluindo juros de 15% fica',
          "images": ["https://www100.github.io/sisviagens/assets/img/Logo.png"],
        },
      },
      'quantity': 1,
    }],
    locale = 'pt-BR',
    payment_method_types=['card', 'boleto'],
    payment_method_options={
      'boleto' : {
        'expires_after_days': 7
      }
    },
    mode='subscription',
    success_url='https://example.com/success',
    cancel_url='https://example.com/cancel',
  )
  return redirect(session.url, code=303)

@app.route('/get-customer/<string:sessionid>', methods=['GET', 'POST'])
def add_SubscriptionShcedule(sessionid):
  session = stripe.checkout.Session.retrieve(sessionid)
  schedule = stripe.SubscriptionSchedule.create(
  customer=session.customer,
  start_date='now',
  end_behavior='cancel',
  phases=[
    {
      'items': [
        {
          'price': session.price,
          'quantity': 1,
        },
      ],
      'iterations': 6,
    },
  ],
  )
  return redirect(schedule.url, code=303)

@app.route('/webhook/boleto', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_wh
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e
      
    # Handle the event
    if event['type'] == 'payment_intent.canceled':
      payment_intent = event['data']['object']
    elif event['type'] == 'payment_intent.created':
      payment_intent = event['data']['object']
    elif event['type'] == 'payment_intent.partially_funded':
      payment_intent = event['data']['object']
    elif event['type'] == 'payment_intent.payment_failed':
      payment_intent = event['data']['object']
    elif event['type'] == 'payment_intent.processing':
      payment_intent = event['data']['object']
    elif event['type'] == 'payment_intent.requires_action':
      payment_intent = event['data']['object']
    elif event['type'] == 'payment_intent.succeeded':
      payment_intent = event['data']['object']
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)

##############################################################
#           SERVER
##############################################################
if __name__== '__main__':
  # 1 = liveserver, else define as flask server
  x = 0
  if x == 1:
    # define as liveserver
    from livereload import Server
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    server = Server(app.wsgi_app)
    server.serve(port=5000, host='127.0.0.1')
  else:
    # define as flask server
    app.run(host="0.0.0.0", port=5000, debug = False)