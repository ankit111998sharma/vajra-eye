const TITLES = {
  dash: ["Live dashboard", "Perception · motion gate · COCO/YOLO · AES-GCM notify"],
  alerts: ["Threat alerts", "Human-harming weapons only · acknowledge to clear fatigue"],
  evidence: ["Keyframe evidence", "Frames admitted by θ_area · laboratory store"],
  admin: ["Policy", "Administrator thresholds · audited on save"],
  audit: ["Audit log", "Login, policy, and acknowledgement trail"],
};

let session = null;
let tickTimer = null;
let liveTimer = null;
let liveBusy = false;

const $ = (id) => document.getElementById(id);

function show(view) {
  document.querySelectorAll("nav button").forEach((b) => b.classList.toggle("active", b.dataset.view === view));
  document.querySelectorAll("main .panel").forEach((p) => {
    p.hidden = p.id !== "view-" + view;
  });
  if ($("view-title")) {
    $("view-title").textContent = TITLES[view][0];
    $("view-sub").textContent = TITLES[view][1];
  }
  if (view === "admin") loadConfig();
  if (view === "alerts") {
    refreshWeapons();
    refreshAlerts();
  }
}

function enterApp() {
  $("login-view").hidden = true;
  $("app-view").hidden = false;
  $("who").textContent = (session.username || "") + " · " + (session.role || "");
  const adminBtn = document.querySelector('[data-view="admin"]');
  if (adminBtn) adminBtn.style.display = session.role === "ADMIN" ? "" : "none";
  if (tickTimer) clearInterval(tickTimer);
  if (liveTimer) clearInterval(liveTimer);
  tick();
  tickTimer = setInterval(tick, 1500);
  liveTimer = setInterval(refreshLive, 1200);
  show("dash");
}

function showLoginError(msg) {
  const box = $("login-err");
  if (!box) return;
  box.hidden = false;
  box.textContent = msg;
}

async function login(ev) {
  if (ev) ev.preventDefault();
  const userEl = $("user");
  const passEl = $("pass");
  const username = userEl ? userEl.value.trim() : "localhost";
  const password = passEl ? passEl.value : "root";
  showLoginError("");
  $("login-err").hidden = true;
  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await res.json();
    if (!data.ok) {
      showLoginError(data.error || "Login failed");
      return;
    }
    session = { username: data.username, role: data.role };
    sessionStorage.setItem("vajra.session", JSON.stringify(session));
    enterApp();
  } catch (err) {
    // JS/API failed — submit the normal HTML form to /login
    const form = $("login-form");
    if (form) {
      form.submit();
      return;
    }
    showLoginError("Cannot reach server at http://localhost:8088/");
  }
}

async function tick() {
  try {
    const st = await (await fetch("/api/status")).json();
    $("kpi-cam").textContent = st.cameraId;
    $("kpi-frames").textContent = st.framesIngested;
    $("kpi-keys").textContent = st.keyframes;
    $("kpi-alerts").textContent = st.alerts;
    $("src").textContent = st.videoSource;
    $("model").textContent = modelLabel(st);
    $("marea").textContent = Math.round(st.lastMotionArea || 0);
    $("upd").textContent = new Date(st.ts).toLocaleTimeString();
    $("clock").textContent = new Date().toLocaleString();
    const badge = $("pipe-badge");
    badge.textContent = st.pipeline;
    badge.className = "badge " + (st.capturing ? "ok" : "");
    const pill = $("motion-pill");
    if (!st.capturing) {
      pill.textContent = "STOPPED";
      pill.className = "pill stopped";
    } else {
      pill.textContent = st.lastMotion ? "MOTION" : "IDLE";
      pill.className = "pill " + (st.lastMotion ? "motion" : "idle");
    }
    const startBtn = $("btn-start");
    const stopBtn = $("btn-stop");
    if (startBtn && stopBtn) {
      startBtn.disabled = !!st.capturing;
      stopBtn.disabled = !st.capturing;
    }
    if (st.alerts > 0) badge.classList.add("hot");
    renderSeen(st.seen);
  } catch (e) {
    console.warn("status refresh", e);
  }
  refreshAlerts();
  refreshEvidence();
  refreshAudit();
}

function renderSeen(seen) {
  const items = Array.isArray(seen) ? seen : [];
  const text = items.length
    ? items.map((s) => (s.threat ? "ALERT " : "") + (s.className || "") + " " + Number(s.probability || 0).toFixed(2)).join(", ")
    : "nothing yet — stand in view so person / face / hand can be labeled";
  const dash = $("seen");
  if (dash) dash.textContent = text;
  const line = $("seen-line");
  if (line) {
    line.textContent = "Camera sees: " + text;
    line.className = items.some((s) => s.threat) ? "alert-banner live" : "alert-banner";
  }
}

function modelLabel(st) {
  if (st.modelReady) {
    return "Ready (" + (st.detector || "COCO") + ") · person / face / hand / knife";
  }
  if ((st.detector || "") === "loading") {
    return "Detector downloading…";
  }
  return "Motion-only (no detector)";
}

function setBanner(data) {
  const banner = $("alert-banner");
  if (!banner) return;
  if (data && data.modelReady) {
    banner.className = "alert-banner live";
    banner.textContent = (data.policy || "Alert on human-harming weapons.") +
      " Detector: " + (data.detector || "ready") +
      ". Labels match the frame: person, face, hand, knife, gun (if the model names it).";
  } else if (data && (data.detector === "loading" || data.detector === undefined)) {
    banner.className = "alert-banner";
    banner.textContent = "Detector is loading. Threat alerts will appear here as soon as a knife, scissors, fork, or baseball bat is seen.";
  } else {
    banner.className = "alert-banner warn";
    banner.textContent = "No neural detector loaded. Motion still records Evidence. Place yolov8n.onnx under models/ or wait for the COCO zoo model.";
  }
}

function renderWeapons(items) {
  const body = $("weapon-rows");
  if (!body) return;
  const rows = items || [];
  body.innerHTML = rows.map((w) => `
    <tr>
      <td>${w.weapon || ""}</td>
      <td>${w.kind || ""}</td>
      <td>${w.alertIfDetected || ""}</td>
      <td>${w.availability || ""}</td>
    </tr>`).join("") || `<tr><td colspan="4">Weapon listing unavailable.</td></tr>`;
}

async function refreshWeapons() {
  try {
    const data = await (await fetch("/api/weapons")).json();
    renderWeapons(data.items);
    setBanner(data);
  } catch (e) {
    console.warn("weapons refresh", e);
  }
}

async function refreshAlerts() {
  const body = $("alert-rows");
  if (!body) return;
  try {
    const alerts = await (await fetch("/api/alerts")).json();
    setBanner(alerts);
    renderSeen(alerts.seen);
    if (alerts.weapons) renderWeapons(alerts.weapons);
    const items = Array.isArray(alerts.items) ? alerts.items : [];
    if (!items.length) {
      const why = alerts.modelReady
        ? "No human-harming weapon seen yet. Hold a knife, scissors, or baseball bat in view of the camera."
        : "Detector not ready yet. Motion keyframes still go to Evidence.";
      body.innerHTML = `<tr><td colspan="7">${why}</td></tr>`;
      return;
    }
    body.innerHTML = items.map((a) => `
    <tr>
      <td>${a.id || ""}</td>
      <td><span class="sev">${a.weaponType || ""}</span></td>
      <td>${Number(a.confidence || 0).toFixed(2)}</td>
      <td>${a.cameraId || ""}</td>
      <td>${a.channel || ""}</td>
      <td>${a.ts ? new Date(a.ts).toLocaleTimeString() : ""}</td>
      <td>${a.acked ? "ACK" : `<button class="btn" data-ack="${a.id}">Ack</button>`}</td>
    </tr>`).join("");
  } catch (e) {
    console.warn("alerts refresh", e);
    body.innerHTML = `<tr><td colspan="7">Could not load threat alerts. Retrying…</td></tr>`;
  }
}

async function refreshEvidence() {
  const grid = $("ev-grid");
  if (!grid) return;
  try {
    const ev = await (await fetch("/api/evidence")).json();
    grid.innerHTML = (ev.items || []).map((e) => `
    <article class="ev-card">
      <img src="/api/evidence/${e.id}.jpg" alt="${e.id}" />
      <p><b>${e.id}</b><br/>${e.cameraId} · area ${e.motionArea}<br/>${e.ts ? new Date(e.ts).toLocaleTimeString() : ""}</p>
    </article>`).join("") || "<p class='hint'>No keyframes stored yet.</p>";
  } catch (e) {
    console.warn("evidence refresh", e);
  }
}

async function refreshAudit() {
  const body = $("audit-rows");
  if (!body) return;
  try {
    const au = await (await fetch("/api/audit")).json();
    body.innerHTML = (au.items || []).map((r) => `
    <tr>
      <td>${r.id}</td><td>${r.user}</td><td>${r.action}</td>
      <td>${r.detail || ""}</td><td>${r.ts ? new Date(r.ts).toLocaleTimeString() : ""}</td>
    </tr>`).join("") || `<tr><td colspan="5">No audit rows.</td></tr>`;
  } catch (e) {
    console.warn("audit refresh", e);
  }
}

function refreshLive() {
  const img = $("live");
  if (!img || liveBusy) return;
  liveBusy = true;
  const done = () => { liveBusy = false; };
  img.onload = () => {
    const empty = $("live-empty");
    if (empty) empty.hidden = true;
    done();
  };
  img.onerror = done;
  img.src = "/api/snapshot.jpg?t=" + Date.now();
}

async function loadConfig() {
  try {
    const c = await (await fetch("/api/config")).json();
    const f = $("policy-form");
    if (!f) return;
    f.pixelThreshold.value = c.pixelThreshold;
    f.minArea.value = c.minArea;
    f.panFraction.value = c.panFraction;
    f.minProbability.value = c.minProbability;
    f.cooldownMs.value = c.cooldownMs;
  } catch (e) {
    console.warn(e);
  }
}

const loginForm = $("login-form");
if (loginForm) {
  // Native POST to /login (no fetch). This is the reliable path in the browser.
}
const logoutBtn = $("logout");
if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    sessionStorage.removeItem("vajra.session");
    try { await fetch("/api/logout", { method: "POST" }); } catch (e) { /* ignore */ }
    location.href = "/";
  });
}
document.querySelectorAll("nav button").forEach((b) => b.addEventListener("click", () => show(b.dataset.view)));
async function toggleCapture(on) {
  const url = on ? "/api/capture/start" : "/api/capture/stop";
  try {
    await fetch(url, { method: "POST" });
    tick();
  } catch (e) {
    console.warn(e);
  }
}
const startBtn = $("btn-start");
const stopBtn = $("btn-stop");
if (startBtn) startBtn.addEventListener("click", () => toggleCapture(true));
if (stopBtn) stopBtn.addEventListener("click", () => toggleCapture(false));
const alertRows = $("alert-rows");
if (alertRows) {
  alertRows.addEventListener("click", async (e) => {
    const id = e.target.getAttribute("data-ack");
    if (!id || !session) return;
    await fetch("/api/alerts/" + id + "/ack", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user: session.username }),
    });
    refreshAlerts();
  });
}
const policyForm = $("policy-form");
if (policyForm) {
  policyForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!session || session.role !== "ADMIN") {
      $("policy-msg").hidden = false;
      $("policy-msg").textContent = "Only ADMIN may change policy.";
      return;
    }
    const f = e.target;
    const body = {
      pixelThreshold: Number(f.pixelThreshold.value),
      minArea: Number(f.minArea.value),
      panFraction: Number(f.panFraction.value),
      minProbability: Number(f.minProbability.value),
      cooldownMs: Number(f.cooldownMs.value),
      user: session.username,
    };
    await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    $("policy-msg").hidden = false;
    $("policy-msg").textContent = "Policy saved to MySQL (vajra_eye.policy_settings).";
  });
}

if (new URLSearchParams(location.search).get("error") === "1") {
  showLoginError("Invalid credentials. Username localhost / password root.");
}

(async function boot() {
  try {
    const me = await (await fetch("/api/me")).json();
    if (me.ok) {
      session = { username: me.username, role: me.role };
      enterApp();
      return;
    }
  } catch (e) {
    /* stay on login */
  }
  const saved = sessionStorage.getItem("vajra.session");
  if (saved) {
    try { session = JSON.parse(saved); } catch (e) { session = null; }
  }
})();
