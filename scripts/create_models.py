"""Original premium educational assemblies; illustrative geometry, never OEM CAD.

Blender Z-up exports to glTF Y-up; the drivetrain remains on X. Every motion
ratio is an explicitly illustrative kinematic ratio, not an installed-machine
measurement. Unknown gearbox variants intentionally contain no Gearbox node.
Meshes are batched by component/material/parent to keep draw calls bounded.
"""
import bpy
import math
import json
import os
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public/models'
BLEND = ROOT / 'assets/blender'
OUT.mkdir(parents=True, exist_ok=True)
BLEND.mkdir(parents=True, exist_ok=True)
TAU = math.tau
BATCHES = {}


def material(name, color, metal=0, rough=.35):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bs = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bs is None:
        bs = m.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        output = next((n for n in m.node_tree.nodes if n.type == 'OUTPUT_MATERIAL'), None) or m.node_tree.nodes.new('ShaderNodeOutputMaterial')
        m.node_tree.links.new(bs.outputs['BSDF'], output.inputs['Surface'])
    bs.inputs['Base Color'].default_value = (*color, 1)
    bs.inputs['Metallic'].default_value = metal
    bs.inputs['Roughness'].default_value = rough
    return m


def group(name, component=None, parent=None, loc=(0, 0, 0), ratio=None, axis='x'):
    o = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(o)
    o.location = loc
    if parent:
        o.parent = parent
    if component:
        o['component'] = component
    if ratio is not None:
        o['motionAxis'] = axis
        o['motionRatio'] = ratio
        o['motionBaseRPM'] = 12
        o['motionIllustrative'] = True
    return o


def add(name, vertices, faces, mat, component, parent, separate=False, smooth=True):
    key = (name if separate else component, parent.name, mat.name, smooth)
    if key not in BATCHES:
        BATCHES[key] = [name if separate else component + '_' + mat.name.replace(' ', '_'), [], [], mat, component, parent, smooth]
    entry = BATCHES[key]
    offset = len(entry[1])
    entry[1].extend(vertices)
    entry[2].extend(tuple(i + offset for i in face) for face in faces)


def flush():
    for name, verts, faces, mat, component, parent, smooth in BATCHES.values():
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        o = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(o)
        o.parent = parent
        o.data.materials.append(mat)
        o['component'] = component
        for polygon in mesh.polygons:
            polygon.use_smooth = smooth
    BATCHES.clear()


def box(name, loc, size, mat, comp, parent, separate=False):
    x, y, z = loc
    a, b, c = (v / 2 for v in size)
    vs = [(x+u*a, y+v*b, z+w*c) for u, v, w in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
    fs = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    add(name, vs, fs, mat, comp, parent, separate, False)


def axial(x, a, b, axis):
    return (x,a,b) if axis == 'X' else ((a,x,b) if axis == 'Y' else (a,b,x))


def cylinder(name, loc, radius, length, mat, comp, parent, axis='X', segments=None, inner=0, separate=False):
    n = segments or SEG
    vs, fs = [], []
    for side in [-1, 1]:
        for r in ([radius, inner] if inner else [radius]):
            for i in range(n):
                p = axial(side*length/2, r*math.cos(TAU*i/n), r*math.sin(TAU*i/n), axis)
                vs.append(tuple(p[j]+loc[j] for j in range(3)))
    if inner:
        for i in range(n):
            j = (i+1)%n
            fs.extend([(i,j,2*n+j,2*n+i),(n+i,3*n+i,3*n+j,n+j),(i,n+i,n+j,j),(2*n+i,2*n+j,3*n+j,3*n+i)])
    else:
        for i in range(n):
            j = (i+1)%n
            fs.append((i,j,n+j,n+i))
        fs.extend([tuple(reversed(range(n))), tuple(n+i for i in range(n))])
    add(name, vs, fs, mat, comp, parent, separate)


def torus(name, loc, radius, tube, mat, comp, parent, axis='X', segments=None, separate=False):
    n = segments or SEG
    k = 6 if LOW else 8
    vs, fs = [], []
    for i in range(n):
        a = TAU*i/n
        for j in range(k):
            b = TAU*j/k
            p = axial(tube*math.sin(b), (radius+tube*math.cos(b))*math.cos(a), (radius+tube*math.cos(b))*math.sin(a), axis)
            vs.append(tuple(p[q]+loc[q] for q in range(3)))
    for i in range(n):
        for j in range(k):
            fs.append((i*k+j, ((i+1)%n)*k+j, ((i+1)%n)*k+(j+1)%k, i*k+(j+1)%k))
    add(name, vs, fs, mat, comp, parent, separate)


def beam(name, start, end, radius, mat, comp, parent, segments=8):
    a, b = Vector(start), Vector(end)
    direction = (b-a).normalized()
    basis = direction.cross(Vector((0,0,1)))
    if basis.length < .01:
        basis = direction.cross(Vector((0,1,0)))
    basis.normalize()
    other = direction.cross(basis).normalized()
    vs, fs = [], []
    for c in [a,b]:
        for i in range(segments):
            p = c + radius*(math.cos(TAU*i/segments)*basis + math.sin(TAU*i/segments)*other)
            vs.append(tuple(p))
    for i in range(segments):
        j = (i+1)%segments
        fs.append((i,j,segments+j,segments+i))
    fs += [tuple(reversed(range(segments))), tuple(segments+i for i in range(segments))]
    add(name, vs, fs, mat, comp, parent)


def pipe(name, points, radius, mat, comp, parent):
    for a,b in zip(points, points[1:]):
        beam(name, a,b,radius,mat,comp,parent,6 if LOW else 8)
    if not LOW:
        for p in points[1:-1]:
            cylinder(name,p,radius*1.4,.08,mat,comp,parent,axis='Z',segments=8)


def bolt_ring(name, center, radius, count, mat, comp, parent, axis='X', size=.055):
    for i in range(count):
        a = TAU*i/count
        p = axial(0,radius*math.cos(a),radius*math.sin(a),axis)
        p = tuple(p[q]+center[q] for q in range(3))
        cylinder(name,p,size,.055,mat,comp,parent,axis=axis,segments=6)
        if not LOW:
            cylinder(name+' washer',p,size*1.32,.02,SILVER,comp,parent,axis=axis,segments=8)


def gear_mesh(name, radius, teeth, width, mat, parent, internal=False, bore=.15, helix=0, tooth_depth=.043):
    # Four vertices per tooth and multiple axial slices for helical flanks.
    # Teeth and ratios are illustrative; only documented stage counts constrain
    # the V110 family layout.
    n = teeth*4
    layers = (3 if LOW else 5) if helix else 2
    vs, fs = [], []
    for layer in range(layers):
        u=layer/(layers-1)
        for ring in [0,1]:
            for i in range(n):
                phase = TAU*i/n + (u-.5)*helix
                if internal:
                    r = radius+.12 if ring == 0 else radius-(.045 if i%4 in (1,2) else -.025)
                else:
                    r = radius+(tooth_depth if i%4 in (1,2) else -tooth_depth*(.025/.043)) if ring == 0 else bore
                vs.append(((u-.5)*width,r*math.cos(phase),r*math.sin(phase)))
    for layer in range(layers-1):
        a=layer*2*n;b=(layer+1)*2*n
        for i in range(n):
            j=(i+1)%n
            fs.extend([(a+i,a+j,b+j,b+i),(a+n+i,b+n+i,b+n+j,a+n+j)])
    back=(layers-1)*2*n
    for i in range(n):
        j=(i+1)%n
        fs.extend([(i,n+i,n+j,j),(back+i,back+j,back+n+j,back+n+i)])
    add(name,vs,fs,mat,'gearbox',parent, smooth=False)


def rounded_shell(name, xs, widths, heights, parent):
    # Loft with a rounded cross section. Roof, back wall and underside remain
    # separate so the educational interior can reveal the entire assembly.
    n=20 if LOW else 40
    sections=[]
    for x,w,h in zip(xs,widths,heights):
        ring=[]
        for i in range(n):
            a=TAU*i/n
            ca,sa=math.cos(a),math.sin(a)
            # Rounded rectangle / soft superellipse.
            ring.append((x, w/2*math.copysign(abs(ca)**.54,ca), h/2*math.copysign(abs(sa)**.54,sa)))
        sections.append(ring)
    vs=[v for ring in sections for v in ring]
    bands={'roof':[], 'window':[], 'rear':[], 'floor':[]}
    for k in range(len(sections)-1):
        for i in range(n):
            a=TAU*(i+.5)/n
            category='roof' if math.sin(a)>.45 else ('floor' if math.sin(a)<-.65 else ('rear' if math.cos(a)>0 else 'window'))
            bands[category].append((k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i))
    for label,faces in bands.items():
        add('Shell_'+name+'_'+label,vs,faces,PEARL,'nacelle',parent,separate=True)
    add('Shell_'+name+'_tail',vs,[tuple((len(sections)-1)*n+i for i in range(n))],PEARL,'nacelle',parent,separate=True)


def blade(name, parent, length, width):
    # Smooth NACA-like asymmetric airfoil, twist and swept tapered tip.
    section_count=13 if LOW else 24
    ring_count=16 if LOW else 28
    vs,fs=[],[]
    for k in range(section_count):
        fraction=k/(section_count-1)
        z=1.12+(length-1.12)*fraction
        shape=math.sin(math.pi*min(1,fraction*1.8)) if fraction<.52 else (1-fraction)**.65
        chord=width*(.3+.7*shape)*(1-.93*fraction**3)
        twist=math.radians(23*(1-fraction)**1.8-2)
        sweep=-.025*z+.16*fraction**4
        for j in range(ring_count):
            a=TAU*j/ring_count
            yy=chord*.5*math.cos(a)+sweep
            xx=chord*(.135 if math.sin(a)>=0 else .075)*math.sin(a)
            camber=.032*chord*math.sin(a)**2
            xx+=camber
            vs.append((xx*math.cos(twist)-yy*math.sin(twist), yy*math.cos(twist)+xx*math.sin(twist),z))
    for i in range(section_count-1):
        for j in range(ring_count):
            fs.append((i*ring_count+j,i*ring_count+(j+1)%ring_count,(i+1)*ring_count+(j+1)%ring_count,(i+1)*ring_count+j))
    fs += [tuple(reversed(range(ring_count))),tuple((section_count-1)*ring_count+j for j in range(ring_count))]
    add(name,vs,fs,PEARL,'blades',parent,separate=True)
    # Root flange and visible bonding line.
    cylinder('Blade composite root',(0,0,1.1),.37,.44,PEARL,'blades',parent,axis='Z',inner=.29)
    torus('Root seal',(0,0,1.29),.375,.016,GRAPHITE,'blades',parent,axis='Z')


def support_frame(root, length, direct=False):
    frame=group('Bedplate','nacelle',root)
    front = -.45 if direct else -3.9
    span = 4.65 if direct else length
    cross_positions = [.0,1.2,2.6,4.1] if direct else [-3.0,-1.2,.6,2.4,4.2]
    rail_positions = [.1,2.4,4.2] if direct else [-2.3,.1,2.4,4.2]
    for y in [-1.15,1.15]:
        box('Longitudinal chassis',(front+span/2,y,-1.26),(span,.18,.32),GRAPHITE,'nacelle',frame)
        for x in cross_positions:
            box('Cross beam',(x,0,-1.35),(.14,2.6,.2),SILVER,'nacelle',frame)
    for x in ([.0,1.2,2.6,4.1] if direct else [-2.8,-.8,1.2,3.2]):
        for y in [-1.18,1.18]:
            cylinder('Frame fastener',(x,y,-1.08),.065,.06,SILVER,'nacelle',frame,axis='Z',segments=6)
    # Walkway with slotted grating, safety rail and maintenance ribs.
    for side in [-1,1]:
        y=side*1.15
        box('Walkway edge',(front+span/2,y,-1.0),(span,.5,.08),SILVER,'nacelle',frame)
        slots=18 if LOW else 38
        for j in range(slots):
            box('Walkway slot',(front+span*j/slots,y,-.95),(.03,.37,.022),GRAPHITE,'nacelle',frame)
        for x in rail_positions:
            beam('Safety stanchion',(x,y,-.95),(x,y,-.52),.025,GOLD,'nacelle',frame)
        beam('Safety handrail',(rail_positions[0],y,-.52),(4.2,y,-.52),.029,GOLD,'nacelle',frame)
    if direct:
        box('Forward bearing support',(-2.98,0,-.92),(1.65,.42,.25),GRAPHITE,'nacelle',frame)
    return frame


def build_tower(root, profile):
    tower=group('Tower','tower',root)
    n=SEG
    vs,fs=[],[]
    for z,r in [(-26.5,1.03),(-18,.91),(-10,.76),(-1.7,.65)]:
        for i in range(n):
            a=TAU*i/n;vs.append((r*math.cos(a),r*math.sin(a),z))
    for k in range(3):
        for i in range(n):
            fs.append((k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i))
    add('Tower seamless steel',vs,fs,PEARL,'tower',tower)
    for z,r in [(-1.7,.65),(-10,.76),(-18,.91),(-26.5,1.03)]:
        torus('Tower welded seam',(0,0,z),r,.017,SILVER,'tower',tower,axis='Z')
    cylinder('Tower base plinth',(0,0,-26.6),1.22,.23,SILVER,'tower',tower,axis='Z')
    bolt_ring('Tower foundation studs',(0,0,-26.43),1.12,12 if LOW else 24,GRAPHITE,'tower',tower,axis='Z')
    # Small service door makes the exterior scale readable.
    box('Service door',(0,-1.025,-24.9),(.5,.045,1.4),SAGE,'tower',tower)
    box('Door handle',(.17,-1.07,-24.7),(.025,.035,.14),SILVER,'tower',tower)
    yaw=group('Yaw','yaw',root)
    cylinder('Yaw slew bearing',(0,0,-1.62),.93,.24,SILVER,'yaw',yaw,axis='Z',inner=.64)
    torus('Yaw seal',(0,0,-1.75),.86,.035,GRAPHITE,'yaw',yaw,axis='Z')
    bolt_ring('Yaw bearing bolts',(0,0,-1.47),.82,16 if LOW else 32,GRAPHITE,'yaw',yaw,axis='Z')
    # Stationary yaw drives are correct under fixed aligned normal wind.
    for i in range(4):
        a=TAU*i/4+.4
        x,y=.92*math.cos(a),.92*math.sin(a)
        cylinder('Yaw drive housing',(x,y,-1.15),.15,.55,SAGE,'yaw',yaw,axis='Z')
        cylinder('Yaw brake actuator',(x,y,-.81),.12,.15,SILVER,'yaw',yaw,axis='Z')
        for j in range(5 if LOW else 9):
            torus('Yaw motor cooling fin',(x,y,-1.35+j*.043),.158,.012,SILVER,'yaw',yaw,axis='Z',segments=12)


def build_rotor(root, profile):
    rotor=group('RotorAssembly','rotor',root,(-4.15,0,0))
    # Hollow mechanical hub, root flange, pitch drivetrain and nose shell.
    cylinder('Hub structural drum',(0,0,0),.72,1.26,SILVER,'hub',rotor,inner=.52)
    for x in [-.6,.6]:
        torus('Hub ring rib',(x,0,0),.72,.055,GRAPHITE,'hub',rotor)
        bolt_ring('Hub flange bolts',(x,0,0),.65,12 if LOW else 24,GRAPHITE,'hub',rotor)
    # Ellipsoid generated as lathed rings, open back lets inspection see hub.
    n=SEG;vs,fs=[],[]
    for k in range(10 if not LOW else 6):
        u=k/((10 if not LOW else 6)-1)
        x=-1.34+.93*u
        r=.80*math.sin(math.pi/2*u)
        for j in range(n):
            a=TAU*j/n;vs.append((x,r*math.cos(a),r*math.sin(a)))
    for k in range(len(vs)//n-1):
        for j in range(n):fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    add('HubCover',vs,fs,PEARL,'hub',rotor,separate=True)
    for i in range(3):
        arm=group(f'BladeArm_{i}',parent=rotor)
        arm.rotation_euler[0]=i*TAU/3
        pitch=group(f'Pitch_{i}','pitch',arm)
        cylinder('Pitch slew race',(0,0,.9),.45,.22,SILVER,'pitch',pitch,axis='Z',inner=.32)
        torus('Pitch seal',(0,0,1.02),.43,.023,GRAPHITE,'pitch',pitch,axis='Z')
        bolt_ring('Pitch root bolts',(0,0,1.06),.39,12 if LOW else 24,GRAPHITE,'pitch',pitch,axis='Z',size=.032)
        cylinder('Pitch electric actuator',(.32,-.27,.45),.13,.35,SAGE,'pitch',arm,axis='Z')
        cylinder('Pitch pinion gearbox',(.32,-.27,.72),.15,.11,SILVER,'pitch',arm,axis='Z')
        beam('Pitch linkage',(.3,-.2,.68),(.12,-.3,.94),.032,GOLD,'pitch',arm)
        box('Pitch control module',(.05,.1,.35),(.32,.18,.28),SAGE,'pitch',arm)
        pipe('Pitch power cable',[(.0,.1,.2),(.1,-.18,.3),(.3,-.22,.5)],.017,COPPER,'pitch',arm)
        blade(f'Blade_{i}',pitch,profile['blade_length'],profile['blade_width'])
    return rotor


def main_bearings(root, direct):
    shaft=group('MainShaft','shaft',root)
    spin=group('MainShaftSpin','shaft',shaft,(-2.65,0,0),ratio=-1)
    cylinder('Low speed machined shaft',(0,0,0),.27,2.95,SILVER,'shaft',spin)
    # Contrasting small witness stripe visibly demonstrates shaft rotation.
    box('Shaft witness stripe',(.0,-.27,0),(2.35,.012,.045),GOLD,'shaft',spin)
    for x in [-3.1,-2.3]:
        cylinder('Main bearing race',(x,0,0),.54,.37,SILVER,'shaft',shaft,inner=.31)
        torus('Main bearing seal',(x-.2,0,0),.46,.027,GRAPHITE,'shaft',shaft)
        bolt_ring('Main bearing flange bolts',(x-.22,0,0),.46,12 if LOW else 20,GRAPHITE,'shaft',shaft)
        for y in [-.38,.38]:
            box('Pillow block',(x,y,-.66),(.48,.21,.8),PEARL,'shaft',shaft)
            cylinder('Bearing anchor bolt',(x,y,-.24),.057,.08,SILVER,'shaft',shaft,axis='Z',segments=6)
        pipe('Bearing oil feed',[(x,-.56,-.48),(x,-.56,.35),(x,-.2,.49)],.023,GOLD,'shaft',shaft)
    return shaft


def planetary_stage(parent, name, x, scale, carrier_ratio):
    stage=group(name,'gearbox',parent,(x,0,0))
    ring=group(name+'_FixedRing','gearbox',stage)
    # 16-tooth sun, 24-tooth planets, 64-tooth fixed ring; 5:1 stage.
    gear_mesh('Internal ring',1.28*scale,64,.22,SILVER,ring,internal=True)
    carrier=group(name+'_Carrier','gearbox',stage,ratio=carrier_ratio)
    sun=group(name+'_Sun','gearbox',stage,ratio=carrier_ratio*5)
    gear_mesh('Sun gear',.32*scale,16,.23,GOLD,sun,bore=.115*scale)
    for i in range(3):
        a=TAU*i/3
        y,z=.8*scale*math.cos(a),.8*scale*math.sin(a)
        planet=group(name+f'_Planet_{i}','gearbox',carrier,(0,y,z),ratio=-carrier_ratio*8/3)
        planet.rotation_euler[0]=math.pi/24
        gear_mesh('Planet gear',.48*scale,24,.24,SILVER,planet,bore=.15*scale)
        cylinder('Planet axle',(0,0,0),.12*scale,.37,GRAPHITE,'gearbox',planet)
        bolt_ring('Planet face bolts',(-.15,0,0),.23*scale,6,GOLD,'gearbox',planet,size=.029)
        beam('Carrier spoke',(-.2,0,0),(-.2,y,z),.045*scale,SAGE,'gearbox',carrier)
    torus('Carrier front rim',(-.19,0,0),.80*scale,.035*scale,SAGE,'gearbox',carrier)
    return stage


def build_gearbox(root, shaft, profile):
    gear=group('Gearbox','gearbox',root)
    planetary_stage(gear,'PlanetaryStage1',-1.1,.88,-1)
    v110 = profile['id'] == 'vestas-v110-20'
    if v110:
        # Vestas 2 MW family source: one planetary + two helical stages.
        # The 5 x 3 x 6 = 90 ratio and shaft spacing remain modeling assumptions.
        gear['stageLayout'] = 'one planetary + two helical stages'
        gear['stageLayoutScope'] = 'family'
        sun_shaft=group('PlanetaryOutputShaftSpin','shaft',shaft,(-.76,0,0),ratio=-5)
        cylinder('Planetary output shaft',(0,0,0),.12,.72,SILVER,'shaft',sun_shaft)
        d1=math.hypot(.50,.30)
        r1=d1*.75;r2=d1*.25
        drive1=group('HelicalStage1_Input','gearbox',gear,(-.42,0,0),ratio=-5)
        gear_mesh('Helical stage 1 input',r1,54,.25,SILVER,drive1,bore=.10,helix=.20,tooth_depth=.018)
        output1=group('HelicalStage1_Output','gearbox',gear,(-.42,.50,.30),ratio=15)
        gear_mesh('Helical stage 1 output',r2,18,.25,GOLD,output1,bore=.06,helix=-.60,tooth_depth=.018)
        middle=group('IntermediateShaftSpin','shaft',shaft,(-.08,.50,.30),ratio=15)
        cylinder('Intermediate shaft',(0,0,0),.071,.86,SILVER,'shaft',middle)
        for xx in [-.28,.23]:
            cylinder('Intermediate bearing',(xx,.50,.30),.12,.12,SAGE,'shaft',shaft,inner=.073)
        d2=math.hypot(.50,.39)
        r3=d2*6/7;r4=d2/7
        drive2=group('HelicalStage2_Input','gearbox',gear,(.31,.50,.30),ratio=15)
        gear_mesh('Helical stage 2 input',r3,108,.22,SILVER,drive2,bore=.075,helix=.16,tooth_depth=.009)
        output2=group('HelicalStage2_Output','gearbox',gear,(.31,0,.69),ratio=-90)
        gear_mesh('Helical stage 2 output',r4,18,.22,GOLD,output2,bore=.043,helix=-.96,tooth_depth=.009)
        output_ratio=-90
        casing_positions=[(-1.1,1.17),(.02,1.03)]
    else:
        planetary_stage(gear,'PlanetaryStage2',-.45,.62,-5)
        # Three-stage 90:1 chain is explicitly a visualization assumption.
        # Offset final gears have pitch radii in the ratio 90/25 = 3.6.
        drive=group('ParallelStageInput','gearbox',gear,(.1,0,0),ratio=-25)
        gear_mesh('Parallel stage input',.54,36,.23,SILVER,drive,bore=.13)
        output=group('ParallelStageOutput','gearbox',gear,(.1,0,.69),ratio=90)
        gear_mesh('Parallel stage output',.15,10,.26,GOLD,output,bore=.07)
        output_ratio=90
        casing_positions=[(-1.1,1.17),(-.45,.84)]
    cylinder('Output coupling',(.6,0,.69),.16,.68,SILVER,'shaft',shaft)
    coupling=group('HighSpeedCoupling','shaft',shaft,(.78,0,.69),ratio=output_ratio)
    torus('Flexible coupling',(0,0,0),.20,.055,GRAPHITE,'shaft',coupling)
    bolt_ring('Coupling fasteners',(-.045,0,0),.20,8,GOLD,'shaft',coupling,size=.033)
    for x,r in casing_positions:
        # Rear half shell plus ring caps, rather than an opaque solid.
        casing=group('GearboxCasing_'+str(x),'gearbox',gear)
        n=SEG//2;vs=[];fs=[]
        for side in [-1,1]:
            for i in range(n+1):
                a=-math.pi/2+math.pi*i/n
                vs.append((x+side*.23,r*math.cos(a),r*math.sin(a)))
        for i in range(n):fs.append((i,i+1,n+2+i,n+1+i))
        add('GearboxCasing_shell'+str(x),vs,fs,SAGE,'gearbox',casing,separate=True)
        bolt_ring('Casing flange studs',(x-.25,0,0),r*.97,12 if LOW else 24,SILVER,'gearbox',gear)
        for y in [-.8,.8]:
            box('Gearbox feet',(x,y,-1.02),(.43,.26,.38),PEARL,'gearbox',gear)
    pipe('Gearbox lubrication manifold',[(-1.2,-1.03,-.75),(-.65,-1.05,-.75),(-.65,-1.05,.55),(.0,-.7,.55)],.029,GOLD,'gearbox',gear)
    cylinder('Oil filter',(-.35,-.95,-.52),.12,.54,SAGE,'gearbox',gear,axis='Z')
    return gear


def build_generator(root, direct, geared, profile):
    gen=group('Generator','generator',root)
    if direct:
        # Large annular PMSG: segmented stator, exposed coils, moving magnet ring.
        x=-1.65;r=1.8
        torus('Generator stator frame',(x,0,0),r,.11,SAGE,'generator',gen)
        cylinder('Annular back plate',(x+.38,0,0),r+.09,.10,SILVER,'generator',gen,inner=1.37)
        torus('Generator rim ribs',(x-.34,0,0),r+.11,.07,SILVER,'generator',gen)
        bolt_ring('Stator ring bolts',(x-.41,0,0),r+.08,24 if LOW else 48,GRAPHITE,'generator',gen)
        rotor=group('GeneratorRotor','generator',gen,(x,0,0),ratio=-1)
        cylinder('Magnet carrier',(0,0,0),1.42,.22,GRAPHITE,'generator',rotor,inner=.46)
        torus('Magnet carrier rim',(-.19,0,0),1.4,.08,SILVER,'generator',rotor)
        count=18 if LOW else 36
        for i in range(count):
            a=TAU*i/count
            y,z=1.56*math.cos(a),1.56*math.sin(a)
            # Coil modules expressed as copper loops around segmented cores.
            coil=group('StatorModule_'+str(i),'generator',gen,(x,y,z))
            coil.rotation_euler[0]=a
            box('Stator lamination',(0,0,0),(.55,.22,.25),SILVER,'generator',coil)
            torus('Copper coil front',(-.3,0,0),.145,.04,COPPER,'generator',coil,segments=12)
            torus('Copper coil rear',(.3,0,0),.145,.035,COPPER,'generator',coil,segments=12)
            for offset in [-.06,.06]:
                beam('Winding bridge',(-.30,offset,.12),(.3,offset,.12),.024,COPPER,'generator',coil,segments=6)
            magnet=group('Magnet_'+str(i),'generator',rotor,(0,1.30*math.cos(a),1.30*math.sin(a)))
            magnet.rotation_euler[0]=a
            box('Permanent magnet',(0,0,0),(.24,.17,.21),SAGE,'generator',magnet)
        for i in range(6):
            a=TAU*i/6
            beam('Rotor spider',(0,.4*math.cos(a),.4*math.sin(a)),(0,1.25*math.cos(a),1.25*math.sin(a)),.052,SILVER,'generator',rotor)
        for y in [-1.0,1.0]:box('Generator pedestal',(x,y,-1.28),(.65,.36,.45),PEARL,'generator',gen)
        # Distinct ring housing, kept translucent during inspection.
        cylinder('GeneratorCasing_annular',(x,0,0),r+.14,.76,SAGE,'generator',gen,inner=r-.1,separate=True)
    else:
        x=2.05;z=.69 if geared else 0;r=.65 if geared else .78
        rotor=group('GeneratorRotor','generator',gen,(x,0,z),ratio=(-90 if profile['id'] == 'vestas-v110-20' else 90) if geared else -1)
        cylinder('Electrical rotor core',(0,0,0),r*.54,1.55,GRAPHITE,'generator',rotor)
        bars=12 if LOW else 24
        for i in range(bars):
            a=TAU*i/bars;y,z0=r*.56*math.cos(a),r*.56*math.sin(a)
            beam('Rotor conductor',(-.72,y,z0),(.72,y,z0),.021,COPPER,'generator',rotor,6)
        for xx in [-.75,.75]:
            torus('Rotor end ring',(xx,0,0),r*.55,.042,COPPER,'generator',rotor)
            bolt_ring('Rotor plate bolts',(xx,0,0),r*.37,8,SILVER,'generator',rotor,size=.027)
        # Coils and lamination ribs reveal electromechanical conversion.
        for i in range(12 if LOW else 24):
            a=TAU*i/(12 if LOW else 24)
            y,z0=r*.84*math.cos(a),r*.84*math.sin(a)
            beam('Stator conductor',(x-.68,y,z+z0),(x+.68,y,z+z0),.048,COPPER,'generator',gen,6)
        for xx in [x-.82,x+.82]:
            torus('Stator winding end',(xx,0,z),r*.83,.07,COPPER,'generator',gen)
            cylinder('Generator flange',(xx,0,z),r+.12,.13,SAGE,'generator',gen,inner=r*.68)
            bolt_ring('Generator flange bolts',(xx-.08,0,z),r+.065,12 if LOW else 24,SILVER,'generator',gen,size=.035)
        # Cooling fins on rear half leave windings visible on the viewing side.
        n=8 if LOW else 16;vs=[];fs=[]
        for xx in [x-.7,x+.7]:
            for i in range(n+1):
                a=-math.pi/2+math.pi*i/n
                vs.append((xx,(r+.08)*math.cos(a),z+(r+.08)*math.sin(a)))
        for i in range(n):fs.append((i,i+1,n+2+i,n+1+i))
        add('GeneratorCasing_half',vs,fs,SAGE,'generator',gen,separate=True)
        for i in range(9 if LOW else 17):
            xx=x-.65+1.3*i/((9 if LOW else 17)-1)
            # Fin support ribs can be seen against the pearl shell.
            torus('Generator cooling fin',(xx,0,z),r+.1,.022,SAGE,'generator',gen,segments=SEG)
        for xx in [x-.5,x+.5]:
            for y in [-.43,.43]:
                box('Generator mounting bracket',(xx,y,-.15),(.22,.19,.75),PEARL,'generator',gen)
        box('Generator terminal box',(x,.20,z+r+.15),(.6,.55,.3),SAGE,'generator',gen)
        for j in range(3):
            pipe('Generator power lead',[(x+.25+j*.06,-.4,z-.45),(x+.35+j*.06,-.95,-.4),(3.4,-1.0,-.4+j*.08)],.03,COPPER,'generator',gen)
    return gen


def electrical_equipment(root, direct, profile):
    converter=group('Converter','converter',root)
    x=3.75 if not direct else 2.75
    for j in range(2):
        y=.65+j*.52
        box('Converter chassis',(x,y,.13),(.8,.43,1.82),PEARL,'converter',converter)
        box('Converter front panel',(x-.42,y,.15),(.045,.39,1.64),SAGE,'converter',converter)
        box('Converter display',(x-.451,y,.6),(.018,.24,.15),GRAPHITE,'converter',converter)
        for k in range(3):
            cylinder('Status indicator',(x-.47,y-.065+k*.065,.43),.015,.017,GOLD if k==0 else SAGE,'converter',converter)
        for z in [-.55,-.45,-.35,-.25,-.15]:
            box('Converter louvre',(x-.45,y,z),(.018,.28,.018),GRAPHITE,'converter',converter)
        cylinder('Converter isolator',(x-.463,y-.13,.2),.04,.018,GOLD,'converter',converter)
        box('Power busbar',(x,y,-.86),(.52,.24,.065),COPPER,'converter',converter)
    pipe('DC bus cables',[(x,.52,-.85),(x,-.35,-.85),(x+0.5,-.45,-.85)],.036,COPPER,'converter',converter)
    transformer=group('Transformer','transformer',root)
    tx=x+.1;ty=-.65
    box('Transformer laminated core',(tx,ty,-.52),(.67,.68,.74),GRAPHITE,'transformer',transformer)
    for k in range(3):
        xx=tx-.25+k*.25
        cylinder('Transformer winding',(xx,ty,-.50),.16,.58,COPPER,'transformer',transformer,axis='Z')
        for z in [-.7,-.58,-.46,-.34]:
            torus('Winding turn',(xx,ty,z),.168,.012,GOLD,'transformer',transformer,axis='Z',segments=12)
        cylinder('Insulator bushing',(xx,ty,-.01),.066,.32,PEARL,'transformer',transformer,axis='Z')
        for z in [-.13,-.06,.01,.08]:
            torus('Bushing rib',(xx,ty,z),.08,.014,PEARL,'transformer',transformer,axis='Z',segments=12)
        cylinder('Terminal bolt',(xx,ty,.16),.04,.08,SILVER,'transformer',transformer,axis='Z',segments=6)
    for i in range(8 if LOW else 16):
        box('Transformer radiator',(tx-.38+i*.048,ty+.39,-.5),(.021,.14,.64),SAGE,'transformer',transformer)
    box('Transformer skid',(tx,ty,-.92),(1.02,.98,.12),SILVER,'transformer',transformer)
    # Hydraulic/cooling auxiliaries are grouped with nacelle; educational layout.
    auxiliary=group('AuxiliaryEquipment','nacelle',root)
    box('Oil service skid',(.45,-.88,-.69),(1.12,.48,.40),GRAPHITE,'nacelle',auxiliary)
    for x0 in [.12,.45]:
        cylinder('Accumulator',(x0,-.9,-.23),.12,.51,SAGE,'nacelle',auxiliary,axis='Z')
        cylinder('Accumulator end cap',(x0,-.9,.06),.11,.055,SILVER,'nacelle',auxiliary,axis='Z')
        pipe('Hydraulic line',[(x0,-.91,-.44),(x0,-1.1,-.50),(-1.2,-1.1,-.52)],.023,GOLD,'nacelle',auxiliary)
    cylinder('Cooling pump',(.75,-.9,-.45),.13,.35,SILVER,'nacelle',auxiliary,axis='Z')
    box('Maintenance controller',(4.2,.3,.71),(.20,.53,.65),PEARL,'nacelle',auxiliary)
    for j in range(3):box('Control relay',(4.08,.12+j*.16,.7),(.035,.10,.36),GRAPHITE,'nacelle',auxiliary)
    pipe('Main cable tray',[(2.1,.9,-.8),(1.0,.9,-.8),(0,.9,-.8),(0,.3,-1.2),(0,.3,-3.2)],.045,COPPER,'nacelle',auxiliary)


def shell_and_sensors(root, direct, profile):
    nacelle=group('Nacelle','nacelle',root)
    if direct:
        rounded_shell('direct',[-3.35,-2.3,-1.3,.5,2.5,4.2,4.8],[2.9,4.25,4.45,3.2,2.95,2.45,1.9],[2.8,4.15,4.2,2.8,2.6,2.3,2.1],nacelle)
    else:
        w=profile['width'];h=profile['height']
        rounded_shell('geared' if profile['known'] else 'generic',[-3.5,-3.1,-1.6,1.0,3.5,4.8,5.0],[2.6,w,w,w,w*.96,w*.83,w*.73],[2.7,h,h,h,h*.97,h*.90,h*.80],nacelle)
    # Structural ribs stay visible when the exterior cover becomes translucent.
    for x in [-2.9,-1.7,.3,2.4,4.3]:
        beam('Nacelle roof rib',(x,1.25,-1),(x,1.25,1.32),.04,PEARL,'nacelle',nacelle)
        beam('Nacelle roof rib',(x,1.25,1.32),(x,-1.2,1.32),.04,PEARL,'nacelle',nacelle)
    for i in range(8 if LOW else 16):
        box('Rear heat exchanger',(4.85,-.90+i*.12,.15),(.13,.025,1.6),GRAPHITE,'nacelle',nacelle)
    # External roof instrumentation and flush access hatch.
    box('Roof service hatch',(3.1,0,1.58),(1.3,.8,.05),SAGE,'nacelle',nacelle)
    beam('Sensor mast',(3.25,0,1.65),(3.25,0,2.62),.029,SILVER,'nacelle',nacelle)
    beam('Instrument crossbar',(2.85,0,2.35),(3.85,0,2.35),.025,SILVER,'nacelle',nacelle)
    vane=group('WindVane','nacelle',nacelle,(2.9,0,2.4))
    beam('Vane arm',(-.3,0,0),(.32,0,0),.017,SILVER,'nacelle',vane)
    add('Vane tail',[(.30,0,-.1),(.55,0,-.16),(.55,0,.16),(.30,0,.1)],[(0,1,2,3)],SAGE,'nacelle',vane)
    anemo=group('Anemometer','nacelle',nacelle,(3.8,0,2.42),ratio=7,axis='y')
    cylinder('Anemometer axle',(0,0,.04),.027,.15,SILVER,'nacelle',anemo,axis='Z')
    for i in range(3):
        a=TAU*i/3
        beam('Cup arm',(0,0,.13),(.20*math.cos(a),.20*math.sin(a),.13),.015,SILVER,'nacelle',anemo)
        cylinder('Wind sensor cup',(.23*math.cos(a),.23*math.sin(a),.15),.065,.06,SAGE,'nacelle',anemo,axis='Z',segments=8)
    return nacelle


def animate_rotor(rotor):
    bpy.context.scene.render.fps=24
    bpy.context.scene.frame_start=1
    bpy.context.scene.frame_end=121
    rotor.rotation_mode='XYZ'
    rotor.rotation_euler[0]=0
    rotor.keyframe_insert(data_path='rotation_euler',index=0,frame=1)
    rotor.rotation_euler[0]=-TAU
    rotor.keyframe_insert(data_path='rotation_euler',index=0,frame=121)
    action=rotor.animation_data.action
    action.name='NormalOperation'
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for curve in bag.fcurves:
                    for key in curve.keyframe_points:key.interpolation='LINEAR'
    bpy.context.scene.frame_set(1)


def profile_for(model):
    identifier=model['id']
    value=model['specs']['gearbox']['value']
    p={'id':identifier,'known':value is not None,'width':3.3,'height':3.2,'blade_length':17,'blade_width':1.82}
    if identifier.startswith('nordex'):
        p.update(width=3.65,height=3.35,blade_length=18.8,blade_width=2.0)
    elif identifier=='vestas-v110-20':
        p.update(width=3.0,height=3.0,blade_length=16.0,blade_width=1.75)
    elif identifier=='vestas-v112-30':
        p.update(width=3.13,height=3.10,blade_length=16.4,blade_width=1.78)
    elif identifier=='vestas-v136-36':
        p.update(width=3.45,height=3.35,blade_length=18.0,blade_width=1.91)
    elif identifier.startswith('vestas-v150'):
        p.update(width=3.6,height=3.35,blade_length=19.0,blade_width=2.05)
    elif identifier.startswith('goldwind'):
        p.update(blade_length=15.4,blade_width=1.75)
    elif identifier.startswith('envision'):
        p.update(width=3.1,height=3.0,blade_length=16.4,blade_width=1.76)
    elif identifier.startswith('gamesa'):
        p.update(width=3.0,height=3.0,blade_length=16.5,blade_width=1.76)
    return p


for data in sorted((ROOT/'src/data/models').glob('*.json')):
    model=json.loads(data.read_text(encoding='utf-8'))
    if os.environ.get('TURBINE_MODEL') and os.environ['TURBINE_MODEL'] != model['id']:
        continue
    for LOW in [False,True]:
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        BATCHES.clear()
        for pool in [bpy.data.meshes,bpy.data.materials,bpy.data.actions]:
            for block in list(pool):
                if block.users == 0:pool.remove(block)
        SEG=16 if LOW else 32
        PEARL=material('Warm pearl ceramic',(.91,.91,.835),.16,.28)
        SILVER=material('Brushed steel',(.54,.60,.57),.82,.27)
        GRAPHITE=material('Graphite frame',(.095,.145,.135),.55,.32)
        SAGE=material('Ecological sage enamel',(.24,.43,.33),.40,.30)
        COPPER=material('Copper winding',(.72,.32,.13),.78,.24)
        GOLD=material('Warm brass fasteners',(.70,.49,.22),.72,.27)
        profile=profile_for(model)
        direct=model['specs']['gearbox']['value'] is False
        geared=model['specs']['gearbox']['value'] is True
        root=group('Turbine')
        root['geometryRevision']='premium-2026-10'
        root['illustrativeGeometry']=True
        root['kinematicRatiosIllustrative']=True
        root['modelId']=model['id']
        build_tower(root,profile)
        support_frame(root,8.1,direct)
        rotor=build_rotor(root,profile)
        shaft=main_bearings(root,direct)
        if geared:build_gearbox(root,shaft,profile)
        build_generator(root,direct,geared,profile)
        electrical_equipment(root,direct,profile)
        shell_and_sensors(root,direct,profile)
        flush()
        animate_rotor(rotor)
        # Centimeters/meters here are normalized display units, never OEM CAD.
        bpy.context.scene.unit_settings.system='METRIC'
        if not LOW:
            bpy.ops.wm.save_as_mainfile(filepath=str(BLEND/(model['id']+'.blend')))
        target=OUT/(model['id']+('-low' if LOW else '')+'.glb')
        bpy.ops.export_scene.gltf(filepath=str(target),export_format='GLB',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_animations=True,export_extras=True,export_animation_mode='ACTIVE_ACTIONS',export_frame_range=True,export_force_sampling=True)
        mesh_objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
        triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in mesh_objects)
        print('PREMIUM_EXPORTED',target.name,'bytes',target.stat().st_size,'meshes',len(mesh_objects),'triangles',triangles,flush=True)
