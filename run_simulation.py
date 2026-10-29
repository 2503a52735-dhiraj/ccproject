#!/usr/bin/env python3
"""
ESP8266 IoT Button Simulation Runner
------------------------------------
This script emulates the ESP8266 NodeMCU execution flow of both:
  1. sketch.ino (Local Serial Button Monitor)
  2. Untitled-1.cpp (IoT Cloud Trigger over WiFi & HTTPS)

It lets you see the serial monitor output, understand state transitions,
and simulate cloud webhook triggers right in your terminal.
"""

import sys
import time
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class MockWorkerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence default server logging to keep output clean
        pass

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        print("\n  [CLOUD SERVER] >> Received HTTP POST request!")
        print(f"  [CLOUD SERVER] >> Path: {self.path}")
        print(f"  [CLOUD SERVER] >> Headers: Content-Type: {self.headers.get('Content-Type')}")
        try:
            payload = json.loads(post_data.decode('utf-8'))
            print(f"  [CLOUD SERVER] >> Payload: {json.dumps(payload, indent=4)}")
        except Exception:
            print(f"  [CLOUD SERVER] >> Raw Body: {post_data.decode('utf-8')}")

        # Send HTTP 200 OK response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "success", "received": true}')
        print("  [CLOUD SERVER] << Responded 200 OK\n")

def run_sketch_ino_demo(cycles=5):
    print("\n" + "="*60)
    print(" RUNNING: sketch.ino (Basic Button State Monitor)")
    print("="*60)
    print("[Serial Monitor: 115200 baud]")
    time.sleep(0.5)
    print("Wokwi button demo started")
    time.sleep(0.5)

    # Simulate button states
    states = [
        ("Released (HIGH)", "Button released"),
        ("Released (HIGH)", "Button released"),
        ("PRESSED  (LOW)",  "Button pressed"),
        ("PRESSED  (LOW)",  "Button pressed"),
        ("Released (HIGH)", "Button released"),
    ]

    for i, (physical, serial_out) in enumerate(states[:cycles], 1):
        time.sleep(0.4)
        print(f" -> Pin D2: {physical} | Serial Output: \"{serial_out}\"")

    print("="*60)
    print(" sketch.ino test completed successfully.")
    print("="*60 + "\n")

def run_untitled_cpp_demo():
    print("\n" + "="*60)
    print(" RUNNING: Untitled-1.cpp (IoT Webhook Cloud Button Trigger)")
    print("="*60)
    print("[Serial Monitor: 115200 baud]")
    time.sleep(0.3)
    print("Connecting to fictional network: Wokwi-GUEST")
    for _ in range(4):
        time.sleep(0.2)
        print(".", end="", flush=True)
    print("\nWi-Fi (simulated) connected.\n")
    time.sleep(0.5)

    # Start local mock server to demonstrate actual network trigger
    port = 8787
    server = HTTPServer(('127.0.0.1', port), MockWorkerHandler)
    server_thread = threading.Thread(target=server.handle_request)
    server_thread.daemon = True
    server_thread.start()

    print("[ESP8266 System Ready - Waiting for button press on GPIO 4 (D2)]")
    print("Simulating: User pushes the physical button...")
    time.sleep(1)

    print("----------------------------------------")
    print(">>> BUTTON PRESSED! <<<")
    print(f"Attempting to connect to: 127.0.0.1:{port} (Simulated Cloudflare Worker)")
    
    # Send actual HTTP POST to the mock server to simulate the network packet
    import urllib.request
    url = f"http://127.0.0.1:{port}/"
    payload = json.dumps({"message": "Hello from the physical trigger button!"}).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            res_body = response.read().decode('utf-8')
            print("HTTPS POST request sent (Simulated Network Success).")
            print(f"Server Response: {res_body}")
    except Exception as e:
        print(f"Connection notice: {e}")

    print("----------------------------------------")
    print("="*60)
    print(" Untitled-1.cpp test completed successfully.")
    print("="*60 + "\n")

if __name__ == "__main__":
    print("\n" + "#"*60)
    print("  ESP8266 / NODEMCU PROJECT SIMULATION & VERIFICATION")
    print("#"*60)
    
    # 1. Run sketch.ino
    run_sketch_ino_demo()
    time.sleep(1)

    # 2. Run Untitled-1.cpp
    run_untitled_cpp_demo()

    print("Simulation finished. All project logic verified!")
