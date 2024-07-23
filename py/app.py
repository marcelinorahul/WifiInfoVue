from flask import Flask, render_template, jsonify
from flask_cors import CORS
import socket
import subprocess
import re
import platform
import logging

app = Flask(__name__, static_folder='../static', template_folder='../templates')
CORS(app, resources={r"/api/*": {"origins": "*"}})
logging.basicConfig(level=logging.DEBUG)  

def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        logging.info(f"IP Address: {ip_address}")
        return ip_address
    except Exception as e:
        logging.error(f"Error getting IP: {str(e)}")
        return "Tidak dapat mengambil IP Address"

def get_wifi_passwords():
    wifi_passwords = []
    if platform.system() == "Windows":
        try:
            command = "netsh wlan show profiles"
            networks = subprocess.check_output(command, shell=True, text=True)
            network_names = re.findall(r"All User Profile\s*:\s*(.*)", networks)
            
            for network_name in network_names:
                network_name = network_name.strip()
                command = f'netsh wlan show profile name="{network_name}" key=clear'
                result = subprocess.check_output(command, shell=True, text=True)
                password = re.search(r"Key Content\s*:\s*(.*)", result)
                if password:
                    wifi_passwords.append({"ssid": network_name, "password": password.group(1).strip()})
                else:
                    wifi_passwords.append({"ssid": network_name, "password": "Tidak ada password"})
            logging.info(f"WiFi Passwords: {wifi_passwords}")
        except Exception as e:
            logging.error(f"Error getting WiFi info: {str(e)}")
            wifi_passwords.append({"ssid": "Error", "password": "Tidak dapat mengambil informasi WiFi"})
    else:
        wifi_passwords.append({"ssid": "Error", "password": "Hanya berfungsi pada Windows"})
    
    return wifi_passwords

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/network-info', methods=['GET'])
def network_info():
    ip_address = get_ip_address()
    wifi_passwords = get_wifi_passwords()
    response = {"ip_address": ip_address, "wifi_passwords": wifi_passwords}
    logging.info(f"API Response: {response}")
    return jsonify(response), 200, {'Access-Control-Allow-Origin': '*'}  

if __name__ == '__main__':
    app.run(debug=True)