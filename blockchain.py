import hashlib
from time import time
from uuid import uuid4
import json

class Blockchain(object):
	"""docstring for Blockchain"""
	def __init__(self):
		self.chain = []
		self.currentTransactions = []
		#create a genesis block
		self.new_block(previous_hash=1,proof=100)
	
	def new_block(self,previous_hash=None,proof):
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

	def new_transaction(self,init_state,final_state,resources_used,pollutants):
		#this will add on the new transations that will be done
		self.currentTransactions.append({
			'init_state' : init_state,
			'final_state' : final_state,
			'resources_used' : resources_used,
			'pollutants' : pollutants,
			})
		return self.last_block['index']+1

	def proof_of_work(self,last_proof):
		proof = 0
		while self.valid_proof(last_proof,proof) is False:
			proof += 1
		return proof

	def valid_proof(last_proof,proof):
		guess = f'{last_proof}{proof}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


	@staticmethod
	def hash(block):
		#hashes a block
		block_string = json.dumps(block,sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()

	@property
	def last_block(self):
		#returns the last block
		return self.chain[-1]