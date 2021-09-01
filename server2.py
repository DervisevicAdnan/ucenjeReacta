from flask import Flask,redirect,request,jsonify,Response
import threading
import time
from flask_socketio import SocketIO, emit
from flask_login import current_user

app = Flask(__name__,static_url_path='', static_folder='.')
socketio = SocketIO(app)

zadaci=[]
sljedeciZadatak=0
uslov=threading.Condition()
socketio = SocketIO(app)

if __name__ == '__main__':
	socketio.run(app)

@socketio.on('connect')
def connect_handler():
	print("aijfsdfajsfsdfj")
	if current_user.is_authenticated:
		return('my response',
			 {'message': '{0} has joined'.format(current_user.name)},
			 broadcast=True)
	else:
		return False  # not allowed here


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
	def eventStream():
		while True:
			# wait for source data to be available, then push it
			yield 'data: {}\n\n'.format(get_message())
	return Response(eventStream(), mimetype="text/event-stream")