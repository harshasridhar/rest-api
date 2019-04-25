from flask import Flask, render_template, request 
from time import sleep
import pandas
from sklearn.utils import shuffle
from random import randint
from pickle import load
app = Flask(__name__,static_url_path='/static')
et_trained_model = load(open('trained_models/et_trained_model','rb'))
rf_trained_model = load(open('trained_models/rf_trained_model','rb'))
def testFunc():
	return 'Hello World'
@app.route('/')
def index():
	# return "Hello, World!"
	return render_template("index.html")

@app.route('/test',methods = ['GET'])
def getPage():
	# return 'GET request made from the server'
	t = "*"
	for i in range(2000): #just to simulate processing delay
		t +="*"*i
		t +="<br>"
	r = randint(0,1)
	d ={0:"Malicious",1:"Normal"}
	return d[r]

@app.route("/main",methods=['GET'])
def mainPage():
	return render_template("main.html")

@app.route("/test",methods =['POST'])
def postFunction():
	print("POST request handling, data obtained:")
	test_data = request.json['test_data']
	algorithm = request.json['algorithm']
	if algorithm == "rfc":
		model = rf_trained_model
	else:
		model = et_trained_model
	# here we will call the model for prediction
	list = []
	list.append(test_data)
	val = model.predict(list)
	return str(val[0])

@app.route("/data", methods =['GET'])
def getData():
	df= pandas.read_csv('data.csv')
	#shuffling so that we can a mixture of both the classes
	df = shuffle(df)
	# changing column names because they contain '.' which would be difficult in JSON parsing
	df.columns = ['Unnamed: 0','frame_time_epoch', 'frame_len', 'eth_src', 'eth_dst', 'ip_src',
       'ip_dst', 'tcp_srcport', 'tcp_dstport', 'udp_srcport', 'udp_dstport',
       'icmp_type', 'icmp_code', 'arp_opcode', 'arp_src_hw_mac',
       'arp_src_proto_ipv4', 'arp_dst_hw_mac', 'arp_dst_proto_ipv4',
       'ipv6_src', 'ipv6_dst', 'output']
	df.reset_index(inplace=True)
	response = df[:][:10].to_json(orient='index')
	return response 

@app.route("/results",methods=['GET'])
def showResults():
	return render_template("results.html")

if __name__ == '__main__':
	app.run(debug=True)
