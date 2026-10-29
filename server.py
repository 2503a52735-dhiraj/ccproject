#!/usr/bin/env python3
"""
ESP8266 IoT Dash Button — Dashboard Local Web Server
-----------------------------------------------------
Serves the web dashboard interface and handles real-time REST API
triggers, AWS Learner Lab (Lambda & API Gateway) proxy forwarding,
telemetry logs, and cloud response analytics.
"""

import os
import sys
import json
import time
import uuid
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(DIRECTORY, "aws_config.json")

# Default AWS Learner Lab Configuration
DEFAULT_CONFIG = {
    "provider": "aws_learner_lab",
    "region": "us-east-1",
    "role": "LabRole",
    "endpoint_url": "",
    "environment": "AWS Academy Learner Lab",
    "auto_forward": True
}


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()


def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        print(f"[CONFIG] Warning: Could not save config file: {e}")


server_config = load_config()


class IoTServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        sys.stdout.write(f"[{time.strftime('%X')}] {format % args}\n")
        sys.stdout.flush()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-amz-date')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        # -------------------------------------------------------------
        # 1. IoT Dash Button Trigger Dispatch
        # -------------------------------------------------------------
        if self.path == '/api/trigger':
            print("\n" + "=" * 55)
            print(" [DASHBOARD EVENT] >> Physical Pushbutton Trigger Received!")
            payload = {}
            try:
                payload = json.loads(post_data.decode('utf-8'))
                pin = payload.get('pin', 'D2')
                gpio = payload.get('gpio', 4)
                event_id = payload.get('event_id', f"evt_aws_{int(time.time())}")
                msg = payload.get('message', 'Physical trigger button pressed')
                target_url = payload.get('target_endpoint') or server_config.get('endpoint_url', '')
                print(f" [PAYLOAD] >> Pin: {pin} (GPIO {gpio})")
                print(f" [PAYLOAD] >> Event ID: {event_id}")
                print(f" [PAYLOAD] >> Target: {target_url or 'AWS Learner Lab (Simulation Mode)'}")
            except Exception as e:
                print(f" [PARSE ERROR] >> {e}")
                target_url = server_config.get('endpoint_url', '')

            # Check if user has provided a real live AWS Endpoint URL
            is_real_aws = bool(target_url and target_url.startswith("http") and "your-worker" not in target_url and "<" not in target_url)

            if is_real_aws:
                print(f" [AWS FORWARD] >> Dispatching live HTTPS POST to AWS Learner Lab...")
                start_t = time.time()
                try:
                    forward_body = json.dumps({
                        "device": "ESP8266-NodeMCU",
                        "pin": payload.get('pin', 'D2'),
                        "gpio": payload.get('gpio', 4),
                        "event_id": payload.get('event_id', f"evt_aws_{int(time.time())}"),
                        "timestamp": payload.get('timestamp', int(time.time())),
                        "message": payload.get('message', 'Hello from physical ESP8266 dash button!'),
                        "cloud": "AWS Learner Lab",
                        "region": server_config.get("region", "us-east-1")
                    }).encode('utf-8')

                    req = urllib.request.Request(
                        target_url,
                        data=forward_body,
                        headers={
                            'Content-Type': 'application/json',
                            'User-Agent': 'ESP8266-NodeMCU-DashButton/1.0 (AWS Academy)'
                        },
                        method='POST'
                    )

                    with urllib.request.urlopen(req, timeout=7.0) as resp:
                        status_code = resp.getcode()
                        raw_resp = resp.read().decode('utf-8')
                        latency = int((time.time() - start_t) * 1000)
                        req_id = resp.headers.get('x-amzn-requestid') or resp.headers.get('x-amz-request-id') or f"aws-{uuid.uuid4().hex[:8]}"

                        print(f" [AWS RESPONSE] << HTTP {status_code} OK | RequestId: {req_id} | Latency: {latency}ms")
                        print("=" * 55 + "\n")

                        try:
                            parsed_body = json.loads(raw_resp)
                        except Exception:
                            parsed_body = {"raw": raw_resp}

                        self._send_json(200, {
                            "status": "success",
                            "is_live_aws": True,
                            "http_code": status_code,
                            "aws_request_id": req_id,
                            "latency_ms": latency,
                            "cloud_provider": "AWS Learner Lab (Live Endpoint)",
                            "region": server_config.get("region", "us-east-1"),
                            "target_url": target_url,
                            "aws_payload": parsed_body,
                            "timestamp": int(time.time())
                        })
                        return

                except urllib.error.HTTPError as he:
                    latency = int((time.time() - start_t) * 1000)
                    err_body = he.read().decode('utf-8', errors='ignore')
                    print(f" [AWS ERROR] << HTTP {he.code}: {err_body} ({latency}ms)")
                    print("=" * 55 + "\n")
                    self._send_json(200, {
                        "status": "aws_error",
                        "is_live_aws": True,
                        "http_code": he.code,
                        "error": str(he),
                        "details": err_body,
                        "latency_ms": latency,
                        "cloud_provider": "AWS Learner Lab",
                        "timestamp": int(time.time())
                    })
                    return

                except Exception as ex:
                    latency = int((time.time() - start_t) * 1000)
                    print(f" [AWS FORWARD FAILED] >> {ex} ({latency}ms)")
                    print("=" * 55 + "\n")
                    self._send_json(200, {
                        "status": "network_error",
                        "is_live_aws": True,
                        "error": str(ex),
                        "latency_ms": latency,
                        "cloud_provider": "AWS Learner Lab",
                        "timestamp": int(time.time()),
                        "note": "Could not connect to the configured AWS URL. Check network or Function URL CORS."
                    })
                    return

            # Default / Simulated AWS Learner Lab mode
            simulated_req_id = f"aws-lab-{uuid.uuid4().hex[:12]}"
            print(f" [AWS SIMULATION] >> Processed with Simulated AWS Lambda (Role: LabRole) [RequestId: {simulated_req_id}]")
            print("=" * 55 + "\n")

            self._send_json(200, {
                "status": "success",
                "is_live_aws": False,
                "http_code": 200,
                "aws_request_id": simulated_req_id,
                "latency_ms": 38,
                "cloud_provider": "AWS Learner Lab (Simulated Lambda)",
                "region": server_config.get("region", "us-east-1"),
                "role": "LabRole",
                "timestamp": int(time.time()),
                "message": "Processed in simulated AWS Learner Lab environment. Enter your live Function URL above to switch to live cloud execution!"
            })
            return

        # -------------------------------------------------------------
        # 2. Update AWS Learner Lab Configuration
        # -------------------------------------------------------------
        elif self.path == '/api/aws-config':
            try:
                new_cfg = json.loads(post_data.decode('utf-8'))
                for k in ["endpoint_url", "region", "provider"]:
                    if k in new_cfg:
                        server_config[k] = new_cfg[k].strip()
                save_config(server_config)
                print(f"[CONFIG] Updated AWS Learner Lab Endpoint: {server_config.get('endpoint_url')}")
                self._send_json(200, {"status": "updated", "config": server_config})
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return

        # -------------------------------------------------------------
        # 3. Test AWS Connection Ping
        # -------------------------------------------------------------
        elif self.path == '/api/test-endpoint':
            try:
                body = json.loads(post_data.decode('utf-8'))
                test_url = body.get('endpoint_url') or server_config.get('endpoint_url', '')
                if not test_url or not test_url.startswith("http"):
                    self._send_json(400, {"status": "error", "message": "Invalid URL provided."})
                    return

                start_t = time.time()
                ping_payload = json.dumps({"test": True, "ping": "AWS Learner Lab Health Check"}).encode('utf-8')
                req = urllib.request.Request(
                    test_url,
                    data=ping_payload,
                    headers={'Content-Type': 'application/json', 'User-Agent': 'AWS-LearnerLab-Ping/1.0'},
                    method='POST'
                )
                with urllib.request.urlopen(req, timeout=5.0) as resp:
                    latency = int((time.time() - start_t) * 1000)
                    resp_data = resp.read().decode('utf-8')
                    req_id = resp.headers.get('x-amzn-requestid') or "available"
                    self._send_json(200, {
                        "status": "connected",
                        "http_code": resp.getcode(),
                        "latency_ms": latency,
                        "aws_request_id": req_id,
                        "body_preview": resp_data[:200]
                    })
            except urllib.error.HTTPError as he:
                latency = int((time.time() - start_t) * 1000)
                self._send_json(200, {
                    "status": "http_error",
                    "http_code": he.code,
                    "latency_ms": latency,
                    "error": str(he)
                })
            except Exception as ex:
                self._send_json(200, {
                    "status": "failed",
                    "error": str(ex)
                })
            return

        elif self.path == '/api/cloud-webhook':
            self._send_json(200, {"status": "delivered", "cloud": "aws-learner-lab"})
            return

        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == '/api/status':
            self._send_json(200, {
                "status": "online",
                "board": "ESP8266 NodeMCU 1.0",
                "pin": "D2",
                "gpio": 4,
                "pullup": "10k internal pull-up",
                "cloud_provider": "AWS Learner Lab",
                "region": server_config.get("region", "us-east-1"),
                "role": "LabRole",
                "has_live_endpoint": bool(server_config.get("endpoint_url"))
            })
            return

        elif self.path == '/api/aws-config':
            self._send_json(200, server_config)
            return

        # Default: serve static files
        return super().do_GET()

    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


def run_server():
    server_address = ('127.0.0.1', PORT)
    try:
        httpd = HTTPServer(server_address, IoTServerHandler)
        print(f"\n=======================================================")
        print(f"  ESP8266 IoT DASH BUTTON -> AWS LEARNER LAB DASHBOARD")
        print(f"  Live URL: http://localhost:{PORT}/")
        print(f"  Cloud Provider: AWS Learner Lab (Region: {server_config.get('region', 'us-east-1')})")
        print(f"  Directory: {DIRECTORY}")
        print(f"=======================================================\n")
        httpd.serve_forever()
    except OSError as e:
        if e.errno in (98, 10048):
            alt_port = 5000
            print(f"Port {PORT} in use, trying {alt_port}...")
            httpd = HTTPServer(('127.0.0.1', alt_port), IoTServerHandler)
            print(f"Live URL: http://localhost:{alt_port}/")
            httpd.serve_forever()
        else:
            raise e


if __name__ == '__main__':
    run_server()
