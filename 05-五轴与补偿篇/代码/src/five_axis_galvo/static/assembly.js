import * as THREE from 'three';

const palette = [0x53d0e5, 0x7eacf8, 0xb2a0f0, 0xefba6d, 0xf28a9c];
const v = a => new THREE.Vector3(...a);

function box(group, size, center, color, metalness = .4) {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(...size),
    new THREE.MeshStandardMaterial({ color, metalness, roughness: .4 }));
  mesh.position.set(...center); group.add(mesh); return mesh;
}

function cylinder(group, center, axis, radius, length, color, topRadius = radius) {
  const mesh = new THREE.Mesh(new THREE.CylinderGeometry(topRadius, radius, length, 40),
    new THREE.MeshStandardMaterial({ color, metalness: .65, roughness: .3 }));
  mesh.position.set(...center);
  mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), v(axis).normalize());
  group.add(mesh); return mesh;
}

function tube(group, points, radius, color) {
  const curve = new THREE.CatmullRomCurve3(points.map(v), false, 'catmullrom', .1);
  const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, 24, radius, 8, false),
    new THREE.MeshStandardMaterial({ color, roughness: .55 }));
  group.add(mesh); return mesh;
}

function wire(group, points, color = 0x57758e) {
  group.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(points.map(v)),
    new THREE.LineBasicMaterial({ color })));
}

function text(group, value, position, width = .115) {
  const canvas = document.createElement('canvas'); canvas.width = Math.max(84, value.length * 27 + 24); canvas.height = 54;
  const ctx = canvas.getContext('2d'); ctx.fillStyle = '#0a172de8'; ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#d7e7f5'; ctx.font = '26px Microsoft YaHei,sans-serif'; ctx.textAlign = 'center';
  ctx.fillText(value, canvas.width / 2, 36);
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
    map: new THREE.CanvasTexture(canvas), depthTest: false, transparent: true,
  }));
  sprite.position.set(...position); sprite.scale.set(width, width * canvas.height / canvas.width, 1);
  sprite.userData.baseScale = sprite.scale.clone(); sprite.userData.basePosition = sprite.position.clone(); group.add(sprite);
}

function dimension(group, a, b, value, position) {
  wire(group, [a, b], 0x75a5bf);
  for (const p of [a, b]) cylinder(group, p, [0, 0, 1], .0017, .004, 0x75a5bf);
  text(group, value, position);
}

export function buildAssembly(config) {
  const d = config.dimensions, root = new THREE.Group();
  const chassis = new THREE.Group(), covers = new THREE.Group(), electronics = new THREE.Group();
  const modules = new THREE.Group(), motors = new THREE.Group(), annotations = new THREE.Group();
  const motorLabels = new THREE.Group(), endPanel = new THREE.Group();
  const dimensions = new THREE.Group(), cabling = new THREE.Group();
  root.add(chassis, covers, electronics, modules, motors, annotations, motorLabels, endPanel, dimensions, cabling);
  const t = d.panel_thickness, W = d.width, D = d.depth, H = d.height;

  box(chassis, [D, W, t], [D / 2, 0, t / 2], 0x647a8e);
  box(chassis, [D, t, H], [D / 2, W / 2 - t / 2, H / 2], 0xa1b1bf);
  box(chassis, [t, W, H], [t / 2, 0, H / 2], 0x8397a9);
  box(endPanel, [t, W, H], [D - t / 2, 0, H / 2], 0x8fa2b4);
  box(covers, [D, t, H], [D / 2, -W / 2 + t / 2, H / 2], 0xb4c3d0);
  box(covers, [D, W, t], [D / 2, 0, H - t / 2], 0xb4c3d0);
  for (const x of [.008, D - .008]) for (const y of [-W / 2 + .008, W / 2 - .008]) {
    box(chassis, [.010, .010, H], [x, y, H / 2], 0x42586a);
  }
  for (const x of [.012, D / 2, D - .012]) for (const z of [.014, H - .014]) {
    cylinder(covers, [x, -W / 2 - .0002, z], [0, 1, 0], .0028, .002, 0x243546);
  }
  for (const y of [-.09, .09]) {
    tube(covers, [[.035, y, H], [.065, y, H + d.handle_rise - .005],
      [.19, y, H + d.handle_rise - .005], [.22, y, H]], .005, 0x778c9e);
  }

  box(electronics, [D - .014, W - .014, .008], [D / 2, 0, d.compartment_split_z], 0x536b7f);
  box(electronics, [.104, .115, .042], [.072, .045, .190], 0x364e61);
  box(electronics, [.105, .108, .004], [.193, .045, .180], 0x287964);
  for (let i = 0; i < 5; i++) {
    box(electronics, [.088, .021, .018], [.178, -.097 + i * .036, .207], 0x243e50);
    box(electronics, [.012, .014, .006], [.234, -.097 + i * .036, .187], palette[i]);
  }
  for (let i = 0; i < 9; i++) box(electronics, [.004, .103, .016], [.03 + i * .01, .045, .219], 0x7892a5);

  const states = [];
  config.motors.forEach((motor, index) => {
    const unit = new THREE.Group(); motors.add(unit);
    const c = v(motor.mirror_center), a = v(motor.axis), b = v(motor.body_center);
    const along = distance => c.clone().addScaledVector(a, distance).toArray();
    const color = palette[index];
    const body = cylinder(unit, b.toArray(), motor.axis, d.motor_radius, d.motor_length, 0x344b61);
    const shaft = motor.shaft_length;
    for (const distance of [shaft, shaft + d.motor_length]) {
      cylinder(unit, along(distance), motor.axis, d.motor_radius * 1.1, .003, color);
    }
    cylinder(unit, along(shaft + d.motor_length + d.encoder_length / 2),
      motor.axis, d.motor_radius * .91, d.encoder_length, 0x172b3d);
    // The drive stub is drawn only over the span the backend verified, never closer to the mirror:
    // the beam crosses the rotation axis at the mirror centre by definition, so a co-axial solid
    // there is inside the beam. Everything drawn here must also appear in the backend's
    // rendered_solids(), or it is unverified geometry.
    const [stubNear, stubFar] = motor.stub_span ?? [shaft - .0024, shaft];
    cylinder(unit, along((stubNear + stubFar) / 2), motor.axis, motor.stub_radius ?? .0012,
      stubFar - stubNear, 0x93a5b6);
    // Pedestal: on the deck under the barrel, rising to the height the backend sized for it. The
    // long shaft is what keeps the barrel out of the beam, so the mount has to reach that far back
    // rather than hug the mirror.
    const deck = d.panel_thickness + .001;
    const underside = motor.mount_top_z ?? b.z - d.motor_radius;
    box(unit, [.036, .042, .005], [b.x, b.y, deck + .0025], 0x6c8293);
    if (underside > deck + .006) {
      box(unit, [.026, .032, underside - deck - .004],
        [b.x, b.y, (deck + .004 + underside) / 2], 0x536c82);
    }
    for (const dx of [-.013, .013]) for (const dy of [-.016, .016]) {
      cylinder(unit, [b.x + dx, b.y + dy, deck + .006], [0, 0, 1], .0017, .002, 0x263c50);
    }
    const rotor = new THREE.Group(); rotor.position.copy(c); unit.add(rotor);
    cylinder(rotor, v(motor.base_normal).multiplyScalar(-.0012).toArray(), motor.base_normal, d.mirror_radius + .0008, .002, color);
    const faceCenter = v(motor.base_normal).multiplyScalar(-.00015).toArray();
    cylinder(rotor, faceCenter, motor.base_normal, d.mirror_radius, .0003, 0xd1e5f3);
    wire(rotor, [[0, 0, 0], v(motor.base_normal).multiplyScalar(.014).toArray()], color);
    const labelPoint = [c.x, c.y, c.z + .026];
    text(motorLabels, `${motor.id}${index === 4 ? ' · 待辨识' : ''}`, labelPoint, index === 4 ? .063 : .029);
    wire(motorLabels, [c.toArray(), [c.x, c.y, c.z + .020]], color);
    const end = along(shaft + d.motor_length + d.encoder_length);
    tube(cabling, [end, [end[0], end[1], .113], [.23, end[1], .118], [.24, .1, .123]], .0018, color);
    states.push({ rotor, axis: a, body, center: c, color });
  });

  for (const [z, color] of [[.023, 0x3999b4], [.150, 0x747bd2]]) {
    tube(cabling, [[.009, .13, z], [.045, .13, z], [.225, .13, z], [.244, .10, z],
      [.244, -.11, z], [.05, -.12, z], [.009, -.12, z]], .003, color);
    for (const y of [.13, -.12]) cylinder(modules, [-.009, y, z], [1, 0, 0], .006, .018, 0xc3a969);
  }
  const ex = d.exit_axis_x, ey = d.exit_axis_y;
  box(modules, [.083, .105, .125], [D + .0415, ey, .0655], 0x8199ac);
  box(modules, [.007, .109, .131], [D + .0865, ey, .0655], 0x536e85);
  box(modules, [D + d.side_extension - (D + .09), .118, .130],
    [(D + .09 + D + d.side_extension) / 2, ey, .0655], 0xb0c1ce);
  cylinder(modules, [ex, ey, -.009], [0, 0, 1], d.exit_flange_diameter / 2, .018, 0x647f95);
  cylinder(modules, [ex, ey, -.025], [0, 0, 1], d.exit_neck_diameter / 2, .014, 0xb6c9d5);
  box(modules, [.094, .089, .008], [ex, ey - .004, -.017], 0x90a9bc);
  box(modules, [.028, .009, .012], [ex, ey - .052, -.017], 0x283e51);
  cylinder(modules, [ex, ey, -.039], [0, 0, 1], .016, .014, 0x263f52);
  cylinder(modules, [ex, ey, (-.046 - d.exit_drop) / 2], [0, 0, 1],
    .0025, d.exit_drop - .046, 0xbca269, .009);
  cylinder(modules, [ex, ey, .143], [0, 0, 1], .016, .030, 0x2d4356);
  cylinder(modules, [ex, ey, .159], [0, 0, 1], .019, .003, 0x6d8798);
  cylinder(modules, [ex, ey, .161], [0, 0, 1], .014, .002, 0x1d2834);
  for (const y of [-.047, .005, .057]) {
    cylinder(modules, [-.009, y, .22], [1, 0, 0], .010, .017, 0xb3c4d0);
    cylinder(modules, [-.019, y, .22], [1, 0, 0], .007, .004, 0x162b3e);
  }
  box(modules, [.018, .031, .070], [-.010, -.104, .209], 0x334c62);
  cylinder(modules, [-.004, d.entrance_y, d.entrance_z], [1, 0, 0], .018, .008, 0x9fb4c6);
  cylinder(modules, [-.009, d.entrance_y, d.entrance_z], [1, 0, 0], .002, .003, 0x182e45);
  text(annotations, '光学舱 · 假设布局', [.13, -.105, .012], .16);
  text(annotations, '控制电子舱', [.133, -.070, .25], .13);
  text(annotations, '位置检测模块', [.425, ey, .155], .1);
  text(annotations, '物镜 / 保护玻璃 / 喷嘴', [ex, ey, -.087], .15);
  dimension(dimensions, [0, -W / 2 - .035, -.017], [D, -W / 2 - .035, -.017],
    '263.5 mm', [D / 2, -W / 2 - .035, -.033]);
  dimension(dimensions, [-.045, -W / 2, -.017], [-.045, W / 2, -.017],
    '303.5 mm', [-.055, 0, -.017]);
  dimension(dimensions, [-.035, W / 2 + .025, 0], [-.035, W / 2 + .025, H],
    '271 mm', [-.035, W / 2 + .025, H / 2]);
  const bounds = new THREE.Box3(new THREE.Vector3(0, -W / 2, 0), new THREE.Vector3(D, W / 2, H));
  const envelope = new THREE.Box3Helper(bounds, 0x44708e); dimensions.add(envelope);
  const beam = new THREE.Group(), opticalParts = new THREE.Group(); root.add(beam, opticalParts);
  const demo = config.optical_demo;
  cylinder(opticalParts, demo.fold_center, demo.fold_normal, demo.fold_radius, .0007, 0xa6c9da);
  const lens = cylinder(opticalParts, demo.lens_center, [0, 0, 1], demo.lens_radius, .001, 0x4bbff2);
  lens.material.transparent = true; lens.material.opacity = .35; lens.material.depthWrite = false;
  const beamLabels = new THREE.Group(); root.add(beamLabels);
  text(beamLabels, '固定折转镜（假设）', [ex + .025, ey, demo.fold_center[2] + .028], .10);
  text(beamLabels, '等效物镜 f = 25 mm', [ex + .034, ey, -.039], .085);
  text(beamLabels, '焦平面（非工件实测）', [ex + .052, ey, -.079], .10);
  return { root, chassis, covers, electronics, modules, motors, annotations, motorLabels, endPanel, dimensions, cabling, states, config, beam, opticalParts, beamLabels };
}

export function updateAssembly(assembly, { mode, payload, selected, previewAngle, showDimensions, showLabels, showBeam }) {
  const a = assembly;
  const beamView = mode === 'beam' || mode === 'focus';
  a.root.visible = mode !== 'optical';
  a.chassis.visible = mode !== 'motors'; a.modules.visible = mode !== 'motors';
  a.covers.visible = mode === 'exterior';
  a.endPanel.visible = mode === 'exterior';
  a.electronics.visible = mode !== 'motors' && !beamView; a.cabling.visible = mode !== 'motors' && !beamView;
  a.dimensions.visible = showDimensions && mode !== 'motors';
  a.annotations.visible = showLabels && mode === 'cutaway';
  a.motorLabels.visible = showLabels && mode !== 'exterior';
  a.beam.visible = showBeam; a.opticalParts.visible = showBeam; a.beamLabels.visible = showBeam && showLabels && mode !== 'exterior';
  a.beamLabels.children.forEach((label, i) => {
    label.scale.copy(label.userData.baseScale).multiplyScalar(mode === 'focus' ? .22 : 1);
    label.position.copy(label.userData.basePosition);
    if (mode === 'focus') { label.visible = i > 0; label.position.x = a.config.dimensions.exit_axis_x + .016; }
    else label.visible = true;
  });
  a.motorLabels.visible = a.motorLabels.visible && mode !== 'focus';
  // The beam is depth-tested now, but sheet metal drawn at 90 % transparency still writes no
  // depth and would halo through the actuators, so the beam views drop it instead.
  a.chassis.visible = a.chassis.visible && !showBeam;
  a.modules.visible = a.modules.visible && !showBeam;
  a.covers.visible = a.covers.visible && !showBeam;
  a.endPanel.visible = a.endPanel.visible && !showBeam;
  for (const group of [a.chassis, a.modules, a.covers, a.endPanel]) group.traverse(object => {
    if (!object.isMesh) return;
    object.material.transparent = false; object.material.opacity = 1; object.material.depthWrite = true;
  });
  a.states.forEach((state, i) => {
    const angle = i === 4 ? previewAngle : payload?.mirror_angles?.[i] ?? 0;
    state.rotor.quaternion.setFromAxisAngle(state.axis, angle);
    state.body.material.emissive.setHex(Number(selected) === i ? state.color : 0);
    state.body.material.emissiveIntensity = .32;
  });
}

export function drawAssemblyBeam(assembly, trace, step, beamScale = 1) {
  const group = assembly.beam;
  group.traverse(object => { object.geometry?.dispose(); object.material?.dispose(); }); group.clear();
  if (!trace) return;
  const show = index => step === 0 || index < step;
  const chief = trace.chief.segments;
  for (const ray of trace.marginal) ray.segments.forEach((segment, i) => {
    if (!show(i)) return;
    const base = chief[i]; if (!base) return;
    const displayed = ['start', 'end'].map(key => v(base[key]).lerp(v(segment[key]), beamScale));
    const geometry = new THREE.BufferGeometry().setFromPoints(displayed);
    const color = !segment.valid ? 0xff6677 : i === 7 ? 0x63efae : i === 6 ? 0x71bbff : 0xffd16c;
    const margin = new THREE.Line(geometry, new THREE.LineBasicMaterial({ color,
      transparent: true, opacity: .5 }));
    margin.renderOrder = 10; group.add(margin);
  });
  chief.forEach((segment, i) => {
    if (!show(i)) return;
    const start = v(segment.start), end = v(segment.end), delta = end.clone().sub(start);
    const color = !segment.valid ? 0xff6677 : i === 7 ? 0x63efae : i === 6 ? 0x71bbff : 0xffd16c;
    const material = new THREE.LineBasicMaterial({ color, transparent: true });
    const ray = new THREE.Line(new THREE.BufferGeometry().setFromPoints([start, end]), material);
    ray.renderOrder = 20; group.add(ray);
    const length = Math.min(.007, delta.length() * .25);
    const arrow = new THREE.ArrowHelper(delta.clone().normalize(), start.clone().addScaledVector(delta, .52), length, color, length * .55, length * .35);
    arrow.traverse(o => { if (o.material) o.renderOrder = 21; });
    group.add(arrow);
  });
  const point = trace.chief.focus;
  if (point && (step === 0 || step === 8)) group.add(new THREE.Points(
    new THREE.BufferGeometry().setFromPoints([v(point)]),
    new THREE.PointsMaterial({ color: 0x63efae, size: 6, sizeAttenuation: false })));
}
