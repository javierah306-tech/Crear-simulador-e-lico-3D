"""Original educational meshes. No OEM CAD, no unverified gearbox on unknown variants.
Blender Z-up exports as glTF Y-up. Rotor and shaft axis: X.
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'public/models'
OUT.mkdir(parents=True,exist_ok=True)
BLEND = ROOT/'assets/blender'
BLEND.mkdir(parents=True,exist_ok=True)

def material(name,color,metal=0,rough=.35):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
    return m
def group(name,component=None,parent=None,loc=(0,0,0)):
    o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=loc
    if parent:o.parent=parent
    if component:o['component']=component
    return o
def finish(o,name,mat,component=None,parent=None):
    o.name=name;o.data.materials.append(mat)
    if component:o['component']=component
    if parent:o.parent=parent
    for p in o.data.polygons:p.use_smooth=True
    return o
def box(name,loc,scale,mat,component,parent=None,bevel=.16):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        mod=o.modifiers.new('Soft edges','BEVEL');mod.width=bevel;mod.segments=3
        bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
    return finish(o,name,mat,component,parent)
def cylinder(name,loc,radius,length,mat,component,parent=None,axis='X'):
    bpy.ops.mesh.primitive_cylinder_add(vertices=SEG,radius=radius,depth=length,location=loc)
    o=bpy.context.object
    if axis=='X':o.rotation_euler[1]=math.pi/2
    if axis=='Y':o.rotation_euler[0]=math.pi/2
    return finish(o,name,mat,component,parent)
def torus(name,loc,radius,tube,mat,component,parent=None,axis='X'):
    bpy.ops.mesh.primitive_torus_add(major_segments=SEG,minor_segments=8,major_radius=radius,minor_radius=tube,location=loc)
    o=bpy.context.object
    if axis=='X':o.rotation_euler[1]=math.pi/2
    return finish(o,name,mat,component,parent)
def blade(name,parent):
    # Tapered twisted airfoil sections, radial along local Z, root at 0.85.
    rings=[(.85,.26),(1.6,.45),(3.1,.91),(5.6,.82),(8.9,.66),(12,.45),(15.4,.23),(17,.025)]
    verts=[];faces=[];n=12
    for z,chord in rings:
        twist=math.radians(18*(1-z/17)); sweep=-.035*z
        for j in range(n):
            a=2*math.pi*j/n; yy=chord*math.cos(a)+sweep;xx=.19*chord*math.sin(a)
            verts.append((xx*math.cos(twist)-yy*math.sin(twist),yy*math.cos(twist)+xx*math.sin(twist),z))
    for i in range(len(rings)-1):
        for j in range(n):faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces.extend([tuple(reversed(range(n))),tuple((len(rings)-1)*n+j for j in range(n))])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o)
    return finish(o,name,WHITE,'blades',parent)

for data in sorted((ROOT/'src/data/models').glob('*.json')):
    m=json.loads(data.read_text(encoding='utf-8'))
    for low in [False,True]:
        bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
        SEG=16 if low else 40
        WHITE=material('Ceramic white',(.81,.87,.90),.12,.28)
        SHELL=material('Nacelle shell',(.74,.83,.87),.15,.26)
        METAL=material('Machined steel',(.30,.42,.49),.8,.25)
        DARK=material('Dark frame',(.08,.14,.19),.55,.32)
        TEAL=material('Generator enamel',(.045,.49,.48),.4,.3)
        COPPER=material('Copper windings',(.82,.36,.12),.7,.25)
        BLUE=material('Electrical cabinets',(.15,.34,.57),.3,.32)
        direct=m['specs']['gearbox']['value'] is False
        geared=m['specs']['gearbox']['value'] is True
        root=group('Turbine')
        tower=group('Tower','tower',root)
        bpy.ops.mesh.primitive_cone_add(vertices=SEG,radius1=1.08,radius2=.57,depth=25,location=(0,0,-14))
        finish(bpy.context.object,'TowerSteel',WHITE,'tower',tower)
        for z in [-1.65,-10,-18]:torus('TowerFlange',(0,0,z),.6 if z==-1.65 else .8,.04,METAL,'tower',tower,axis='Z')
        yaw=group('Yaw','yaw',root)
        cylinder('YawBearing',(0,0,-1.5),.85,.35,METAL,'yaw',yaw,axis='Z')
        for a in [0,2.1,4.2]:cylinder('YawMotor',(.8*math.cos(a),.8*math.sin(a),-1.1),.17,.45,BLUE,'yaw',yaw,axis='Z')
        nacelle=group('Nacelle','nacelle',root)
        box('Shell',(1,0,.0),(8.8,3.25,3),SHELL,'nacelle',nacelle,.65)
        box('Bedplate',(1,0,-1.25),(8,2.8,.3),DARK,'nacelle',root,.08)
        rotor=group('RotorAssembly','rotor',root,(-4.15,0,0))
        cylinder('HubCore',(0,0,0),.72,1.3,METAL,'hub',rotor)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=SEG,ring_count=12,location=(-.75,0,0));o=bpy.context.object;o.scale=(1.1,.83,.83);finish(o,'HubCover',WHITE,'hub',rotor)
        for i in range(3):
            arm=group(f'BladeArm_{i}',parent=rotor);arm.rotation_euler[0]=i*2*math.pi/3
            pitch=group(f'Pitch_{i}','pitch',arm)
            cylinder(f'PitchBearing_{i}',(0,0,.92),.35,.3,METAL,'pitch',pitch,axis='Z')
            blade(f'Blade_{i}',pitch)
        shaft=group('MainShaft','shaft',root)
        cylinder('LowSpeedShaft',(-2.45,0,0),.25,3.1,METAL,'shaft',shaft)
        cylinder('MainBearing',(-2.6,0,0),.55,.45,DARK,'shaft',shaft)
        generator=group('Generator','generator',root)
        gx=-1.9 if direct else 1.9; gr=1.27 if direct else .79
        cylinder('GeneratorStator',(gx,0,0),gr,.85 if direct else 1.9,TEAL,'generator',generator)
        moving=group('GeneratorRotor','generator',generator,(gx-.55,0,0))
        cylinder('GeneratorRotorDisk',(0,0,0),gr*.76,.12,METAL,'generator',moving)
        if direct:torus('StatorCopperCoil',(gx-.58,0,0),gr*.86,.10,COPPER,'generator',generator)
        for i in range(12):
            a=i*2*math.pi/12
            r=gr*(.57 if direct else .85)
            box(f'Magnet_{i}' if direct else f'RotorWinding_{i}',(0,r*math.sin(a),r*math.cos(a)),(.24,.19,.23),BLUE if direct else COPPER,'generator',moving,.03)
        for x in [gx-.5,gx+.5]:box('GeneratorFoot',(x,0,-.9),(.3,1.7,.5),DARK,'generator',generator,.04)
        if geared:
            gear=group('Gearbox','gearbox',root)
            box('GearHousing',(-.75,0,0),(1.8,1.65,1.55),METAL,'gearbox',gear,.28)
            for j in range(3):
                cog=group(f'GearWheel_{j}','gearbox',gear,(-1.1+j*.42,-.95,0))
                cylinder('GearDisk',(0,0,0),.43,.12,COPPER,'gearbox',cog)
                for i in range(12):
                    a=i*math.pi/6;box('GearTooth',(0,.46*math.cos(a),.46*math.sin(a)),(.18,.13,.13),METAL,'gearbox',cog,.01)
            cylinder('HighSpeedShaft',(.8,0,0),.14,1.9,METAL,'shaft',shaft)
        converter=group('Converter','converter',root)
        box('ConverterCabinet',(3.4,.9,.05),(1.0,.7,1.6),BLUE,'converter',converter,.1)
        for z in [-.4,-.1,.2,.5]:box('ConverterVent',(2.89,.9,z),(.03,.5,.05),DARK,'converter',converter,.005)
        transformer=group('Transformer','transformer',root)
        box('TransformerCore',(3.2,-.85,-.3),(1.1,.65,1.0),COPPER,'transformer',transformer,.08)
        for x in [2.9,3.2,3.5]:cylinder('TransformerInsulator',(x,-.85,.42),.10,.28,WHITE,'transformer',transformer,axis='Z')
        # glTF loop, 12 RPM at native playback speed; scaled by estimated rotor RPM.
        bpy.context.scene.render.fps=24;bpy.context.scene.frame_start=1;bpy.context.scene.frame_end=121
        rotor.rotation_mode='XYZ'
        rotor.rotation_euler[0]=0;rotor.keyframe_insert(data_path='rotation_euler',index=0,frame=1)
        rotor.rotation_euler[0]=-2*math.pi;rotor.keyframe_insert(data_path='rotation_euler',index=0,frame=121)
        if rotor.animation_data and rotor.animation_data.action:
            action=rotor.animation_data.action;action.name='NormalOperation'
            for layer in action.layers:
                for strip in layer.strips:
                    for bag in strip.channelbags:
                        for curve in bag.fcurves:
                            for key in curve.keyframe_points:key.interpolation='LINEAR'
        bpy.context.scene.frame_set(1)
        if not low:bpy.ops.wm.save_as_mainfile(filepath=str(BLEND/(m['id']+'.blend')))
        target=OUT/(m['id']+('-low' if low else '')+'.glb')
        bpy.ops.export_scene.gltf(filepath=str(target),export_format='GLB',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_animations=True,export_extras=True,export_animation_mode='ACTIVE_ACTIONS',export_frame_range=True,export_force_sampling=True)
        print('EXPORTED',target.name)
