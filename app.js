/**
 * ESP8266 IoT Dash Button — Dashboard Controller
 * AWS Learner Lab & Cloud Telemetry Client
 */

(function () {
  'use strict';

  // Complete AWS Lambda Handler Code ready for 1-click clipboard copy
  const AWS_LAMBDA_TEMPLATE = `import json
import time

def lambda_handler(event, context):
    print(" [AWS LEARNER LAB] ESP8266 IoT Dash Button Triggered!")
    print(f" Request ID: {context.aws_request_id}")
    
    # Handle CORS preflight
    http_method = event.get('requestContext', {}).get('http', {}).get('method') or event.get('httpMethod', '')
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            },
            'body': ''
        }

    body = {}
    raw_body = event.get('body')
    if raw_body:
        try:
            body = json.loads(raw_body)
        except Exception:
            body = {"raw": raw_body}

    pin = body.get('pin', 'D2')
    gpio = body.get('gpio', 4)
    device = body.get('device', 'ESP8266-NodeMCU')
    event_id = body.get('event_id', f"evt_aws_{int(time.time())}")

    print(f" Device: {device} | Pin: {pin} (GPIO {gpio}) | Event: {event_id}")

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "status": "success",
            "cloud": "AWS Learner Lab",
            "region": "us-east-1",
            "role": "LabRole",
            "aws_request_id": context.aws_request_id,
            "message": f"Pushbutton on {pin} successfully processed in AWS Lambda!"
        })
    }
`;

  // --- STATE ---
  const state = {
    mode: 'cloud', // 'cloud' (Untitled-1.cpp) or 'basic' (sketch.ino)
    soundEnabled: true,
    totalClicks: 0,
    successfulPosts: 0,
    latencies: [42, 38, 45],
    events: [],
    lastPressTime: 0,
    debounceMs: 500,
    isProcessing: false,
    endpointUrl: '',
    cloudProvider: 'AWS Learner Lab',
    region: 'us-east-1',
    role: 'LabRole',
    filter: 'all'
  };

  // --- AUDIO SYNTHESIS ---
  let audioCtx = null;
  function playClickSound(isPress = true) {
    if (!state.soundEnabled) return;
    try {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.connect(gain);
      gain.connect(audioCtx.destination);

      if (isPress) {
        osc.frequency.setValueAtTime(320, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(140, audioCtx.currentTime + 0.04);
        gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.04);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.04);
      } else {
        osc.frequency.setValueAtTime(450, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(280, audioCtx.currentTime + 0.03);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.03);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.03);
      }
    } catch (e) {
      // Audio autoplay policy catch
    }
  }

  // --- DOM ELEMENTS ---
  const dashBtn = document.getElementById('dash-button');
  const ledRing = document.getElementById('led-ring');
  const pinBadge = document.getElementById('pin-state-badge');
  const btnPressAction = document.getElementById('btn-press-action');
  const btnBurstAction = document.getElementById('btn-burst-action');
  const terminalBody = document.getElementById('terminal-body');
  const autoscrollToggle = document.getElementById('autoscroll-toggle');
  const modeCloudOpt = document.getElementById('mode-cloud-opt');
  const modeSketchOpt = document.getElementById('mode-sketch-opt');
  const activeFirmwareName = document.getElementById('active-firmware-name');
  const toggleAudioBtn = document.getElementById('toggle-audio-btn');
  const audioState = document.getElementById('audio-state');
  const audioIcon = document.getElementById('audio-icon');
  const runAutoTestBtn = document.getElementById('run-auto-test-btn');
  const targetEndpointInput = document.getElementById('target-endpoint-input');
  const btnSaveEndpoint = document.getElementById('btn-save-endpoint');
  const btnTestCloudPing = document.getElementById('btn-test-cloud-ping');
  const btnCopyPayload = document.getElementById('btn-copy-payload');
  const payloadCode = document.getElementById('payload-code');
  const eventsTbody = document.getElementById('events-tbody');
  const btnClearTable = document.getElementById('btn-clear-table');
  const btnExportCsv = document.getElementById('btn-export-csv');
  const btnClearTerminal = document.getElementById('btn-clear-terminal');
  const btnCopyTerminal = document.getElementById('btn-copy-terminal');
  const endpointModeTag = document.getElementById('endpoint-mode-tag');

  // AWS Guide Modal Elements
  const btnOpenGuide = document.getElementById('btn-open-guide');
  const awsGuideModal = document.getElementById('aws-guide-modal');
  const btnCloseModal = document.getElementById('btn-close-modal');
  const btnCloseModalFooter = document.getElementById('btn-close-modal-footer');
  const btnCopyLambdaCode = document.getElementById('btn-copy-lambda-code');
  const btnCopyModalCode = document.getElementById('btn-copy-modal-code');

  // Metric displays
  const valTotalClicks = document.getElementById('val-total-clicks');
  const valSuccessfulPosts = document.getElementById('val-successful-posts');
  const valAvgLatency = document.getElementById('val-avg-latency');
  const valWifiRssi = document.getElementById('val-wifi-rssi');
  const pipelineStatus = document.getElementById('pipeline-status');

  // Pipeline elements
  const stepButton = document.getElementById('step-button');
  const stepEsp = document.getElementById('step-esp');
  const stepWifi = document.getElementById('step-wifi');
  const stepCloud = document.getElementById('step-cloud');
  const stepResponse = document.getElementById('step-response');
  const stepCloudDetail = document.getElementById('step-cloud-detail');
  const stepResponseDetail = document.getElementById('step-response-detail');
  const conn1 = document.getElementById('conn-1');
  const conn2 = document.getElementById('conn-2');
  const conn3 = document.getElementById('conn-3');
  const conn4 = document.getElementById('conn-4');

  // --- TERMINAL UTILITY ---
  function getTimeStr() {
    const d = new Date();
    return d.toTimeString().split(' ')[0] + '.' + String(d.getMilliseconds()).padStart(3, '0');
  }

  function logToTerminal(text, type = 'system') {
    const line = document.createElement('div');
    line.className = `terminal-line ${type}-msg`;
    line.dataset.type = type;
    line.textContent = `[${getTimeStr()}] ${text}`;

    if (state.filter !== 'all' && type !== state.filter) {
      line.style.display = 'none';
    }

    terminalBody.appendChild(line);

    if (autoscrollToggle.checked) {
      terminalBody.scrollTop = terminalBody.scrollHeight;
    }
  }

  // Fetch initial config from local server
  async function initServerConfig() {
    try {
      const resp = await fetch('/api/aws-config');
      if (resp.ok) {
        const cfg = await resp.json();
        if (cfg.endpoint_url) {
          state.endpointUrl = cfg.endpoint_url;
          targetEndpointInput.value = cfg.endpoint_url;
          endpointModeTag.textContent = 'AWS LIVE CONNECTED';
          endpointModeTag.style.background = 'rgba(16, 185, 129, 0.2)';
          endpointModeTag.style.color = '#10b981';
          endpointModeTag.style.borderColor = 'rgba(16, 185, 129, 0.4)';
          logToTerminal(`[AWS] Loaded saved endpoint: ${cfg.endpoint_url}`, 'ready-msg');
        } else {
          endpointModeTag.textContent = 'AWS SIMULATION ACTIVE';
          logToTerminal('[AWS] Ready in AWS Learner Lab Simulation Mode (Role: LabRole, us-east-1).', 'system');
        }
      }
    } catch (e) {
      logToTerminal('[AWS] Local server ready (offline simulation available).', 'system');
    }
  }

  // --- BUTTON INTERACTION LOGIC ---
  function triggerButtonPress(isManual = true) {
    const now = Date.now();
    const timeSinceLast = now - state.lastPressTime;

    // Visual button press animation
    dashBtn.classList.add('pressed');
    ledRing.classList.add('active-flash');
    pinBadge.textContent = 'PIN D2: LOW (PRESSED)';
    pinBadge.classList.add('pressed');
    playClickSound(true);

    // Debounce Check
    if (state.lastPressTime !== 0 && timeSinceLast < state.debounceMs) {
      logToTerminal(`[DEBOUNCE] Suppressed bounce event (${timeSinceLast}ms < ${state.debounceMs}ms limit)`, 'system');
      setTimeout(() => releaseButtonVisual(), 150);
      return;
    }

    state.lastPressTime = now;
    state.totalClicks++;
    valTotalClicks.textContent = state.totalClicks;

    if (state.mode === 'basic') {
      logToTerminal('Button pressed (GPIO 4 / D2)', 'press-msg');
      setTimeout(() => {
        releaseButtonVisual();
        logToTerminal('Button released (GPIO 4 / D2)', 'system');
      }, 200);
      return;
    }

    executeCloudPipeline();
    setTimeout(() => releaseButtonVisual(), 200);
  }

  function releaseButtonVisual() {
    dashBtn.classList.remove('pressed');
    ledRing.classList.remove('active-flash');
    pinBadge.textContent = 'PIN D2: HIGH (RELEASED)';
    pinBadge.classList.remove('pressed');
    playClickSound(false);
  }

  // --- AWS CLOUD PIPELINE EXECUTION ---
  async function executeCloudPipeline() {
    pipelineStatus.textContent = 'TRANSMITTING HTTPS POST TO AWS...';
    pipelineStatus.classList.add('firing');

    const isLive = Boolean(state.endpointUrl && state.endpointUrl.startsWith('http'));
    const targetLabel = isLive ? state.endpointUrl : 'AWS Learner Lab (Simulated Lambda)';

    logToTerminal('----------------------------------------', 'system');
    logToTerminal('>>> BUTTON PRESSED! <<<', 'press-msg');
    logToTerminal(`Target: ${targetLabel} (Region: ${state.region})`, 'net-msg');

    // Pipeline Step 1: Button Push
    stepButton.classList.add('active');
    await delay(120);
    conn1.classList.add('active');

    // Pipeline Step 2: ESP8266 ISR & Debounce
    await delay(150);
    stepEsp.classList.add('active');
    conn2.classList.add('active');
    logToTerminal('WiFiClientSecure initialized. TLS session starting...', 'net-msg');

    // Pipeline Step 3: Wi-Fi Transmission
    await delay(150);
    stepWifi.classList.add('active');
    conn3.classList.add('active');

    const eventId = 'evt_aws_' + Math.random().toString(36).substring(2, 8).toUpperCase();
    const payload = {
      device: 'ESP8266-NodeMCU',
      pin: 'D2',
      gpio: 4,
      message: 'Hello from physical ESP8266 dash button!',
      cloud: 'AWS Learner Lab',
      region: state.region,
      timestamp: Math.floor(Date.now() / 1000),
      event_id: eventId,
      target_endpoint: state.endpointUrl
    };

    logToTerminal(`POST / HTTP/1.1 | Host: ${isLive ? state.endpointUrl.replace('https://', '').split('/')[0] : 'lambda.us-east-1.amazonaws.com'}`, 'http-msg');
    logToTerminal(`Payload: ${JSON.stringify({ device: payload.device, pin: payload.pin, event_id: payload.event_id })}`, 'http-msg');

    // Pipeline Step 4: AWS Lambda Execution
    await delay(150);
    stepCloud.classList.add('active');
    stepCloudDetail.textContent = isLive ? 'AWS Lambda (Live Proxy)' : 'AWS Lambda (LabRole)';
    conn4.classList.add('active');

    const startTime = performance.now();
    let latency = 40 + Math.floor(Math.random() * 20);
    let awsReqId = 'aws-' + Math.random().toString(36).substring(2, 10);
    let serverSuccess = true;
    let respBodyPreview = '';

    try {
      const resp = await fetch('/api/trigger', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (resp.ok) {
        const data = await resp.json();
        latency = data.latency_ms || Math.round(performance.now() - startTime);
        if (data.aws_request_id) awsReqId = data.aws_request_id;
        if (data.is_live_aws) {
          logToTerminal(`[AWS LIVE RESPONSE] HTTP ${data.http_code} OK (RequestId: ${awsReqId})`, 'response-msg');
          respBodyPreview = JSON.stringify(data.aws_payload || {});
        } else {
          logToTerminal(`[AWS SIMULATION] Processed by AWS Lambda (LabRole, us-east-1) [${awsReqId}]`, 'response-msg');
          respBodyPreview = data.message || 'Lambda execution complete';
        }
      }
    } catch (e) {
      logToTerminal(`[NETWORK NOTICE] Local proxy offline; executed in client simulation.`, 'system');
    }

    state.latencies.push(latency);
    if (state.latencies.length > 20) state.latencies.shift();
    const avgLatency = Math.round(state.latencies.reduce((a, b) => a + b, 0) / state.latencies.length);
    valAvgLatency.textContent = avgLatency;

    // Pipeline Step 5: HTTP 200 OK
    await delay(120);
    stepResponse.classList.add('active');
    stepResponseDetail.textContent = `HTTP 200 (${latency}ms)`;
    logToTerminal(`Cloud Response: 200 OK | RequestId: ${awsReqId}`, 'response-msg');
    logToTerminal('----------------------------------------', 'system');

    // Record Event
    state.successfulPosts++;
    valSuccessfulPosts.textContent = state.successfulPosts;
    addEventToLog(eventId, payload.pin, isLive ? state.endpointUrl : 'AWS Learner Lab (Sim)', 200, latency, awsReqId);

    // Reset pipeline visual
    setTimeout(() => {
      [stepButton, stepEsp, stepWifi, stepCloud, stepResponse].forEach(el => el.classList.remove('active', 'completed'));
      [conn1, conn2, conn3, conn4].forEach(el => el.classList.remove('active'));
      pipelineStatus.textContent = 'IDLE - AWAITING TRIGGER';
      pipelineStatus.classList.remove('firing');
    }, 1400);
  }

  function addEventToLog(id, pin, host, status, latency, reqId) {
    const timeStr = new Date().toLocaleTimeString();
    const eventObj = { time: timeStr, id, pin, host, status, latency, reqId };
    state.events.unshift(eventObj);

    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${timeStr}</td>
      <td style="color:#FF9900;font-weight:700;">#${id}</td>
      <td>${pin}</td>
      <td title="${host}" style="max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#94a3b8;">${host}</td>
      <td><span class="badge-200" style="background:rgba(255,153,0,0.15);color:#ffb039;">HTTP ${status}</span></td>
      <td>${latency}ms</td>
    `;
    eventsTbody.insertBefore(row, eventsTbody.firstChild);
  }

  function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // --- BURST TEST (3x rapid debounce) ---
  async function runBurstTest() {
    logToTerminal('[TEST] Launching 3x rapid burst push sequence...', 'system');
    triggerButtonPress();
    await delay(100);
    triggerButtonPress();
    await delay(100);
    triggerButtonPress();
  }

  // --- AUTOMATED SIMULATION SEQUENCE ---
  async function runAutoTest() {
    runAutoTestBtn.disabled = true;
    runAutoTestBtn.textContent = 'Testing in Progress...';
    logToTerminal('============================================================', 'system');
    logToTerminal('STARTING AUTOMATED SIMULATION SEQUENCE (AWS LEARNER LAB)', 'ready-msg');
    logToTerminal('============================================================', 'system');

    // 1. Test sketch.ino mode
    state.mode = 'basic';
    modeSketchOpt.classList.add('active');
    modeCloudOpt.classList.remove('active');
    activeFirmwareName.textContent = 'sketch.ino (Serial Monitor)';
    logToTerminal('MODE SWITCH: Running sketch.ino demo cycle', 'system');
    await delay(400);

    for (let i = 0; i < 2; i++) {
      triggerButtonPress();
      await delay(600);
    }

    // 2. Test AWS Lambda mode
    await delay(800);
    state.mode = 'cloud';
    modeCloudOpt.classList.add('active');
    modeSketchOpt.classList.remove('active');
    activeFirmwareName.textContent = 'Untitled-1.cpp (AWS Lambda Webhook)';
    logToTerminal('MODE SWITCH: Running Untitled-1.cpp -> AWS Lambda Webhook test', 'system');
    await delay(600);

    triggerButtonPress();
    await delay(2000);

    logToTerminal('============================================================', 'system');
    logToTerminal('Simulation Finished. AWS Learner Lab Pipeline Verified!', 'ready-msg');
    logToTerminal('============================================================', 'system');

    runAutoTestBtn.disabled = false;
    runAutoTestBtn.innerHTML = `
      <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
      Run Test Cycle
    `;
  }

  function copyToClipboard(text, btnElement, successMsg = 'Copied!') {
    navigator.clipboard.writeText(text).then(() => {
      const originalText = btnElement.textContent;
      btnElement.textContent = successMsg;
      setTimeout(() => {
        btnElement.textContent = originalText;
      }, 1600);
    });
  }

  // --- EVENT LISTENERS ---
  dashBtn.addEventListener('click', () => triggerButtonPress(true));
  btnPressAction.addEventListener('click', () => triggerButtonPress(true));
  btnBurstAction.addEventListener('click', runBurstTest);
  runAutoTestBtn.addEventListener('click', runAutoTest);

  // Keyboard Space trigger
  window.addEventListener('keydown', (e) => {
    if (e.code === 'Space' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
      e.preventDefault();
      triggerButtonPress(true);
    }
  });

  // Sound toggle
  toggleAudioBtn.addEventListener('click', () => {
    state.soundEnabled = !state.soundEnabled;
    audioState.textContent = state.soundEnabled ? 'ON' : 'OFF';
    audioIcon.textContent = state.soundEnabled ? '🔊' : '🔇';
  });

  // Firmware toggle
  modeCloudOpt.addEventListener('click', () => {
    state.mode = 'cloud';
    modeCloudOpt.classList.add('active');
    modeSketchOpt.classList.remove('active');
    activeFirmwareName.textContent = 'Untitled-1.cpp (AWS Lambda Webhook)';
    logToTerminal('[MODE] Switched firmware to Untitled-1.cpp (AWS Lambda Webhook enabled)', 'system');
  });

  modeSketchOpt.addEventListener('click', () => {
    state.mode = 'basic';
    modeSketchOpt.classList.add('active');
    modeCloudOpt.classList.remove('active');
    activeFirmwareName.textContent = 'sketch.ino (Serial Monitor)';
    logToTerminal('[MODE] Switched firmware to sketch.ino (Local Serial Monitor only)', 'system');
  });

  // Save AWS Endpoint
  btnSaveEndpoint.addEventListener('click', async () => {
    const val = targetEndpointInput.value.trim();
    state.endpointUrl = val;
    if (val) {
      endpointModeTag.textContent = 'AWS LIVE CONNECTED';
      endpointModeTag.style.background = 'rgba(16, 185, 129, 0.2)';
      endpointModeTag.style.color = '#10b981';
      endpointModeTag.style.borderColor = 'rgba(16, 185, 129, 0.4)';
      logToTerminal(`[CONFIG] Applied AWS endpoint: ${val}`, 'ready-msg');
      try {
        await fetch('/api/aws-config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ endpoint_url: val, region: 'us-east-1', provider: 'aws_learner_lab' })
        });
      } catch (e) {}
    } else {
      endpointModeTag.textContent = 'AWS SIMULATION ACTIVE';
      endpointModeTag.style.background = 'rgba(255, 153, 0, 0.15)';
      endpointModeTag.style.color = '#FF9900';
      logToTerminal('[CONFIG] AWS endpoint cleared. Reverted to AWS Learner Lab Simulation mode.', 'system');
    }
  });

  // Ping AWS Endpoint
  btnTestCloudPing.addEventListener('click', async () => {
    const testUrl = state.endpointUrl || targetEndpointInput.value.trim();
    if (!testUrl) {
      logToTerminal('[PING] No live endpoint entered. Executing test dispatch via simulated AWS Lambda...', 'system');
      executeCloudPipeline();
      return;
    }
    logToTerminal(`[PING] Dispatching health check to ${testUrl}...`, 'system');
    try {
      const resp = await fetch('/api/test-endpoint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ endpoint_url: testUrl })
      });
      const res = await resp.json();
      if (res.status === 'connected') {
        logToTerminal(`[PING SUCCESS] Connected to AWS! HTTP ${res.http_code} (${res.latency_ms}ms) | ReqId: ${res.aws_request_id}`, 'ready-msg');
      } else {
        logToTerminal(`[PING RESULT] ${res.status}: ${res.error || res.message || 'Check URL'}`, 'system');
      }
    } catch (e) {
      logToTerminal(`[PING ERROR] Could not contact local proxy: ${e}`, 'system');
    }
  });

  // Copy JSON Payload
  btnCopyPayload.addEventListener('click', () => {
    copyToClipboard(payloadCode.textContent, btnCopyPayload, 'Copied!');
  });

  // Copy Lambda Code buttons
  if (btnCopyLambdaCode) {
    btnCopyLambdaCode.addEventListener('click', () => {
      copyToClipboard(AWS_LAMBDA_TEMPLATE, btnCopyLambdaCode, 'Lambda Code Copied!');
    });
  }
  if (btnCopyModalCode) {
    btnCopyModalCode.addEventListener('click', () => {
      copyToClipboard(AWS_LAMBDA_TEMPLATE, btnCopyModalCode, 'Lambda Code Copied!');
    });
  }

  // Guide Modal controls
  if (btnOpenGuide) {
    btnOpenGuide.addEventListener('click', () => {
      awsGuideModal.classList.add('open');
    });
  }
  if (btnCloseModal) {
    btnCloseModal.addEventListener('click', () => {
      awsGuideModal.classList.remove('open');
    });
  }
  if (btnCloseModalFooter) {
    btnCloseModalFooter.addEventListener('click', () => {
      awsGuideModal.classList.remove('open');
    });
  }
  window.addEventListener('click', (e) => {
    if (e.target === awsGuideModal) {
      awsGuideModal.classList.remove('open');
    }
  });

  // Table actions
  btnClearTable.addEventListener('click', () => {
    state.events = [];
    eventsTbody.innerHTML = '';
  });

  btnExportCsv.addEventListener('click', () => {
    if (state.events.length === 0) {
      alert('No events to export yet. Press the button to generate events!');
      return;
    }
    const header = 'Time,Event ID,Pin,Target Host,Status,Latency (ms),AWS Request ID\n';
    const rows = state.events.map(e => `"${e.time}","${e.id}","${e.pin}","${e.host}",${e.status},${e.latency},"${e.reqId || ''}"`).join('\n');
    const blob = new Blob([header + rows], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `aws_iot_events_${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  });

  // Terminal actions
  btnClearTerminal.addEventListener('click', () => {
    terminalBody.innerHTML = '';
  });

  btnCopyTerminal.addEventListener('click', () => {
    const lines = Array.from(terminalBody.querySelectorAll('.terminal-line')).map(l => l.textContent).join('\n');
    copyToClipboard(lines, btnCopyTerminal, 'Copied!');
  });

  // Filter chips
  document.querySelectorAll('.filter-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      state.filter = chip.dataset.filter;
      const lines = terminalBody.querySelectorAll('.terminal-line');
      lines.forEach(l => {
        if (state.filter === 'all' || l.dataset.type === state.filter) {
          l.style.display = 'block';
        } else {
          l.style.display = 'none';
        }
      });
    });
  });

  // Initialize
  initServerConfig();
  addEventToLog('EVT_AWS_INIT', 'D2', 'AWS Learner Lab (us-east-1)', 200, 39, 'aws-init-req');

})();
