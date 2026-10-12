import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';

const $ = id => document.getElementById(id);
const scene = new THREE.Scene(); scene.background = new THREE.Color('#0b1420');
const renderer = new THREE.WebGLRenderer({antialias:true}); renderer.setPixelRatio(Math.min(devicePixelRatio,2));
$('stage').appendChild(renderer.domElement);
const camera = new THREE.PerspectiveCamera(43,1,.0002,5); camera.up.set(0,0,1);
const orbit = new OrbitControls(camera,renderer.domElement); orbit.enableDamping=true;
scene.add(new THREE.HemisphereLight(0xc9eaff,0x284452,2.4));
const light = new THREE.DirectionalLight(0xffffff,3); light.position.set(.3,-.2,.5); scene.add(light);
const hardware = new THREE.Group(), beams = new THREE.Group(), shell = new THREE.Group();scene.add(hardware,beams,shell);
const q = [0,0,0,0,0], tags=[]; let response=null, pending=false, serial=0, abort=null, timer=null;
let targetMode=false;
const targetIds=['target-x','target-y','target-z','target-alpha','target-beta'];
const v = a => new THREE.Vector3(...a);
const material = (color,opacity=1) => new THREE.MeshStandardMaterial({color,metalness:.38,roughness:.35,transparent:opacity<1,opacity,side:THREE.DoubleSide});

function clear(group){while(group.children.length){const child=group.children[0];group.remove(child);child.traverse(o=>{o.geometry?.dispose();if(Array.isArray(o.material))o.material.forEach(m=>m.dispose());else o.material?.dispose();});}}
function box(parent,center,size,color,opacity=1){const mesh=new THREE.Mesh(new THREE.BoxGeometry(...size),material(color,opacity));mesh.position.copy(v(center));parent.add(mesh);return mesh;}
function cylinder(parent,center,axis,radius,length,color){const mesh=new THREE.Mesh(new THREE.CylinderGeometry(radius,radius,length,40),material(color));mesh.position.copy(v(center));mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),v(axis).normalize());parent.add(mesh);return mesh;}
function ring(parent,center,normal,inner,outer,color){const mesh=new THREE.Mesh(new THREE.RingGeometry(inner,outer,48),material(color));mesh.position.copy(v(center));mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,0,1),v(normal));parent.add(mesh);}
function line(parent,points,color,opacity=1){const mesh=new THREE.Line(new THREE.BufferGeometry().setFromPoints(points.map(v)),new THREE.LineBasicMaterial({color,transparent:opacity<1,opacity}));parent.add(mesh);}
function label(text,point){const el=document.createElement('span');el.className='tag';el.textContent=text;$('labels').appendChild(el);tags.push({el,point:v(point)});}
function setView(){const view=$('view').value;const views={overview:[[.46,-.28,.35],[.15,.125,.045]],top:[[.155,.132,.52],[.155,.132,.04]],focus:[[-.055,-.05,.135],[.040,.06,.06]],work:[[.41,.045,.075],[.275,.20,-.015]]};camera.position.copy(v(views[view][0]));orbit.target.copy(v(views[view][1]));orbit.update();}
function makeShell(){const geom=new THREE.BoxGeometry(.310,.264,.271);const edges=new THREE.LineSegments(new THREE.EdgesGeometry(geom),new THREE.LineBasicMaterial({color:0x395c72}));geom.dispose();edges.position.set(.155,.132,.1355);shell.add(edges);}
makeShell();setView();

function draw(payload){
  clear(hardware);clear(beams);$('labels').replaceChildren();tags.length=0;
  if(!payload)return;
  for(const solid of payload.solids)cylinder(hardware,solid.center,solid.axis,solid.radius,solid.length,({motor:0x327598,encoder:0x172d42,shaft:0x9aaebd,backing:0x586d7c})[solid.role]);
  for(const s of payload.surfaces){
    const mesh=new THREE.Mesh(new THREE.CircleGeometry(s.radius,48),material(s.kind==='lens'?0x73dccc:0xc8e4f1,s.kind==='lens'?.40:1));mesh.position.copy(v(s.center));mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,0,1),v(s.normal));hardware.add(mesh);
    if(s.kind==='lens')ring(hardware,s.center,s.normal,s.radius,s.radius+.0018,s.name.startsWith('L1')?0xe5ab58:0x697f91);
    label(s.name,[s.center[0],s.center[1],s.center[2]+.016]);
  }
  for(const part of payload.supports)box(hardware,part.center,part.size,part.name.startsWith('Z5')?0xb68e56:0x405e73,part.name.startsWith('基板')?.65:1);
  label('Z5 直线导轨 / 位移反馈',[.020,.028,.038]);
  box(hardware,[.275,.20,-.062],[.026,.026,.002],0x68848d,.7);
  const f=payload.focus_world;
  for(let i=0;i<3;i++){const a=[...f],b=[...f];a[i]-=.001;b[i]+=.001;line(hardware,[a,b],0xffe4a2);}
  label('计算焦点 · 十字标记',[f[0]+.009,f[1],f[2]]);
  const step=Number($('step').value);
  if($('show-beam').checked)payload.paths.forEach((path,index)=>{const points=step?path.slice(step-1,step+1):path;line(beams,points,index===0?0xe3ffb4:0x60e5bd,index===0?1:.45);});
  $('carriage').style.left=`calc(${50+payload.z5_actual_displacement_m/.00065*44}% - 5px)`;
  const collision=payload.collisions.length?`遮挡：${payload.collisions.join('、')}`:'当前 9 条采样光线未与受检电机 / 侧轴 / 镜背板 / 支承相交';
  $('trace-status').textContent=`${collision}\nZ5 实际镜片位移 ${(payload.z5_actual_displacement_m*1000).toFixed(4)} mm → 焦点 Z ${(payload.pose[2]*1000).toFixed(6)} mm\n几何弥散 RMS ${payload.geometric_rms_um.toFixed(4)} μm（不含衍射）；检查不覆盖压圈厚度、外壳、线缆、公差与完整连续束体。`;
  $('trace-status').classList.toggle('warning',payload.collisions.length>0);
}

function show(){
  const selected=pending?null:response?.[$('state').value];
  ['x','y','z','aoi','rotz'].forEach((id,i)=>{let value=null;if(selected){const r=selected.readout;value=i<3?r.position_mm[i]:i===3?r.aoi_deg:r.rotz_deg;}$(id).textContent=value==null?'—':value.toFixed(6);});
  draw(selected);
  if(!selected)$('trace-status').textContent=pending?'正在计算新指令，旧读数已清空…':'当前状态无有效结果，请训练补偿或减小指令。';
  if(response&&!pending){$('message').textContent=response.message;renderErrors();if(response.mode==='inverse')renderInverse(response);}
}

function fillTable(id,rows){
  $(id).replaceChildren(...rows.map(row=>{const tr=document.createElement('tr');for(const value of row){const td=document.createElement('td');td.textContent=value;tr.append(td);}return tr;}));
}

function renderInverse(data){
  const keys=['baseline','truth','calibrated'],branches=keys.map(key=>data?.branches[key]);
  const number=(value)=>value==null?'—':value.toFixed(6);
  fillTable('inverse-commands',['A1 / °','A2 / °','A3 / °','A4 / °','Z5 / mm'].map((name,i)=>[name,...branches.map(b=>number(b?.success?b.command[i]*(i<4?180/Math.PI:1000):null))]));
  const rows=['X / mm','Y / mm','Z / mm','α / °','β / °'].map((name,i)=>[name,...branches.map(b=>number(b?.payload?b.payload.pose[i]*(i<3?1000:180/Math.PI):null))]);
  rows.push(['空间残差 / μm',...branches.map(b=>number(b?.errors?.norm_um))]);
  rows.push(['角度残差 / μrad',...branches.map(b=>number(b?.errors?Math.hypot(...b.errors.angles_urad):null))]);
  fillTable('inverse-poses',rows);
  $('inverse-status').textContent=data?branches.map((b,i)=>`${['未校准模型','真实模型参考','校准后模型'][i]}：${b.message}${b.success?`（${b.iterations} 次函数评估）`:''}`).join('\n'):'';
  if(data)$('inverse-message').textContent=`已计算目标：XYZ [${data.requested_pose.slice(0,3).map(x=>(x*1000).toFixed(6)).join(', ')}] mm；αβ [${data.requested_pose.slice(3).map(x=>(x*180/Math.PI).toFixed(6)).join(', ')}] °。${data.fitted?'':'校准组尚未标定。'}`;
}

function invalidate(){
  ++serial;abort?.abort();response=null;pending=true;show();renderInverse(null);
  $('errors').replaceChildren();$('error-plot').getContext('2d').clearRect(0,0,$('error-plot').width,$('error-plot').height);
  $('message').textContent='目标或指令已变化，旧结果已清空。';
}

function renderErrors(){
  const b=response.errors_before,a=response.errors_after;
  const rows=[['空间误差 / μm',b?.norm_um,a?.norm_um],...['X','Y','Z'].map((n,i)=>[`${n} 误差 / μm`,b?.position_um[i],a?.position_um[i]]),...['α','β'].map((n,i)=>[`${n} 误差 / μrad`,b?.angles_urad[i],a?.angles_urad[i]])];
  $('errors').replaceChildren(...rows.map(row=>{const tr=document.createElement('tr');row.forEach((value,i)=>{const td=document.createElement('td');td.textContent=i===0?value:value==null?'—':value.toFixed(5);tr.append(td);});return tr;}));
  const c=$('error-plot'),rect=c.getBoundingClientRect(),dpr=devicePixelRatio;c.width=rect.width*dpr;c.height=180*dpr;const ctx=c.getContext('2d');ctx.scale(dpr,dpr);const w=rect.width,h=180,cx=w/2,cy=h/2;
  const points=[{p:b?.position_um,color:'#ffad54',label:'补偿前'},{p:a?.position_um,color:'#63efae',label:'补偿后'}].filter(item=>item.p);
  const range=Math.max(1,...points.flatMap(({p})=>[Math.abs(p[0]),Math.abs(p[2])]))*1.4;const scale=Math.min(w/2-40,h/2-30)/range;
  ctx.strokeStyle='#335268';ctx.beginPath();ctx.moveTo(15,cy);ctx.lineTo(w-15,cy);ctx.moveTo(cx,12);ctx.lineTo(cx,h-15);ctx.stroke();ctx.fillStyle='#98b3c5';ctx.font='11px sans-serif';ctx.fillText(`±${range.toFixed(2)} μm`,10,17);ctx.fillText('X',w-25,cy-8);ctx.fillText('Z',cx+8,20);
  ctx.strokeStyle='#67dbf3';ctx.strokeRect(cx-4,cy-4,8,8);
  points.forEach(({p,color,label},i)=>{const x=cx+p[0]*scale,y=cy-p[2]*scale;ctx.strokeStyle=ctx.fillStyle=color;ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(x,y);ctx.stroke();ctx.beginPath();ctx.arc(x,y,i?3:4,0,2*Math.PI);ctx.fill();ctx.fillText(label,x+8,y+(i?15:-7));});
}

async function api(path,body,signal){const res=await fetch('/api/4p1/'+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),signal});const data=await res.json();if(!res.ok)throw Error(typeof data.detail==='string'?data.detail:JSON.stringify(data.detail));return data;}
async function update(){
  invalidate();const id=serial;abort=new AbortController();
  if(targetMode&&!$('inverse-form').reportValidity()){pending=false;show();$('inverse-message').textContent='请填写全部目标值，并检查输入范围。';return;}
  const path=targetMode?'inverse':'compare';
  const body=targetMode?{pose:targetIds.map((name,i)=>Number($(name).value)*(i<3?.001:Math.PI/180))}:{q:[...q]};
  if(targetMode)$('inverse-message').textContent='正在逆解三组模型，尚未向任何硬件发送指令…';
  try{
    const result=await api(path,body,abort.signal);if(id!==serial)return;response=result;pending=false;
    if(result.mode==='inverse'){
      const baseline=result.branches.baseline;
      if(baseline.success){q.splice(0,5,...baseline.command);syncControls();}
      if($('state').value==='target')$('state').value=result.after?'after':'before';
    }
    show();
  }
  catch(e){if(id!==serial||e.name==='AbortError')return;pending=false;response=null;show();$('message').textContent=e.message;$('trace-status').textContent=`光路无效：${e.message}`;if(targetMode)$('inverse-message').textContent=e.message;}
}
function syncControls(){q.forEach((value,i)=>{const displayed=i<4?value*180/Math.PI:value*1000;$('q'+i).value=displayed;$('out'+i).textContent=displayed.toFixed(i<4?3:4)+(i<4?'°':' mm');});}
for(let i=0;i<5;i++){const labelEl=document.createElement('label');labelEl.className='control';labelEl.innerHTML=`<span>${i<4?'A'+(i+1):'Z5'}</span><input id="q${i}" aria-label="${i<4?'A'+(i+1):'Z5'}" type="range" min="${i<4?-.8:-.65}" max="${i<4?.8:.65}" step="${i<4?.001:.0005}" value="0"><output id="out${i}"></output>`;$('controls').append(labelEl);$('q'+i).oninput=()=>{targetMode=false;q[i]=Number($('q'+i).value)*(i<4?Math.PI/180:.001);syncControls();clearTimeout(timer);invalidate();$('inverse-message').textContent='已切换为轴指令正向计算；手动目标尚未重新逆解。';timer=setTimeout(update,90);};}
syncControls();
const notes=['入射 → 移动负透镜 → 固定准直镜 → 四振镜 → 折转镜 → 固定物镜 → 聚焦。Z5 改变前置镜组间距，四振镜共同控制 XY 与入射方向。','入口为直径 2 mm 的平行采样光束；L1 沿光轴平移。','负透镜使光束发散，L2 名义上准直并扩束 3×；间距变化产生正 / 负会聚度。','调焦后的光束进入四镜组，平面反射不凭空产生光焦度。','第一镜对改变光束的位置与走向。','两镜对之间保留传播距离，形成位置与方向的独立控制杠杆。','第二镜对与第一镜对共同决定 XY、α、β；不是每面镜只控制一个工件坐标。','四镜输出经固定折转镜转向工件。','物镜固定，接收随 Z5 改变的入射会聚度。','在物镜后寻找瞳边缘光线位置方差最小的水平面；主光线与该平面的交点作为焦点。'];
function stepChanged(){$('step-note').textContent=notes[Number($('step').value)];show();}
$('step').onchange=stepChanged;$('next').onclick=()=>{$('step').value=(Number($('step').value)+1)%10;stepChanged();};
$('state').onchange=show;$('view').onchange=setView;$('show-beam').onchange=show;$('show-shell').onchange=()=>shell.visible=$('show-shell').checked;$('show-tags').onchange=()=>$('labels').hidden=!$('show-tags').checked;
$('reset').onclick=()=>{targetMode=false;clearTimeout(timer);q.fill(0);syncControls();update();};
$('z-demo').onclick=()=>{targetMode=false;clearTimeout(timer);q.fill(0);q[4]=.0005;syncControls();$('view').value='focus';setView();update();};
$('tilt-demo').onclick=()=>{targetMode=false;clearTimeout(timer);q.splice(0,5,.002,-.001,-.001,.001,0);syncControls();update();};
async function trainCalibration(){
  $('calibrate').disabled=$('train-target').disabled=true;$('training').textContent='正在训练与独立验证…';
  try{const m=await api('calibrate',{});$('training').textContent=`独立验证 ${m.sample_count}/${m.requested_validation_samples} 点；失败 ${m.failed_validation_samples} 点\n位置 RMSE ${(m.position_rmse_before*1e6).toFixed(4)} → ${(m.position_rmse_after*1e6).toFixed(4)} μm\n角度 RMSE ${(m.orientation_rmse_before*1e6).toFixed(4)} → ${(m.orientation_rmse_after*1e6).toFixed(4)} μrad\n仅确定性仿真，无测量噪声，不代表实机指标。`;$('state').value='after';await update();}
  catch(e){$('training').textContent=e.message;$('inverse-message').textContent=`标定失败：${e.message}`;}
  finally{$('calibrate').disabled=$('train-target').disabled=false;}
}
$('calibrate').onclick=trainCalibration;
$('train-target').onclick=()=>{if(!$('inverse-form').reportValidity())return;clearTimeout(timer);targetMode=true;trainCalibration();};
$('inverse-form').onsubmit=e=>{e.preventDefault();clearTimeout(timer);targetMode=true;update();};
for(const id of targetIds)$(id).oninput=()=>{clearTimeout(timer);targetMode=true;invalidate();pending=false;show();$('inverse-message').textContent='目标已修改，点击逆解重新计算；旧指令已失效。';};
$('copy-target').onclick=()=>{
  const pose=response?.requested_pose??response?.target?.pose;
  if(!pose){$('inverse-message').textContent='当前没有有效理想位姿，请先完成一次正向计算。';return;}
  targetIds.forEach((id,i)=>$(id).value=(pose[i]*(i<3?1000:180/Math.PI)).toFixed(9));
  targetMode=true;invalidate();pending=false;show();$('inverse-message').textContent='已填入当前目标位姿，点击逆解计算三组指令。';
};
renderInverse(null);
new ResizeObserver(()=>{const r=$('stage').getBoundingClientRect();renderer.setSize(r.width,r.height);camera.aspect=r.width/r.height;camera.updateProjectionMatrix();if(response&&!pending)renderErrors();}).observe($('stage'));
function animate(){
  requestAnimationFrame(animate);orbit.update();renderer.render(scene,camera);
  const width=$('stage').clientWidth,height=$('stage').clientHeight,occupied=[];
  for(const tag of tags){
    const p=tag.point.clone().project(camera);
    tag.el.hidden=p.z>1||p.z<-1||Math.abs(p.x)>1||Math.abs(p.y)>1;
    if(tag.el.hidden)continue;
    const w=tag.el.offsetWidth,h=tag.el.offsetHeight;
    const x=Math.max(5,Math.min(width-w-5,(p.x+1)*.5*width));
    let y=Math.max(48,Math.min(height-125,(1-p.y)*.5*height));
    for(let attempt=0;attempt<tags.length;attempt++){
      const overlap=occupied.find(r=>x<r.x+r.w+4&&x+w+4>r.x&&y<r.y+r.h+3&&y+h+3>r.y);
      if(!overlap)break;
      y=overlap.y+overlap.h+4;
    }
    occupied.push({x,y,w,h});tag.el.style.left=`${x}px`;tag.el.style.top=`${y}px`;
  }
}
stepChanged();animate();update();
