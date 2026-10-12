import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { buildAssembly, updateAssembly, drawAssemblyBeam } from './assembly.js';

const $ = id => document.getElementById(id);
const stage = $('stage'), scene = new THREE.Scene();
scene.background = new THREE.Color(0x09121e);
const camera = new THREE.PerspectiveCamera(40, 1, 0.0001, 5);
camera.up.set(0, 0, 1);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
stage.append(renderer.domElement);
const orbit = new OrbitControls(camera, renderer.domElement);
orbit.enableDamping = true;
let machineAssembly = null;
let assemblyTrace = null, traceRequest = null, traceSequence = 0;
function home() {
  const mode = $('view').value;
  if (mode === 'optical') {
    camera.position.set(.085, -.11, .115); orbit.target.set(0, .006, .043);
    camera.position.sub(orbit.target).multiplyScalar(Math.max(1.15, .85 / camera.aspect)).add(orbit.target);
  } else {
    const close = mode === 'motors' || mode === 'beam', focus = mode === 'focus';
    orbit.target.set(focus ? .31108 : close ? .17 : .21, focus ? -.04028 : 0, focus ? -.047 : close ? .025 : .105);
    const halfFov = Math.min(camera.fov * Math.PI / 360, Math.atan(Math.tan(camera.fov * Math.PI / 360) * camera.aspect));
    const distance = (focus ? .045 : close ? .215 : .360) / Math.sin(halfFov) * 1.1;
    const offset = new THREE.Vector3(close ? .40 : .47, -.88, close ? .51 : .28).normalize().multiplyScalar(distance);
    camera.position.copy(orbit.target).add(offset);
  }
  orbit.update();
}
home();
scene.add(new THREE.HemisphereLight(0xbcdfff, 0x192737, 2.4));
const light = new THREE.DirectionalLight(0xffffff, 3);
light.position.set(.05, -.1, .2); scene.add(light);
const grid = new THREE.GridHelper(1, 20, 0x355068, 0x192d40);
grid.rotation.x = Math.PI / 2; scene.add(grid);
const hardware = new THREE.Group(); scene.add(hardware);
const colors = { target: 0x46d9ff, before: 0xffad54, after: 0x63efae };
const paths = Object.fromEntries(Object.keys(colors).map(k => {
  const g = new THREE.Group(); scene.add(g); return [k, g];
}));
let params = [0, 0, 0, 0, .075], current = null, sequence = 0;
let pending = null, timer = null, training = false, autoAttempted = false;
let commandPending = true;

function dispose(group) {
  const materials = new Set(), textures = new Set();
  group.traverse(o => {
    o.geometry?.dispose();
    if (o.material) for (const m of Array.isArray(o.material) ? o.material : [o.material]) {
      materials.add(m); if (m.map) textures.add(m.map);
    }
  });
  textures.forEach(t => t.dispose()); materials.forEach(m => m.dispose()); group.clear();
}

function line(group, points, color, opacity = 1) {
  const material = new THREE.LineBasicMaterial({ color, transparent: opacity < 1, opacity });
  group.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(points.map(p => new THREE.Vector3(...p))), material));
}

function label(group, text, position) {
  const canvas = document.createElement('canvas'); canvas.width = 320; canvas.height = 64;
  const ctx = canvas.getContext('2d'); ctx.font = '25px Microsoft YaHei, sans-serif';
  ctx.fillStyle = '#0b182be6'; ctx.fillRect(0, 0, 320, 64);
  ctx.fillStyle = '#bed2e6'; ctx.textAlign = 'center'; ctx.fillText(text, 160, 41);
  const texture = new THREE.CanvasTexture(canvas);
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: texture, depthTest: false, transparent: true }));
  sprite.position.set(...position); sprite.scale.set(.020, .004, 1); group.add(sprite);
}

function disc(group, center, normal, radius, thickness, color, opacity = 1) {
  const item = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, thickness, 64),
    new THREE.MeshStandardMaterial({ color, metalness: opacity === 1 ? .55 : .1, roughness: .25,
      transparent: opacity < 1, opacity, depthWrite: opacity === 1 }));
  item.position.set(...center);
  item.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), new THREE.Vector3(...normal).normalize());
  group.add(item);
}

function ring(group, center, normal, inner, outer, color) {
  const item = new THREE.Mesh(new THREE.RingGeometry(inner, outer, 64),
    new THREE.MeshStandardMaterial({ color, side: THREE.DoubleSide, metalness: .6, roughness: .4 }));
  item.position.set(...center);
  item.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), new THREE.Vector3(...normal).normalize());
  group.add(item);
}

function drawHardware(payload) {
  dispose(hardware); if (!payload) return;
  for (const mirror of payload.mirrors) {
    disc(hardware, mirror.center, mirror.normal, mirror.radius, .0007, 0x8dacc4);
    ring(hardware, mirror.center, mirror.normal, mirror.radius * 1.03, mirror.radius * 1.18, 0x526880);
    const c = new THREE.Vector3(...mirror.center), a = new THREE.Vector3(...mirror.axis);
    line(hardware, [c.clone().addScaledVector(a, -.007).toArray(), c.clone().addScaledVector(a, .007).toArray()], 0xd4b77c);
    label(hardware, `${mirror.name} 振镜`, [c.x, c.y, c.z + .010]);
  }
  const entry = payload.entrance;
  ring(hardware, entry.center, entry.axis, entry.radius, entry.radius * 1.65, 0xc4a56d);
  label(hardware, '入射光阑 Ø4 mm', [entry.center[0] - .004, entry.center[1], entry.center[2] + .009]);
  const objective = payload.objective;
  disc(hardware, objective.center, objective.axis, objective.clear_aperture_radius, .001, 0x71c9f2, .35);
  ring(hardware, objective.center, objective.axis, objective.clear_aperture_radius, objective.clear_aperture_radius * 1.4, 0x486986);
  label(hardware, '等效聚焦镜组', [objective.center[0] + .015, objective.center[1], objective.center[2] + .003]);
  ring(hardware, [.01, 0, 0], [0, 0, 1], .00247, .0025, 0x46637a);
}

function drawPath(key, payload) {
  const group = paths[key]; dispose(group); if (!payload) return;
  const color = colors[key]; payload.segments.forEach(s => line(group, [s.start, s.end], color));
  group.add(new THREE.Points(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(...payload.pose.slice(0, 3))]),
    new THREE.PointsMaterial({ color, size: 4, sizeAttenuation: false, depthTest: false })));
  const obj = payload.objective, axis = new THREE.Vector3(...obj.axis);
  const side = new THREE.Vector3().crossVectors(axis, Math.abs(axis.z) < .9 ? new THREE.Vector3(0, 0, 1) : new THREE.Vector3(0, 1, 0)).normalize();
  const other = new THREE.Vector3().crossVectors(axis, side);
  for (const v of [side, side.clone().negate(), other, other.clone().negate()]) {
    line(group, obj.envelope.map(s => new THREE.Vector3(...s.position).addScaledVector(v, s.radius).toArray()), color, .4);
  }
}

async function post(path, body, signal) {
  const response = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal });
  const data = await response.json();
  if (!response.ok) throw Error(typeof data.detail === 'string' ? data.detail : '请求无效，请检查控制指令');
  return data;
}

function drawPlot(id, indices, type, unit, span) {
  const canvas = $(id), box = canvas.getBoundingClientRect(), dpr = Math.min(devicePixelRatio, 2);
  canvas.width = Math.max(1, Math.round(box.width * dpr)); canvas.height = Math.round(box.height * dpr);
  const ctx = canvas.getContext('2d'); ctx.scale(dpr, dpr);
  const w = box.width, h = box.height, cx = w / 2, cy = h / 2, r = Math.max(12, Math.min(w - 65, h - 46) / 2);
  ctx.strokeStyle = '#23394e'; ctx.lineWidth = 1;
  for (let i = -2; i <= 2; i++) {
    const k = r * i / 2; ctx.beginPath(); ctx.moveTo(cx - r, cy + k); ctx.lineTo(cx + r, cy + k);
    ctx.moveTo(cx + k, cy - r); ctx.lineTo(cx + k, cy + r); ctx.stroke();
  }
  ctx.fillStyle = '#8fa8bf'; ctx.font = '10px sans-serif'; ctx.textAlign = 'center';
  ctx.fillText(`−${span.toPrecision(3)}`, cx - r, cy + r + 16); ctx.fillText(`+${span.toPrecision(3)}`, cx + r, cy + r + 16);
  ctx.fillText('0', cx, cy + r + 16); ctx.fillText(id === 'ab' ? 'δα →' : 'ΔX →', cx + r, cy - 8);
  ctx.fillText(id === 'xy' ? 'ΔY ↑' : id === 'xz' ? 'ΔZ ↑' : 'δβ ↑', cx, cy - r - 9);
  ctx.strokeStyle = '#46d9ff'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(cx - 8, cy); ctx.lineTo(cx + 8, cy);
  ctx.moveTo(cx, cy - 8); ctx.lineTo(cx, cy + 8); ctx.stroke();
  const clippedNames = [];
  for (const [name, color] of [['before', '#ffad54'], ['after', '#63efae']]) {
    const values = current?.[`errors_${name}`]?.[type]; if (!values) continue;
    const x = values[indices[0]], y = values[indices[1]];
    const out = Math.abs(x) > span || Math.abs(y) > span;
    if (out) clippedNames.push(name === 'before' ? '未补偿' : '补偿后');
    const px = cx + Math.max(-1, Math.min(1, x / span)) * r, py = cy - Math.max(-1, Math.min(1, y / span)) * r;
    ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 1.5; ctx.setLineDash(name === 'after' ? [3, 3] : []);
    ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(px, py); ctx.stroke(); ctx.setLineDash([]);
    ctx.beginPath();
    if (name === 'before') { ctx.arc(px, py, 4, 0, Math.PI * 2); ctx.fill(); }
    else { ctx.moveTo(px, py - 6); ctx.lineTo(px + 6, py); ctx.lineTo(px, py + 6); ctx.lineTo(px - 6, py); ctx.closePath(); ctx.stroke(); }
  }
  if (clippedNames.length) {
    ctx.fillStyle = '#ffad54'; ctx.fillText(`${clippedNames.join('、')}超出图框`, cx, h - 2);
  }
  $(id + '-scale').textContent = `±${span.toPrecision(3)} ${unit}`;
}

function plots() {
  const selected = $('scale').value;
  const span = type => selected === 'residual' ? Math.max(1e-6,
    ...(current?.errors_after?.[type]?.map(Math.abs) ?? [1])) * 1.5 :
    selected === 'auto' ? Math.max(type === 'position_um' ? .1 : 1,
    ...['before', 'after'].flatMap(k => current?.[`errors_${k}`]?.[type]?.map(Math.abs) ?? [])) * 1.35 : Number(selected);
  const positionSpan = span('position_um');
  drawPlot('xy', [0, 1], 'position_um', 'μm', positionSpan); drawPlot('xz', [0, 2], 'position_um', 'μm', positionSpan);
  drawPlot('ab', [0, 1], 'angles_urad', 'μrad', span('angles_urad'));
}

function metrics() {
  const before = current?.errors_before, after = current?.errors_after;
  const fmt = v => v == null ? '—' : v !== 0 && Math.abs(v) < .001 ? v.toExponential(2) : v.toFixed(3);
  const rows = [['位置范数 μm', before?.position_norm_um, after?.position_norm_um],
    ['ΔX μm', before?.position_um[0], after?.position_um[0]], ['ΔY μm', before?.position_um[1], after?.position_um[1]],
    ['ΔZ μm', before?.position_um[2], after?.position_um[2]], ['姿态范数 μrad', before?.angle_norm_urad, after?.angle_norm_urad],
    ['δα μrad', before?.angles_urad[0], after?.angles_urad[0]], ['δβ μrad', before?.angles_urad[1], after?.angles_urad[1]]];
  $('metrics').innerHTML = rows.map(([name, a, b]) => `<tr><td>${name}</td><td class="orange">${fmt(a)}</td><td class="green">${fmt(b)}</td></tr>`).join('');
  const reduction = after && before.position_norm_um > 1e-12 ? 100 * (1 - after.position_norm_um / before.position_norm_um) : null;
  $('reduction').textContent = reduction == null ? '补偿后结果等待有效逆解' :
    `当前位置误差降低 ${reduction > 99.995 ? '>99.99' : reduction.toFixed(2)}%`;
  plots();
}

function renderCurrent() {
  Object.keys(paths).forEach(k => drawPath(k, current?.[k]));
  drawHardware(current?.[$('hardware').value]); applyView(); metrics();
}

function applyView() {
  const mode = $('view').value, optical = mode === 'optical';
  hardware.visible = optical;
  hardware.traverse(object => { if (object.isSprite) object.visible = $('labels').checked; });
  $('dimensions').disabled = optical || mode === 'motors';
  document.querySelectorAll('[data-path]').forEach(input => paths[input.dataset.path].visible = optical && input.checked);
  $('path-legend').hidden = !optical;
  grid.position.z = optical ? 0 : -.096;
  grid.scale.setScalar(optical ? .14 : 1);
  const payload = current?.[$('hardware').value];
  if (machineAssembly) updateAssembly(machineAssembly, {
    mode, payload, selected: $('motor').value, previewAngle: Number($('a5-preview').value) * Math.PI / 180,
    showDimensions: $('dimensions').checked, showLabels: $('labels').checked,
    showBeam: $('assembly-beam').checked && !optical,
  });
  $('beam-controls').hidden = optical;
  $('viewnote').textContent = optical ?
    '等效光路坐标 · 焦点固定 4 px · 此光路尚未按整机装配坐标辨识' :
    `${mode === 'exterior' ? '整机外观' : mode === 'focus' ? '聚焦特写' : mode === 'beam' ? '五镜光路透视' : mode === 'motors' ? '五轴装配特写' : '剖视'} · 假设光路，不是实机复原或下方补偿模型 · 光线穿透外壳显示`;
  motorDetails();
  updateFocusPanel();
  void refreshAssemblyTrace();
}

function updateFocusPanel() {
  const optical = $('view').value === 'optical', selected = $('hardware').value;
  const stateName = { target: '理想目标', before: '仿真未补偿', after: '仿真补偿后' }[selected];
  const frame = optical ? '原四镜 + qf · 等效光路坐标' : '五镜假设追迹 · 装配坐标';
  const payload = current?.[selected];
  const readout = commandPending ? null : optical ? payload?.readout : payload ? assemblyTrace?.readout : null;
  const fmt = value => Number.isFinite(value) ? (Math.abs(value) < .0000005 ? 0 : value).toFixed(6) : '—';
  ['x', 'y', 'z'].forEach((name, i) => $('focus-' + name).textContent = fmt(readout?.position_mm[i]));
  $('focus-aoi').textContent = fmt(readout?.aoi_deg);
  $('focus-rotz').textContent = fmt(readout?.rotz_deg);
  let status;
  if (commandPending) status = '指令更新中，等待新计算结果';
  else if (!payload) status = current?.message ?? '没有有效计算结果';
  else if (!readout) status = optical ? '读数不可用，请检查计算服务' : assemblyTrace?.chief.message ?? '追迹中或追迹不可用';
  else status = readout.rotz_defined ? '有效焦点' : '有效焦点 · 垂直入射，RotZ 无定义';
  if (readout && !optical && assemblyTrace.transmitted_rays < assemblyTrace.total_marginal_rays)
    status += ` · 部分边缘光线被截断（${assemblyTrace.transmitted_rays}/8 通过）`;
  $('focus-status').textContent = `${frame} / ${stateName} · ${status}`;
  $('focus-status').className = readout ? '' : 'invalid';
}

let lastTraceKey = '';
async function refreshAssemblyTrace() {
  if (!machineAssembly) return;
  const payload = commandPending ? null : current?.[$('hardware').value];
  if (!payload) {
    ++traceSequence; traceRequest?.abort(); lastTraceKey = ''; assemblyTrace = null;
    drawAssemblyBeam(machineAssembly, null, 0); $('beam-status').textContent = '当前选定状态无有效指令，不显示旧光路。'; updateFocusPanel(); return;
  }
  const angles = [...payload.mirror_angles, Number($('a5-preview').value) * Math.PI / 180];
  const key = JSON.stringify(angles);
  if (key === lastTraceKey) { renderAssemblyTrace(); return; }
  lastTraceKey = key; const token = ++traceSequence; traceRequest?.abort(); traceRequest = new AbortController();
  assemblyTrace = null; drawAssemblyBeam(machineAssembly, null, 0); $('beam-status').textContent = '正在追迹五面镜…';
  updateFocusPanel();
  try {
    const result = await post('/api/assembly/trace', { angles }, traceRequest.signal);
    if (token !== traceSequence) return;
    assemblyTrace = result; renderAssemblyTrace();
  } catch (error) {
    if (token !== traceSequence || error.name === 'AbortError') return;
    lastTraceKey = ''; $('beam-status').textContent = `追迹失败：${error.message}`; updateFocusPanel();
  }
}

function renderAssemblyTrace() {
  if (!assemblyTrace) { updateFocusPanel(); return; }
  const step = Number($('beam-step').value);
  drawAssemblyBeam(machineAssembly, assemblyTrace, step, Number($('beam-width').value));
  const s = assemblyTrace.chief.segments[Math.max(0, step - 1)];
  $('beam-status').textContent = `${assemblyTrace.chief.message} · 边缘光线 ${assemblyTrace.transmitted_rays}/8 通过` +
    (step ? `\n第 ${step} 段：${s?.stage ?? '前级已打偏，未到达本段'}` : '\n金色：反射路径 · 蓝色：入物镜 · 绿色：会聚 · 红色：打偏');
  updateFocusPanel();
}

function motorDetails() {
  const index = Number($('motor').value), payload = current?.[$('hardware').value];
  const config = machineAssembly?.config; if (!config) return;
  const m = config.motors[index], d = config.dimensions;
  const center = m.mirror_center.map(x => (x * 1000).toFixed(1)).join(', ');
  const angle = index === 4 ? Number($('a5-preview').value) : (payload?.mirror_angles?.[index] ?? 0) * 180 / Math.PI;
  $('motor-info').textContent = `镜心（装配）：[${center}] mm\n` +
    `转轴：[${m.axis.map(x => x.toFixed(3)).join(', ')}] · 壳体 Ø${d.motor_radius * 2000} × ${d.motor_length * 1000} mm\n` +
    `当前转角：${angle.toFixed(4)}°${index === 4 ? '（假设光路）' : payload ? '（求解器状态）' : '（无有效解，零位示意）'}\n` +
    (index === 4 ? 'A5 参与假设光路追迹，不参与下方补偿；不是实机调焦模型。' : '转角共用；五镜演示用装配几何追迹，下方补偿仍用原四镜模型。');
  $('a5-row').hidden = index !== 4;
}

async function refresh() {
  const token = ++sequence; pending?.abort(); pending = new AbortController();
  try {
    const data = await post('/api/compare', { q: [...params] }, pending.signal); if (token !== sequence) return;
    commandPending = false; current = data; renderCurrent(); $('message').textContent = data.message; $('message').className = data.after ? '' : 'error';
    if (!training) $('training').textContent = data.fitted ? '补偿模型已就绪，可拖动滑块观察。' : '尚未训练';
    if (!data.fitted && !autoAttempted) { autoAttempted = true; void train(); }
  } catch (error) {
    if (token !== sequence || error.name === 'AbortError') return;
    commandPending = false; current = null; renderCurrent(); $('message').textContent = `当前光路无效：${error.message}`; $('message').className = 'error';
  }
}

function schedule() {
  clearTimeout(timer); ++sequence; pending?.abort();
  commandPending = true; ++traceSequence; traceRequest?.abort(); lastTraceKey = ''; assemblyTrace = null;
  if (machineAssembly) drawAssemblyBeam(machineAssembly, null, 0);
  updateFocusPanel(); timer = setTimeout(refresh, 100);
}
const inputs = [];
['q1', 'q2', 'q3', 'q4', 'qf'].forEach((name, index) => {
  const row = document.createElement('label'); row.className = 'control';
  row.innerHTML = `<span>${name}</span><input aria-label="${name}" type="range" min="${index < 4 ? -3.75 : 74}" max="${index < 4 ? 3.75 : 76}" step="${index < 4 ? .005 : .001}" value="${index < 4 ? 0 : 75}"><output>${index < 4 ? '0.000°' : '75.000 mm'}</output>`;
  const input = row.querySelector('input'); inputs.push(input);
  input.addEventListener('input', () => {
    const v = Number(input.value); params[index] = index < 4 ? v * Math.PI / 180 : v / 1000;
    row.querySelector('output').textContent = v.toFixed(3) + (index < 4 ? '°' : ' mm'); schedule();
  }); $('controls').append(row);
});

async function train() {
  if (training) return; training = true; $('calibrate').disabled = true;
  $('training').textContent = '正在生成 400 个标定点并独立验证…';
  try {
    const result = await post('/api/calibrate', { sample_count: 400, seed: 42 }); await refresh();
    $('training').textContent = `训练完成 · ${result.sample_count}/${result.requested_validation_samples} 个验证点成功\n位置 RMSE ${(result.position_rmse_before * 1e6).toFixed(3)} → ${(result.position_rmse_after * 1e6).toFixed(3)} μm`;
  } catch (e) { $('training').textContent = `训练失败：${e.message}`; }
  finally { training = false; $('calibrate').disabled = false; }
}

$('calibrate').onclick = train; $('home').onclick = home;
$('reset').onclick = () => {
  $('a5-preview').value = 0; $('a5-value').textContent = '0.00°';
  params = [0, 0, 0, 0, .075]; inputs.forEach((input, i) => {
    input.value = i < 4 ? 0 : 75; input.parentElement.querySelector('output').textContent = i < 4 ? '0.000°' : '75.000 mm';
  }); schedule();
};
$('hardware').onchange = () => { drawHardware(current?.[$('hardware').value]); applyView(); }; $('scale').onchange = plots;
$('view').onchange = () => { applyView(); home(); };
for (const id of ['motor', 'dimensions', 'labels', 'assembly-beam']) $(id).onchange = applyView;
$('beam-step').onchange = renderAssemblyTrace;
$('beam-width').onchange = renderAssemblyTrace;
$('beam-next').onclick = () => { $('beam-step').value = (Number($('beam-step').value) + 1) % 9; renderAssemblyTrace(); };
$('a5-preview').oninput = () => { $('a5-value').textContent = `${Number($('a5-preview').value).toFixed(2)}°`; applyView(); };
document.querySelectorAll('[data-path]').forEach(input => input.onchange = applyView);
fetch('/api/assembly').then(r => { if (!r.ok) throw Error(`HTTP ${r.status}`); return r.json(); }).then(config => {
  machineAssembly = buildAssembly(config); scene.add(machineAssembly.root);
  const d = config.dimensions;
  $('envelope').textContent = `${(d.width * 1000).toFixed(1)} × ${(d.depth * 1000).toFixed(1)} × ${(d.height * 1000).toFixed(0)} mm`;
  applyView();
}).catch(e => { $('envelope').textContent = `结构读取失败：${e.message}`; });
fetch('/api/specifications').then(r => r.json()).then(s => {
  $('specs').textContent = `${s.profile_name} · 入射光束 ${(s.entrance_beam_diameter_m * 1000).toFixed(1)} mm · M²=${s.beam_quality_m2} · 典型焦斑 ${(s.typical_focus_diameter_m * 1e6).toFixed(1)} μm · AOI ±7.5° · Z ±1 mm · 有效焦距 25 mm`;
}).catch(() => $('specs').textContent = '规格读取失败');
new ResizeObserver(() => {
  const w = stage.clientWidth, h = stage.clientHeight;
  camera.aspect = w / h; camera.updateProjectionMatrix(); renderer.setSize(w, h); home(); plots();
}).observe(stage);
addEventListener('resize', plots);
renderer.setAnimationLoop(() => { orbit.update(); renderer.render(scene, camera); });
metrics(); refresh();
