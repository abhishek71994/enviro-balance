import hashlib
from time import time
from uuid import uuid4
import json
import requests
from urllib.parse import urlparse
from textwrap import dedent
import requests
from flask import Flask, jsonify, request,render_template


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


	def new_transaction(self,sender,reciever,entity,resources_used,pollutants):
		#this will add on the new transations that will be done
		self.currentTransactions.append({
			'sender' : sender,
			'reciever' : reciever,
			'entity' : entity,
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
	def valid_chain(self,chain):
		last_block = chain[0]
		current_index = 1

		while current_index < len(chain):
			block = chain[current_index]
			print(f'{last_block}')
			print(f'{block}')
			print("\n-----------\n")
			# Check that the hash of the block is correct
			if block['previous_hash'] != self.hash(last_block):
				return False

			if not self.valid_proof(last_block['proof'], block['proof']):
				return False

			last_block = block
			current_index += 1

		return True
	def resolve_conflict(self):
		neighbours = self.nodes
		new_chain = none
		max_length = len(self.chain)

		for node in neighbours:
			response = requests.get(f'http://{node}/chain')
			if response.status_code == 200 :
				length = response.json()['length']
				chain = response.json()['chain']
				#check for longer chain and validate it
				if length > max_length and self.valid_chain(chain):
					new_length = length
					new_chain = chain

			if new_chain:
				self.chain = new_chain
				return True
			return False
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
		entity = '',
		resources_used = [],
		pollutants = []
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

@app.route('/nodes/register',methods=['POST'])
def register_nodes():
	value = request.get_json()

	nodes = value.get('nodes')
	if nodes is None:
		return "Error: Please supply a valid list of nodes", 400

	for node in nodes:
		blockchain.register_node(node)

	response = {
		'message': 'New nodes have been added',
		'total_nodes': list(blockchain.nodes),
	}
	return jsonify(response), 201
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
	replaced = blockchain.resolve_conflicts()

	if replaced:
		response = {
 			'message': 'Our chain was replaced',
			'new_chain': blockchain.chain
		}
	else:
		response = {
			'message': 'Our chain is authoritative',
			'chain': blockchain.chain
		}

	return jsonify(response), 200
@app.route('/')
def index():
	return render_template('index.html')
@app.route('/manufacture')
def manufacture():
	return render_template('manufacture.html')
@app.route('/user')
def buyer():
	return render_template('buyer.html')
@app.route('/transactions/new',methods=['POST'])
def transations_new():
	values = request.get_json()
	#required fields
	required = ['sender','reciever','resources_used','pollutants']
	print(required)
	if not all(k in values for k in required):
		return 'Missing values',400

	#create a new transaction
	index = blockchain.new_transaction(values['sender'],values['reciever'],values['entity'],values['resources_used'],values['pollutants'])
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