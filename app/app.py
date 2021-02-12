import json
import time
import logging

from pypresence import Presence
from flask import Flask, request


client_id = '794449494585638922'

rpc = Presence(client_id)
app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/', methods=['POST'])
def index():
	body = json.loads(request.data)
	if body['action'] == 'set':
		rpc.update(
			state = body['state'][:128],
			details = body['details'][:128],
			start = time.time(),
			large_image = 'dclogo'
			)
	else:
		rpc.clear()
	return ''

if __name__ == '__main__':
	rpc.connect()
	app.run('localhost', 3000, False)