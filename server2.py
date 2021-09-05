from flask import Flask,redirect,request,jsonify,Response
import threading
import time

app = Flask(__name__,static_url_path='', static_folder='.')

zadaci=[]
sljedeciZadatak=0
uslov=threading.Condition()
squares=[]
history=[]
step=0;

for i in range(0,9):
	squares.append(None)

history.append({"squares":squares})
print(history)

brojKlijenata=0


def get_message():
	with uslov:
		uslov.wait()
	s = time.ctime(time.time())
	return s

@app.route("/")
def hello_world():
	return redirect("/index.html", code=302)

@app.route("/sabiranje")
def saberi():
	a=request.args.get("a")
	b=request.args.get("b")
	return str(int(a)+int(b))

@app.route("/api/to-do")
def toDo():
	return jsonify(zadaci)

@app.route("/api/novi-zadatak", methods=["POST"])
def dodajNoviZadatak():
	global sljedeciZadatak
	zadaci.append({"id":sljedeciZadatak,"tekst":request.json["noviZadatak"]})
	sljedeciZadatak+=1
	with uslov:
		uslov.notify_all()
	return jsonify(zadaci)

@app.route("/api/izbaci-zadatak", methods=["POST"])
def izbaciZadatak():
	zaIzbaciti=request.json["izbaciZadatak"]
	for i in range(0,len(zadaci)):
		if zadaci[i]["id"]==int(zaIzbaciti):
			zadaci.pop(i)
			break
	with uslov:
		uslov.notify_all()
	return jsonify(zadaci)

@app.route('/stream')
def stream():
	global brojKlijenata
	print("spojio se klijent",brojKlijenata)
	brojKlijenata+=1
	def eventStream():
		while True:
			# wait for source data to be available, then push it
			yield 'data: {}\n\n'.format(get_message())
	return Response(eventStream(), mimetype="text/event-stream")


@app.route("/api/ticTacToe")
def ticTacToe():
	global history
	global step
	return jsonify({"history":history,"step":step})

@app.route("/api/ticTacToeStep")
def ticTacToeStep():
	
	print(step)
	return jsonify(step)

@app.route("/api/noviKorak", methods=["POST"])
def dodajNoviKorak():
	global squares
	global step
	global history
	square=[]
	step+=1
	print(history)
	square=request.json["noviKorak"]
	history.append({"squares":square})
	print(history)
	with uslov:
		uslov.notify_all()
	return jsonify(history)

@app.route('/stream/ticTacToe')
def streamTicTacToe():
	def eventStream1():
		while True:
			# wait for source data to be available, then push it
			yield 'data: {}\n\n'.format(get_message())
	return Response(eventStream1(), mimetype="text/event-stream")


@app.route("/api/ticTacToeSetStep", methods=["POST"])
def setStep():
	global step
	step=request.json["setStep"]
	del history[step+1:]
	with uslov:
		uslov.notify_all()
	return jsonify(step)

@app.route("/api/proba", methods=["POST"])
def proba():
	print("probaaaa")
	print(request.json["proba"])
	#with uslov:
	#	uslov.notify_all()
	return jsonify(history)
