'''
usage           : python DriverClient.py (port - 8087)
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
		conn = sqlite3.connect("Driver.db")
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS blockchain_driver (id INTEGER PRIMARY KEY, senAdd text, senPriv text, reciAdd text, quantity integer, Hash_transaction text)")
		#
		conn.commit()
		conn.close()

	def __init__(self, driver_identifier, driver_private_key, truck_number, good, destination, insurance_number, quantity): #These attributes are need by the sender to create a transaction.
		self.driver_identifier = driver_identifier
		self.driver_private_key = driver_private_key
		self.truck_number = truck_number
		self.good = good
		self.destination = destination
		self.insurance_number = insurance_number
		self.quantity = quantity
		#self.policy = policy
		#self.size = size
		#self.width = width
		#self.height = height
		#self.load = load
		#self.axleNum = axleNum
		#self.province = province



	def __getattr__(self, attr):
		return self.data[attr]

	def dri_dict(self): #returns transaction information
		return OrderedDict({'driver_identifier': self.driver_identifier,
							'truck_number': self.truck_number,
							'good':self.good,
							'destination': self.destination,
							'insurance_number':self.insurance_number,
							'quantity': self.quantity})
							#'policy': self.axleNum
							#'size': self.size
							#'width': self.width
							#'height': self.height
							#'load': self.load
							#'axleNum': self.axleNum
							#'province': self.province
							

	def sign_transaction(self):
		"""
		Sign transaction with private key
		"""
		private_key = RSA.importKey(binascii.unhexlify(self.driver_private_key))
		signer = PKCS1_v1_5.new(private_key)
		h = SHA.new(str(self.dri_dict()).encode('utf8'))
		return binascii.hexlify(signer.sign(h)).decode('ascii')

	def t_hash(self, dri_dict):
		tx_list = list(dri_dict.values())
		tx_string = "".join(str(x) for x in tx_list)
		tx_hash = hashlib.sha256(tx_string.encode('utf-8'))
		hash_digest = tx_hash.hexdigest()
		return hash_digest

	def insert(driver_identifier, driver_private_key, truck_number, good, destination, insurance_number, quantity):
		conn = sqlite3.connect("Driver.db")
		cur = conn.cursor()
		cur.execute("INSERT INTO blockchain insurance_valueS (NULL, ?, ?, ?, ?, ?, ?, ?)", (driver_identifier, driver_private_key, truck_number, good, destination, insurance_number, quantity))
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

	driver_identifier = request.form['driver_identifier']
	driver_private_key = request.form['driver_private_key']
	truck_number = request.form['truck_number']
	good = request.form['good']
	destination = request.form['destination']
	insurance_number = request.form['insurance_number']
	quantity = request.form['quantity']

	transaction = Transaction(driver_identifier, driver_private_key, truck_number, good, destination, insurance_number, quantity)
	#cur = mysql.connect().cursor()
	#cur.execute("INSERT INTO blockchain insurance_valueS (?,?,?,?)",(driver_identifier, driver_private_key, truck_number, quantity))
	#Transaction.insert(driver_identifier, driver_private_key, truck_number, quantity)


	response = {'transaction': transaction.dri_dict(), 'transaction_hashed': transaction.t_hash(transaction.dri_dict()),'signature': transaction.sign_transaction()}

	return jsonify(response), 200


if __name__ == '__main__':
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('-p', '--port', default=8087, type=int, help='port to listen on')
	args = parser.parse_args()
	port = args.port

	app.run(host='127.0.0.1', port=port, debug = True)
