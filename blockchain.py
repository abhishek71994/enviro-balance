import hashlib
from time import time
from uuid import uuid4
import json
import requests
from urllib.parse import urlparse
from textwrap import dedent
import requests
from flask import Flask, jsonify, request


class Blockchain(object):
	"""docstring for Blockchain"""
	def __init__(self):
		self.chain = []
		self.currentTransactions = []
		self.node = set()
		#create a genesis block
		self.new_block(previous_hash='1',proof=100)
	
	def new_block(self,proof,previous_hash=None):
		#this code is used to make the new blocks
		block = {
			'index' : len(self.chain)+1,
			'timestamp' : time(),
			'transations' : self.currentTransactions,
			'proof' : proof,
			'previous_hash' : previous_hash or self.hash(self.chain[-1]),
		}

		self.transations = []

		self.chain.append(block);
		return block

	def register_node(self,address):
		parsed_url = urlparse(address)
		self.node.add(parsed_url.netloc)


	def new_transaction(self,sender,reciever,resources_used,pollutants):
		#this will add on the new transations that will be done
		self.currentTransactions.append({
			'sender' : sender,
			'reciever' : reciever,
			'resources_used' : resources_used,
			'pollutants' : pollutants,
			})
		return self.last_block['index']+1

	def proof_of_work(self,last_block):
		last_proof = last_block['proof']
		last_hash = self.hash(last_block)
		proof = 0
		while self.valid_proof(last_proof,proof,last_hash) is False:
			proof += 1
		return proof

	def valid_proof(self,last_proof,proof,last_hash):
		guess = f'{last_proof}{proof}{last_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

	@staticmethod
	def hash(block):
		#hashes a block
		block_string = json.dumps(block,sort_keys=True).encode()
		return hashlib	.sha256(block_string).hexdigest()

	@property
	def last_block(self):
		#returns the last block
		return self.chain[-1]

#instantiating our node 
app = Flask(__name__)

#global unique id
node_identifier = str(uuid4()).replace('-','')

#creating the block chain

blockchain = Blockchain()

@app.route('/mine',methods=['GET'])
def mine():
	#proof of work algorithm to get next proof
	last_block = blockchain.last_block
	proof = blockchain.proof_of_work(last_block)

	#we have to find a way for the blockchain to have it's root entry
	#the states are 0 to show that the property chain has started
	blockchain.new_transaction(
		sender = '0',
		reciever = node_identifier,
		resources_used = '',
		pollutants = ''
		)
	previous_hash = blockchain.hash(last_block)
	block = blockchain.new_block(proof,previous_hash)

	response = {
		'message' : 'New block made',
		'index' : block['index'],
		'transations' : block['transations'],
		'proof' : block['proof'],
		'previous_hash' : block['previous_hash'],
	}
	return jsonify(response), 200

@app.route('/transactions/new',methods=['POST'])
def transations_new():
	values = request.get_json()
	#required fields
	required = ['sender','reciever','resources_used','pollutants']
	if not all(k in values for k in required):
		return 'Missing values',400

	#create a new transaction
	index = blockchain.new_transaction(values['sender'],values['reciever'],values['resources_used'],values['pollutants'])
	response = {'message' : f'transaction will be added to the block {index}'}
	return jsonify(response),201

@app.route('/chain',methods=['GET'])
def chain():
	response = {
		'chain' : blockchain.chain,
		'length' : len(blockchain.chain),
	}

	return jsonify(response),200

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=3000)