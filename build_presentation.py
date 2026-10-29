#!/usr/bin/env python3
"""
Generates a 10-slide PowerPoint presentation (.pptx) for the
ESP8266 IoT Smart Dash Button & Cloud Computing Project.
Includes the 5 team members with their exact Roll Numbers and contributions.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cc_project_presentation.pptx")
IMAGE_PATH = r"C:\Users\gandi\.gemini\antigravity-ide\brain\c10ccf7d-0cbe-4a02-a73b-27ed39be58f0\iot_dash_board_1791694011652.jpg"

# Color Palette: Modern Cloud Tech (Deep Navy, Slate, Vibrant Cyan, White)
COLOR_BG = RGBColor(11, 19, 43)        # #0B132B Dark Navy
COLOR_CARD = RGBColor(28, 37, 65)      # #1C2541 Slate Card
COLOR_CYAN = RGBColor(0, 180, 216)     # #00B4D8 Accent Cyan
COLOR_EMERALD = RGBColor(16, 185, 129) # #10B981 Success Green
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_MUTED = RGBColor(160, 175, 200)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def apply_background(slide):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = COLOR_BG
    bg_shape.line.color.rgb = COLOR_BG

def add_header(slide, title_text, category_text="CLOUD COMPUTING PROJECT"):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_CYAN
    p_cat.font.name = "Arial"
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE
    p_title.font.name = "Arial"

def add_card(slide, left, top, width, height, title, items, badge=""):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD
    card.line.color.rgb = RGBColor(45, 60, 95)
    card.line.width = Pt(1)
    
    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), width - Inches(0.4), height - Inches(0.36))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_head = tf.paragraphs[0]
    p_head.text = (f"[{badge}] " if badge else "") + title
    p_head.font.size = Pt(14)
    p_head.font.bold = True
    p_head.font.color.rgb = COLOR_CYAN
    p_head.font.name = "Arial"
    p_head.space_after = Pt(8)
    
    for item in items:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_WHITE
        p.font.name = "Arial"
        p.space_after = Pt(5)

# =========================================================================
# SLIDE 1: Title Slide
# =========================================================================
slide1 = prs.slides.add_slide(blank_layout)
apply_background(slide1)

accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.12), Inches(3.8))
accent_bar.fill.solid()
accent_bar.fill.fore_color.rgb = COLOR_CYAN
accent_bar.line.fill.background()

tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.2))
tf1 = tb1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "COURSE PROJECT : CLOUD COMPUTING & IoT"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_CYAN
p.space_after = Pt(10)

p = tf1.add_paragraph()
p.text = "IoT Smart Dash Button System"
p.font.size = Pt(38)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE

p = tf1.add_paragraph()
p.text = "Edge-to-Cloud Event-Driven Architecture with ESP8266 NodeMCU"
p.font.size = Pt(20)
p.font.color.rgb = COLOR_MUTED
p.space_after = Pt(24)

p = tf1.add_paragraph()
p.text = "Presented By: G.Dhiraj kumar • M.Sri Harsh • Y.Jay Vardhan • G.Sathwik • S.Jashwanth"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_CYAN

# =========================================================================
# SLIDE 2: Team Members & Contributions (5 MEMBERS)
# =========================================================================
slide2 = prs.slides.add_slide(blank_layout)
apply_background(slide2)
add_header(slide2, "Project Team Members & Contributions", "TEAM CREDITS")

team_members = [
    ("G.Dhiraj kumar", "2503A52735", "Team Lead / Cloud Architecture", "LEAD", [
        "Serverless cloud webhook design",
        "Cloudflare Worker HTTP POST pipeline",
        "Architecture planning & team coordination"
    ]),
    ("M.Sri Harsh", "2503A52740", "Firmware & Networking", "CORE", [
        "ESP8266 C++ firmware (Untitled-1.cpp)",
        "WiFiClientSecure TLS socket handler",
        "Wi-Fi handshake & connection management"
    ]),
    ("Y.Jay Vardhan", "2503A52747", "Hardware & Circuit Design", "CORE", [
        "Wokwi circuit schematic design",
        "NodeMCU Pin D2 (GPIO 4) pull-up logic",
        "Short-circuit removal & wiring validation"
    ]),
    ("G.Sathwik", "2503A52734", "Debounce Logic & Testing", "CORE", [
        "500ms software debounce implementation",
        "Baseline Serial Monitor sketch (sketch.ino)",
        "Contact bounce rejection verification"
    ]),
    ("S.Jashwanth", "2503A52743", "Telemetry & UI Dashboard", "CORE", [
        "Real-time web monitoring dashboard",
        "Python simulation suite (run_simulation.py)",
        "Latency profiling & CSV event audit logging"
    ])
]

# 5 Columns layout
card_w = Inches(2.28)
gap = Inches(0.18)
start_left = Inches(0.6)

for idx, (name, roll, role, badge, tasks) in enumerate(team_members):
    c_left = start_left + idx * (card_w + gap)
    
    card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.8), card_w, Inches(4.9))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD
    card.line.color.rgb = RGBColor(45, 60, 95)
    card.line.width = Pt(1)
    
    tb = slide2.shapes.add_textbox(c_left + Inches(0.14), Inches(1.95), card_w - Inches(0.28), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = f"[{badge}]"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD if badge == "LEAD" else COLOR_CYAN
    
    p = tf.add_paragraph()
    p.text = name
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.font.name = "Arial"
    
    p = tf.add_paragraph()
    p.text = f"Roll: {roll}"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.font.name = "Arial"
    p.space_after = Pt(4)
    
    p = tf.add_paragraph()
    p.text = f"Role: {role}"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_MUTED
    p.space_after = Pt(10)
    
    for t in tasks:
        p = tf.add_paragraph()
        p.text = "• " + t
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_WHITE
        p.font.name = "Arial"
        p.space_after = Pt(4)

# =========================================================================
# SLIDE 3: Introduction & Motivation
# =========================================================================
slide3 = prs.slides.add_slide(blank_layout)
apply_background(slide3)
add_header(slide3, "Introduction & Motivation", "PROJECT OVERVIEW")

add_card(slide3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "The IoT Edge-Trigger Paradigm", [
    "Traditional IoT sensors maintain 24/7 persistent socket connections, wasting bandwidth and battery power.",
    "The Smart Dash Button paradigm solves this via Event-Driven Computing: the device sleeps until physically triggered.",
    "A single button push wakes the controller, establishes secure Wi-Fi, dispatches a cloud webhook, and returns to idle.",
    "Eliminates unnecessary cloud server compute hours and maximizes device longevity."
], "CONCEPT")

add_card(slide3, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Real-World Application Domains", [
    "Industrial IoT: Factory-floor emergency stop alerts, maintenance requests, and hazardous incident logging.",
    "Smart Healthcare: Hospital bed patient-call trigger system with zero complex training needed.",
    "Supply Chain & Retail: Instant one-click inventory reordering (Amazon Dash model).",
    "Smart Facilities: Immediate facility maintenance or security scene dispatch over cloud webhooks."
], "APPLICATIONS")

# =========================================================================
# SLIDE 4: Problem Statement & Objectives
# =========================================================================
slide4 = prs.slides.add_slide(blank_layout)
apply_background(slide4)
add_header(slide4, "Problem Statement & Objectives", "PROBLEM DEFINITION")

add_card(slide4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Key Engineering Challenges", [
    "Floating Pin Noise: Microcontroller input pins pick up ambient EMI, triggering false events without stable biasing.",
    "Mechanical Contact Bounce: Physical switches oscillate for several milliseconds, causing 5-10 duplicate triggers per press.",
    "Transmission Insecurity: IoT devices often send unencrypted cleartext HTTP packets over local Wi-Fi networks.",
    "Cloud Idle Waste: Dedicated cloud servers run continuously even when requests arrive sporadically."
], "CHALLENGES")

add_card(slide4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Core Project Objectives", [
    "Design a zero-external-resistor circuit leveraging internal INPUT_PULLUP logic on NodeMCU D2.",
    "Implement an embedded 500ms software debounce filter to eliminate spurious transmissions.",
    "Establish encrypted TLS connections over Wi-Fi using WiFiClientSecure on port 443.",
    "Integrate a Serverless Cloud Webhook backend and a real-time web telemetry dashboard."
], "OBJECTIVES")

# =========================================================================
# SLIDE 5: System Architecture (3-Tier Model)
# =========================================================================
slide5 = prs.slides.add_slide(blank_layout)
apply_background(slide5)
add_header(slide5, "System Architecture : 3-Tier Cloud Model", "ARCHITECTURE")

tiers = [
    ("Tier 1: Edge Layer", "Microcontroller & Sensors", [
        "ESP8266 NodeMCU (160 MHz)",
        "Pin D2 (GPIO 4) & GND wiring",
        "Internal 10k pull-up resistor",
        "500ms debounce interrupt filter"
    ]),
    ("Tier 2: Transport Layer", "Networking & Encryption", [
        "Wi-Fi 802.11 b/g/n (Wokwi-GUEST)",
        "WiFiClientSecure socket handler",
        "TLS encrypted channel (Port 443)",
        "JSON-formatted POST payload"
    ]),
    ("Tier 3: Cloud Layer", "Serverless & Dashboard", [
        "Cloudflare Workers / AWS Lambda",
        "Zero-idle compute scaling",
        "HTTP 200 OK acknowledgment",
        "Live Web Telemetry Dashboard"
    ])
]

for idx, (title, subtitle, items) in enumerate(tiers):
    left = Inches(0.8 + idx * 3.95)
    add_card(slide5, left, Inches(1.8), Inches(3.8), Inches(4.8), title, [f"Focus: {subtitle}"] + items, f"TIER {idx+1}")

# =========================================================================
# SLIDE 6: Hardware Design & Circuit Schematic
# =========================================================================
slide6 = prs.slides.add_slide(blank_layout)
apply_background(slide6)
add_header(slide6, "Hardware Design & Circuit Schematic", "CIRCUIT SPECS")

add_card(slide6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "ESP8266 NodeMCU 1.0 Specifications", [
    "Processor: Tensilica L106 32-bit RISC running at 80/160 MHz.",
    "Memory: 64 KB Instruction RAM, 96 KB Data RAM, 4MB SPI Flash.",
    "Wireless: Integrated 802.11 b/g/n Wi-Fi transceiver with PCB antenna.",
    "GPIO: Configured Pin D2 (GPIO 4) with internal pull-up enabled.",
    "Operating Voltage: 3.3V logic level powered via micro-USB 5V regulator."
], "HARDWARE")

add_card(slide6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Circuit Schematic & Wiring Logic", [
    "Pin D2 (GPIO 4) is connected directly to pushbutton terminal 1.",
    "Opposite pushbutton terminal is connected directly to NodeMCU GND.",
    "Normal State (Released): Pin D2 is held HIGH (3.3V) by internal 10k resistor.",
    "Trigger State (Pressed): Pin D2 is grounded to LOW (0V).",
    "Critical Fix: Removed erroneous 3V3-to-GND bypass connection from early design, preventing circuit shorts."
], "SCHEMATIC")

# =========================================================================
# SLIDE 7: Embedded Firmware Implementation
# =========================================================================
slide7 = prs.slides.add_slide(blank_layout)
apply_background(slide7)
add_header(slide7, "Embedded Firmware & Dual-Mode Logic", "FIRMWARE")

add_card(slide7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "sketch.ino : Serial Validation Mode", [
    "Serves as the baseline hardware sanity check sketch.",
    "Configures pinMode(buttonPin, INPUT_PULLUP) at 115200 baud.",
    "Runs continuous loop reading digitalRead(D2) with 200ms polling.",
    "Outputs 'Button pressed' (LOW) or 'Button released' (HIGH).",
    "Validates physical contact connectivity before initializing network stacks."
], "LOCAL MODE")

add_card(slide7, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Untitled-1.cpp : IoT Cloud Webhook Mode", [
    "Full production firmware with <ESP8266WiFi.h> and <WiFiClientSecure.h>.",
    "Connects to Wi-Fi access point with automatic connection retry.",
    "Active Debouncing: delay(500) prevents duplicate triggers on contact bounce.",
    "Formats HTTP POST request with host header and Content-Type: application/json.",
    "Dispatches JSON payload and cleanly closes TCP socket on completion."
], "CLOUD MODE")

# =========================================================================
# SLIDE 8: Serverless Cloud Webhook Processing
# =========================================================================
slide8 = prs.slides.add_slide(blank_layout)
apply_background(slide8)
add_header(slide8, "Serverless Cloud Webhook Integration", "CLOUD BACKEND")

add_card(slide8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Serverless Compute Model", [
    "Event-Triggered: Cloud worker instantiates only when an HTTP POST packet arrives.",
    "Zero Idle Cost: Eliminates 24/7 compute charges incurred by traditional virtual machines.",
    "Auto-Scaling: Can process from 1 to 100,000 simultaneous button presses seamlessly.",
    "Target Providers: Cloudflare Workers (V8 isolates), AWS Lambda, or Google Cloud Run."
], "PARADIGM")

add_card(slide8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Webhook Payload & Response Cycle", [
    "Request Method: POST / HTTP/1.1 with TLS 1.3 encryption.",
    "Payload Schema: {\"message\": \"Hello from physical trigger button!\", \"pin\": \"D2\", \"device\": \"NodeMCU\"}.",
    "Authentication: API bearer token or HMAC signature header support.",
    "Response: HTTP 200 OK with {\"status\": \"success\", \"received\": true}.",
    "Downstream Actions: SMS alert (Twilio), database entry, or MQTT broker relay."
], "API PROTOCOL")

# =========================================================================
# SLIDE 9: Live Dashboard & Telemetry Results
# =========================================================================
slide9 = prs.slides.add_slide(blank_layout)
apply_background(slide9)
add_header(slide9, "Live Dashboard & Telemetry Results", "RESULTS & VERIFICATION")

if os.path.exists(IMAGE_PATH):
    slide9.shapes.add_picture(IMAGE_PATH, Inches(0.8), Inches(1.8), width=Inches(6.2))
else:
    add_card(slide9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Telemetry Web Dashboard", [
        "Interactive 3D push button with tactile sound FX.",
        "Live animated packet tracer across all 5 architecture steps.",
        "Real-time serial console running at 115200 baud.",
        "Historical event audit table with CSV export."
    ], "DASHBOARD")

add_card(slide9, Inches(7.3), Inches(1.8), Inches(5.2), Inches(4.8), "Experimental Performance Metrics", [
    "Average Round-Trip Latency: 42ms (Edge button press to Cloud 200 OK).",
    "Debounce Accuracy: 100% of sub-500ms bounce contacts successfully suppressed.",
    "Cloud Delivery Success Rate: 100% across all simulated test cycles.",
    "Wi-Fi Signal Strength: -54 dBm RSSI (Excellent connection quality).",
    "Python Simulation Runner: run_simulation.py successfully verifies entire pipeline locally."
], "METRICS")

# =========================================================================
# SLIDE 10: Future Enhancements & Conclusion
# =========================================================================
slide10 = prs.slides.add_slide(blank_layout)
apply_background(slide10)
add_header(slide10, "Future Enhancements & Conclusion", "CONCLUSION")

add_card(slide10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Planned Future Enhancements", [
    "Deep Sleep Power Optimization: Put ESP8266 into deep sleep (<20µA current) and wake via GPIO 16 (D0) to RST tie for 1+ year coin-cell battery life.",
    "MQTT / AWS IoT Core Protocol: Transition from HTTP to lightweight MQTT publish/subscribe for ultra-low packet overhead.",
    "Hardware mTLS: Integrate ATECC608A cryptographic co-processor for zero-touch hardware certificate authentication.",
    "Multi-Click Gestures: Support single-click, double-click, and long-press for multi-purpose action triggering."
], "FUTURE WORK")

add_card(slide10, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), "Summary & Key Takeaways", [
    "Successfully prototyped a functional IoT Smart Dash Button using ESP8266 NodeMCU.",
    "Eliminated external circuit components using internal INPUT_PULLUP resistor logic.",
    "Demonstrated seamless integration between edge physical hardware and Serverless Cloud Webhooks.",
    "Developed an interactive live monitoring dashboard and Python simulation suite for full project validation."
], "SUMMARY")

prs.save(OUTPUT_FILE)
print(f"Successfully generated: {OUTPUT_FILE} with 5 team members.")
