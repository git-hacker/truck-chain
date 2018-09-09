'''
usage           : python AdminClient.py (port - 8088)
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
import hashlib


class Transaction:

	def connect():
		conn = sqlite3.connect("Admin.db")
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS blockchain_admin (id INTEGER PRIMARY KEY, ADMIN_IDENTIFIER text, DRIVER_IDENTIFIER text, GOOD text, QUANTITY integer, DESTINATION text)")
		conn.commit()
		conn.close()

	def __init__(self, admin_identifier, admin_private_key, driver_id, good, destination, quantity): #These attributes are need by the sender to create a transaction.
		self.admin_identifier = admin_identifier
		self.admin_private_key = admin_private_key
		self.driver_id = driver_id
		self.good = good
		self.destination = destination
		self.quantity = quantity



	def __getattr__(self, attr):
		return self.data[attr]

	def admin_dict(self): #returns transaction information
		return OrderedDict({'admin_identifier': self.admin_identifier,
							'driver_id': self.driver_id,
							'good':self.good,
							'destination': self.destination,
							'quantity': self.quantity})

	def sign_transaction(self):
		"""
		Sign transaction with private key
		"""
		private_key = RSA.importKey(binascii.unhexlify(self.admin_private_key))
		signer = PKCS1_v1_5.new(private_key)
		h = SHA.new(str(self.admin_dict()).encode('utf8'))
		return binascii.hexlify(signer.sign(h)).decode('ascii')

	def t_hash(self, add_dict):
		tx_list = list(add_dict.values())
		tx_string = "".join(str(x) for x in tx_list)
		tx_hash = hashlib.sha256(tx_string.encode('utf-8'))
		hash_digest = tx_hash.hexdigest()
		return hash_digest

	def insert(ADMIN_IDENTIFIER, DRIVER_IDENTIFIER, GOOD, QUANTITY, DESTINATION):
		conn = sqlite3.connect("Admin.db")
		cur = conn.cursor()
		cur.execute("INSERT INTO blockchain_admin VALUES (NULL, ?, ?, ?, ?, ?)", (ADMIN_IDENTIFIER, DRIVER_IDENTIFIER, GOOD, QUANTITY, DESTINATION))
		conn.commit()
		conn.close()

	connect()



app = Flask(__name__)





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

	admin_identifier = request.form['admin_identifier']
	admin_private_key = request.form['admin_private_key']
	driver_id = request.form['driver_id']
	good = request.form['good']
	destination = request.form['destination']
	quantity = request.form['quantity']

	transaction = Transaction(admin_identifier, admin_private_key, driver_id, good, destination,  quantity)
	#cur = mysql.connect().cursor()
	#cur.execute("INSERT INTO blockchain insurance_valueS (?,?,?,?)",(admin_identifier, admin_private_key, admin_id, quantity))
	#transaction.insert(ADMIN_IDENTIFIER, DRIVER_IDENTIFIER, GOOD, QUANTITY, DESTINATION)


	response = {'transaction': transaction.admin_dict(), 'transaction_hashed': transaction.t_hash(transaction.admin_dict()),'signature': transaction.sign_transaction()}

	return jsonify(response), 200



if __name__ == '__main__':
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('-p', '--port', default=8088, type=int, help='port to listen on')
	args = parser.parse_args()
	port = args.port

	app.run(host='127.0.0.1', port=port, debug = True)
