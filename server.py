import http.server
import socketserver
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs

class MojHandler(http.server.SimpleHTTPRequestHandler):
	zadaci=[]
	sljedeciZadatak=0

	def end_headers(self):
		self.send_my_headers()
		http.server.SimpleHTTPRequestHandler.end_headers(self)

	def send_my_headers(self):
		self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
		self.send_header("Pragma", "no-cache")
		self.send_header("Expires", "0")


	def do_GET(self):
		print(self.path)
		if self.path.startswith("/sabiranje"):
			parsed_url = urlparse(self.path)
			captured_value = parse_qs(parsed_url.query)
			print(captured_value["a"][0])
			print(captured_value["b"][0])
			data=str(int(captured_value["a"][0])+int(captured_value["b"][0]))
			self.send_response(200)
			self.send_header('Content-Type', 'text/plain')
			self.end_headers()
			self.wfile.write(data.encode('utf8'))
			return

		if self.path.startswith("/api/to-do"):
			data=json.dumps(MojHandler.zadaci)
			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			self.wfile.write(data.encode('utf8'))
			return

		return http.server.SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):
		if self.path.startswith("/api/novizapis"):
			print("bla bla")
			length = int(self.headers.get('content-length'))
			rfile_str = json.loads(self.rfile.read(length).decode('utf8'))
			print(rfile_str["tekst"])
			data=json.dumps({"stanje":"zapisano"})
			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			self.wfile.write(data.encode('utf8'))
			return

		if self.path.startswith("/api/novi-zadatak"):
			length = int(self.headers.get('content-length'))
			rfile_str = json.loads(self.rfile.read(length).decode('utf8'))
			MojHandler.zadaci.append({"id":MojHandler.sljedeciZadatak,"tekst":rfile_str["noviZadatak"]})
			MojHandler.sljedeciZadatak=MojHandler.sljedeciZadatak+1;
			data=json.dumps(MojHandler.zadaci)
			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			self.wfile.write(data.encode('utf8'))
			return

		if self.path.startswith("/api/izbaci-zadatak"):
			length = int(self.headers.get('content-length'))
			rfile_str = json.loads(self.rfile.read(length).decode('utf8'))
			for i in range(0,len(MojHandler.zadaci)):
				if MojHandler.zadaci[i]["id"]==int(rfile_str["izbaciZadatak"]):
					MojHandler.zadaci.pop(i)
					break

			data=json.dumps(MojHandler.zadaci)
			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			self.wfile.write(data.encode('utf8'))
			return
		

PORT = 8000

with socketserver.TCPServer(("", PORT), MojHandler) as httpd:
	print("serving at port", PORT)
	httpd.serve_forever()


