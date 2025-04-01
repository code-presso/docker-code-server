
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
# import requests #pip install requests
import urllib.request
import logging

logging.basicConfig(
    format='(%(asctime)s) %(levelname)s:%(message)s',
    datefmt='%m/%d %I:%M:%S %p',
    level=logging.DEBUG
)


class MyHandler(BaseHTTPRequestHandler):
    ROUTE_HANDLERS = {
        '/health-check': lambda: 'OK'
    }

    def do_GET(self):
        route = self.path
        response_handler = self.ROUTE_HANDLERS.get(route, None)

        if response_handler:
            response_text = response_handler()
            send_response_and_headers(self, response_text)
        else:
            self.send_error(404, 'Not Found')


def update_settings_json():

    settings_json_file_path = "/config/data/User/settings.json"

    try:
        with open(settings_json_file_path, 'r') as file:
            existing_settings = json.load(file)

        add_settings_json(existing_settings)

        with open(settings_json_file_path, 'w') as file:
            json.dump(existing_settings, file, indent=2)


    except Exception as e:
        logging.error(f'Error {e}')

def add_settings_json(existing_settings):
    existing_settings["liveServer.settings.host"] = get_host_ip()

def get_host_ip():
    try:
        # Use urllib to get the external IP
        with urllib.request.urlopen('https://ifconfig.me') as response:
            return response.read().decode().strip()
    except Exception as e:
        logging.error(f'Error retrieving host IP: {e}')
        return None


def send_response_and_headers(self, response_text):
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write(response_text.encode())


# http://localhost:8443/?folder=/workspace 사용자 작업 코드
if __name__ == '__main__':
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyHandler)
    logging.info(f'Starting server on port {port}...')

    # update_settings_json()

    httpd.serve_forever()
