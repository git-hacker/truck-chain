'''
usage           : python InsuranceNode.py (port - 8089)
'''


from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
from flask import Flask, jsonify, request, render_template
import sqlite3
#from flaskext.mysql import MySQL


class Transaction:

	def connect():
		conn = sqlite3.connect("BucketList.db")
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS blockchain (id INTEGER PRIMARY KEY, senAdd text, senPriv text, reciAdd text, insurance_value integer)")
		conn.commit()
		conn.close()

	def __init__(self, insurance_identifier, insurance_private_key, insurance_receiver, insured_good, insurance_value): #These attributes are need by the sender to create a transaction.
		self.insurance_identifier = insurance_identifier
		self.insurance_private_key = insurance_private_key
		self.insurance_receiver = insurance_receiver
		self.insured_good = insured_good
		self.insurance_value = insurance_value

	def __getattr__(self, attr):
		return self.data[attr]

	def to_dict(self): #returns transaction information
		return OrderedDict({'insurance_identifier': self.insurance_identifier,
							'insurance_receiver': self.insurance_receiver,
							'insured_good':self.insured_good,
							'insurance_value': self.insurance_value})

	def sign_transaction(self):
		"""
		Sign transaction with private key
		"""
		private_key = RSA.importKey(binascii.unhexlify(self.insurance_private_key))
		signer = PKCS1_v1_5.new(private_key)
		h = SHA.new(str(self.to_dict()).encode('utf8'))
		return binascii.hexlify(signer.sign(h)).decode('ascii')

	def insert(insurance_identifier, insurance_private_key, insurance_receiver, insured_good,insurance_value):
		conn = sqlite3.connect("BucketList.db")
		cur = conn.cursor()
		cur.execute("INSERT INTO blockchain insurance_valueS (NULL, ?, ?, ?, ?)", (insurance_identifier, insurance_private_key, insurance_receiver, insured_good,insurance_value))
		conn.commit()
		conn.close()

	connect()



app = Flask(__name__)

'''
# DB

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MySQL_Server123'
app.config['MYSQL_DB'] = 'BucketList'

mysql = MySQL(app)

# End of DB
'''



@app.route('/')
def index():
	return render_template('./index.html')

@app.route('/make/transaction')
def make_transaction():
	return render_template('./make_transaction.html')

@app.route('/view/transactions')
def view_transaction():
	return render_template('./view_transactions.html')

@app.route('/wallet/new', methods=['GET'])
def new_wallet():
	random_gen = Crypto.Random.new().read
	private_key = RSA.generate(1024, random_gen)
	public_key = private_key.publickey()
	response = {
		'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
		'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
	}

	return jsonify(response), 200

@app.route('/generate/transaction', methods=['POST'])
def generate_transaction():

	insurance_identifier = request.form['insurance_identifier']
	insurance_private_key = request.form['insurance_private_key']
	insurance_receiver = request.form['insurance_receiver']
	insured_good = request.form['insured_good']
	insurance_value = request.form['amount']

	transaction = Transaction(insurance_identifier, insurance_private_key, insurance_receiver, insured_good, insurance_value)
	#cur = mysql.connect().cursor()
	#cur.execute("INSERT INTO blockchain insurance_valueS (?,?,?,?)",(insurance_identifier, insurance_private_key, insurance_receiver, insurance_value))
	#Transaction.insert(insurance_identifier, insurance_private_key, insurance_receiver, insurance_value)


	response = {'transaction': transaction.to_dict(), 'signature': transaction.sign_transaction()}

	return jsonify(response), 200


if __name__ == '__main__':
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('-p', '--port', default=8089, type=int, help='port to listen on')
	args = parser.parse_args()
	port = args.port

	app.run(host='127.0.0.1', port=port, debug = True)
