"""Model-specific silhouettes and drivetrain layouts, reconstructed from cited sources.
Internal dimensions and service equipment placement remain illustrative.
"""
import math

def configure(api):
    keys=['group','box','cylinder','torus','beam','pipe','bolt_ring','gear_mesh','planetary_stage','rounded_shell','label_mesh','LOW','SEG','PEARL','SILVER','GRAPHITE','SAGE','COPPER','GOLD','RUBBER','MAKER','REAR_RED']
    globals().update({key:api[key] for key in keys})

def identity_profile(p,model):
    maker=model['manufacturer'];p['style']=maker.lower()
    defaults={
      'Envision':dict(gx=2.50,gz=1.10,gr=.62,gl=1.55,planet_x=-.75,planet_scale=.88,px=[.12,.76],ims=[.15,.22],bearings=[-3.18,-2.23],bearing_r=.52,conv=[4.5,.95,-.12],trans=[3.9,-.92,-.56],end=5.4,nose=1.70,shape=.28),
      'Gamesa':dict(gx=2.85,gz=.92,gr=.82,gl=1.9,planet_x=-.90,planet_scale=1.02,px=[.20,.88],ims=[.25,.24],bearings=[-3.20,-2.20],bearing_r=.63,conv=[4.8,1.03,-.05],trans=[4.5,-1.05,-.55],end=6.0,nose=1.10,shape=.64),
      'Nordex':dict(gx=3.10,gz=1.18,gr=.91,gl=1.95,planet_x=-1.30,planet_scale=1.08,px=[.64],ims=[0,0],bearings=[-3.10],bearing_r=.80,conv=[5.0,1.22,.02],trans=[5.0,-1.20,-.58],end=6.6,nose=1.48,shape=.25),
      'Vestas':dict(gx=2.38,gz=1.04,gr=.71,gl=1.55,planet_x=-1.10,planet_scale=.84,px=[-.12,.56],ims=[.18,.25],bearings=[-3.12,-2.48],bearing_r=.56,conv=[4.5,1.10,-.06],trans=[4.8,-.98,-.56],end=6.9,nose=1.95,shape=.33),
      'Goldwind':dict(gx=-1.65,gz=0,conv=[2.75,.90,.13],trans=[2.85,-.65,-.52],end=4.8,nose=1.34,shape=.54),
    }
    p.update(defaults[maker]);return p

def bedplate(root,p):
    frame=group('Bedplate','nacelle',root)
    end=p['end']-.35
    if p['style']=='gamesa':
        # Four-point G114 reference: cast front frame around two bearing seats.
        for y in [-.87,.87]:
            box('Cast front mainframe',(-2.05,y,-.84),(3.5,.42,.65),MAKER,'nacelle',frame)
            beam('Cast bearing arch',(-3.3,y,-.80),(-3.3,0,-.55),.12,MAKER,'nacelle',frame)
        box('Cast yaw crossmember',(-.55,0,-1.12),(1.4,2.5,.42),MAKER,'nacelle',frame)
    elif p['style']=='nordex':
        for y in [-1.17,1.17]:
            beam('Three-point cast frame',(-3.25,y*.55,-.6),(-.8,y,-1.18),.21,GRAPHITE,'nacelle',frame,12)
            box('Gearbox torque foot',(-1.3,y,-1.12),(.8,.5,.4),MAKER,'nacelle',frame)
    elif p['style']=='vestas':
        box('Integrated module base',(-1.7,0,-.98),(3.9,1.32,.44),SILVER,'nacelle',frame)
        for y in [-.7,.7]:box('Integrated module stiffener',(-2.1,y,-.7),(2.65,.18,.35),MAKER,'nacelle',frame)
    else:
        for y in [-.85,.85]:box('PEAB support frame',(-1.6,y,-1.0),(3.8,.22,.45),PEARL,'nacelle',frame)
    for y in [-1.17,1.17]:
        box('Rear platform rail',((end-1.5)/2,y,-1.30),(end+1.5,.18,.25),GRAPHITE,'nacelle',frame)
        count=20 if LOW else 44
        for i in range(count):box('Service grating',(-3.5+(end+3.5)*i/count,y,-1.02),(.035,.42,.045),SILVER,'nacelle',frame)
        for x in [-3.4,-1.0,1.5,end]:
            beam('Safety stanchion',(x,y,-1),(x,y,-.47),.024,GOLD,'nacelle',frame)
        beam('Safety handrail',(-3.4,y,-.47),(end,y,-.47),.026,GOLD,'nacelle',frame)
    return frame

def drivetrain(root,p,model):
    shaft=group('MainShaft','shaft',root)
    front=-4.10;back=p['planet_x']-.14
    spin=group('MainShaftSpin','shaft',shaft,((front+back)/2,0,0),ratio=-1)
    cylinder('Model main shaft',(0,0,0),.34 if p['style']=='nordex' else .275,back-front,SILVER,'shaft',spin)
    box('Shaft witness',(.0,-.278,.025),((back-front)*.8,.015,.035),GOLD,'shaft',spin)
    for i,x in enumerate(p['bearings']):
        r=p['bearing_r'];housing=group('MainBearing_'+str(i),'shaft',shaft)
        cylinder('Bearing race',(x,0,0),r,.34,SILVER,'shaft',housing,inner=.33 if r>.6 else .29)
        torus('Bearing seal',(x-.18,0,0),r*.86,.028,RUBBER,'shaft',housing)
        bolt_ring('Bearing face screws',(x-.20,0,0),r*.84,12 if LOW else 20,GRAPHITE,'shaft',housing)
        if p['style']=='nordex':
            for y in [-.42,.42]:beam('Cast mainbearing stand',(x,y,-.32),(x,y,-1.05),.19,MAKER,'shaft',housing,12)
        elif p['style']=='gamesa':
            for y in [-.48,.48]:box('Four-point bearing seat',(x,y,-.61),(.65,.26,.85),MAKER,'shaft',housing)
        else:
            box('Bearing module housing',(x,0,-.48),(.48,1.10,.50),PEARL,'shaft',housing)
    gear=group('Gearbox','gearbox',root)
    gear['stageLayoutScope']='family'
    gear['stageLayout']=model['engineering']['layout']
    planetary_stage(gear,'PlanetaryStage1',p['planet_x'],p['planet_scale'],-1)
    if p['style']=='nordex':
        planetary_stage(gear,'PlanetaryStage2',-.28,.82,-5)
        x=p['px'][0];d=p['gz'];rout=d/4.6;rin=d-rout
        a=group('ParallelStageInput','gearbox',gear,(x,0,0),ratio=-25)
        gear_mesh('Final spur input',rin,36,.31,SILVER,a,bore=.18,tooth_depth=.035)
        b=group('ParallelStageOutput','gearbox',gear,(x,0,p['gz']),ratio=p['ratio'])
        gear_mesh('Final spur pinion',rout,10,.33,GOLD,b,bore=.075,tooth_depth=.025)
        ratio=p['ratio']
        for y in [-1.4,1.4]:
            cylinder('Elastomer torque support',(p['planet_x'],y,-.55),.20,.65,RUBBER,'gearbox',gear,axis='Z')
            beam('Torque arm',(p['planet_x'],y,-.35),(p['planet_x'],.9 if y>0 else -.9,0),.15,MAKER,'gearbox',gear)
    else:
        first,second=p['px'];iy,iz=p['ims'];d=math.hypot(iy,iz)
        a=group('HelicalStage1_Input','gearbox',gear,(first,0,0),ratio=-5)
        gear_mesh('First parallel input',d*.75,54,.25,SILVER,a,bore=.065,helix=.18,tooth_depth=.012)
        b=group('HelicalStage1_Output','gearbox',gear,(first,iy,iz),ratio=15)
        gear_mesh('First parallel output',d*.25,18,.25,GOLD,b,bore=.025,helix=-.54,tooth_depth=.01)
        mid=group('IntermediateShaftSpin','shaft',shaft,((first+second)/2,iy,iz),ratio=15)
        cylinder('Intermediate shaft',(0,0,0),.05,second-first+.32,SILVER,'shaft',mid)
        d2=math.hypot(iy,p['gz']-iz);last=p['ratio']/15;small=d2/(last+1);big=d2-small
        a=group('HelicalStage2_Input','gearbox',gear,(second,iy,iz),ratio=15)
        teeth=118 if p['style']=='envision' else 108
        pinion=15 if p['style']=='envision' else 18
        gear_mesh('Second parallel input',big,teeth,.28,SILVER,a,bore=.08,helix=.15,tooth_depth=.014)
        b=group('HelicalStage2_Output','gearbox',gear,(second,0,p['gz']),ratio=-p['ratio'])
        gear_mesh('Second parallel output',small,pinion,.29,GOLD,b,bore=.035,helix=-.60,tooth_depth=.012)
        ratio=-p['ratio']
    # Cast cases are different by platform, leaving a translucent inspection cover.
    for i in range(2 if p['style']=='nordex' else 1):
        x=p['planet_x']+i*1.0;r=(1.28*p['planet_scale']) if i==0 else 1.05
        cylinder('GearboxCasing_barrel_'+str(i),(x,0,0),r+.14,.58,MAKER,'gearbox',gear,inner=r-.05,separate=True)
        bolt_ring('Case bolt flange',(x-.33,0,0),r+.10,16 if LOW else 30,SILVER,'gearbox',gear,size=.045)
    if p['style']=='envision':
        box('GearboxCasing_PEAB tower',(.43,.35,.57),(1.35,1.16,1.98),MAKER,'gearbox',gear,separate=True)
    elif p['style']=='gamesa':
        box('GearboxCasing_G114 rear',(.3,.24,.44),(1.6,1.55,1.75),MAKER,'gearbox',gear,separate=True)
    elif p['style']=='vestas':
        box('GearboxCasing_V110 module',(-.2,.22,.44),(1.9,1.35,1.75),SILVER,'gearbox',gear,separate=True)
    else:
        box('GearboxCasing_Delta4000 rear',(.60,.35,.62),(1.30,1.85,2.25),MAKER,'gearbox',gear,separate=True)
    lastx=p['px'][-1];end=p['gx']-p['gl']/2-.08
    high=group('HighSpeedCoupling','shaft',shaft,((lastx+end)/2,0,p['gz']),ratio=ratio)
    cylinder('High speed shaft',(0,0,0),.07,end-lastx+.12,SILVER,'shaft',high)
    torus('Flexible coupling',(0,0,0),.20,.055,RUBBER,'shaft',high)
    cylinder('Brake disc',(.14,0,0),.31,.035,SILVER,'shaft',high)
    box('Stationary brake caliper',((lastx+end)/2+.14,-.29,p['gz']+.04),(.17,.15,.24),GRAPHITE,'shaft',shaft)
    pipe('Gear lubrication line',[(p['planet_x'],-1.03,-.35),(.4,-1.03,-.35),(.4,-1.03,.72)],.023,GOLD,'gearbox',gear)
    gen=group('Generator','generator',root)
    x,z,r,length=p['gx'],p['gz'],p['gr'],p['gl']
    rotor=group('GeneratorRotor','generator',gen,(x,0,z),ratio=ratio)
    cylinder('DFIG wound rotor',(0,0,0),r*.51,length*.87,GRAPHITE,'generator',rotor)
    count=12 if LOW else 24
    for i in range(count):
        a=math.tau*i/count;yy,zz=r*.55*math.cos(a),r*.55*math.sin(a)
        beam('Rotor winding',(-length*.45,yy,zz),(length*.45,yy,zz),.026,COPPER,'generator',rotor,6)
        beam('Stator winding',(x-length*.45,yy*1.56,z+zz*1.56),(x+length*.45,yy*1.56,z+zz*1.56),.042,COPPER,'generator',gen,6)
    for side in [-1,1]:
        xx=side*length*.48
        torus('Rotor winding crown',(xx,0,0),r*.57,.065,COPPER,'generator',rotor)
        torus('Stator end winding',(x+xx,0,z),r*.84,.075,COPPER,'generator',gen)
        cylinder('Generator end shield',(x+xx,0,z),r+.11,.11,MAKER,'generator',gen,inner=r*.67)
        bolt_ring('Generator end bolts',(x+xx-.06,0,z),r+.045,12 if LOW else 24,SILVER,'generator',gen,size=.034)
    for j in range(3):
        xx=length*.55+.09*j
        torus('DFIG slip ring',(xx,0,0),r*.37,.028,COPPER,'generator',rotor)
        box('Carbon brush',(x+xx,-r*.40,z),(.07,.10,.12),RUBBER,'generator',gen)
    cylinder('GeneratorCasing_main',(x,0,z),r+.04,length,MAKER,'generator',gen,inner=r-.05,separate=True)
    if p['style']=='envision':
        for j in range(10 if LOW else 22):
            torus('Air-cooling fin',(x-length*.43+j*(length*.86/(10 if LOW else 22)),0,z),r+.085,.018,MAKER,'generator',gen)
        cylinder('Rear fan guard',(x+length*.55,0,z),r*.93,.08,GRAPHITE,'generator',gen,inner=r*.7)
    elif p['style']=='nordex':
        box('GeneratorCasing_liquid jacket',(x,.22,z),(length,1.25,1.35),MAKER,'generator',gen,separate=True)
        for yy in [-.65,.65]:
            pipe('Generator liquid cooling hose',[(x+.3,yy,z-.4),(x+.8,yy,-.6),(5.6,yy,1.25)],.055,RUBBER,'generator',gen)
    elif p['style']=='vestas':
        box('CoolerTop air duct',(x+.75,.35,z+.2),(.7,.9,.9),SILVER,'generator',gen)
        pipe('CoolerTop cooling connection',[(x+.9,.45,z+.45),(3.8,.7,1.55),(5,.7,2.2)],.075,RUBBER,'generator',gen)
    else:
        for j in range(7):box('Motor casing rib',(x-.7+j*.22,.46,z),(.035,.35,r*1.3),MAKER,'generator',gen)
    # Pedestals meet the machine casing and the platform; no floating generator.
    base_z=-1.16; seat_z=z-r*.72
    for xx in [x-length*.32,x+length*.32]:
        for yy in [-r*.63,r*.63]:
            box('Generator mounting pedestal',(xx,yy,(base_z+seat_z)/2),(.32,.30,seat_z-base_z),MAKER if p['style']=='gamesa' else SILVER,'generator',gen)
            box('Generator resilient mounting pad',(xx,yy,base_z),(.42,.40,.09),RUBBER,'generator',gen)
    for xx in [x-length*.32,x+length*.32]:
        box('Generator platform crossmember',(xx,0,-1.23),(.25,2.5,.18),GRAPHITE,'nacelle',gen)
    box('Generator terminal enclosure',(x,-r*.65,z+r*.78),(.65,.48,.32),MAKER,'generator',gen)
    electrical(root,p)
    return {'generator':[x,z,0],'converter':[p['conv'][0],p['conv'][2],-p['conv'][1]],'transformer':[p['trans'][0],p['trans'][2],-p['trans'][1]]}

def electrical(root,p):
    converter=group('Converter','converter',root);x,y,z=p['conv']
    count=3 if p['style']=='nordex' else 2
    for i in range(count):
        xx=x+(i-(count-1)/2)*.43
        box('Converter cabinet',(xx,y,z),(.40,.70,1.85 if p['style']=='nordex' else 1.52),PEARL,'converter',converter)
        box('Cabinet door seam',(xx,y-.36,z),(.34,.016,1.30),GRAPHITE,'converter',converter)
        box('Cabinet door',(xx,y-.38,z),(.32,.018,1.26),PEARL,'converter',converter)
        cylinder('Cabinet handle',(xx+.10,y-.40,z),.025,.12,SILVER,'converter',converter,axis='Z',segments=8)
    transformer=group('Transformer','transformer',root);tx,ty,tz=p['trans']
    box('Transformer core',(tx,ty,tz),(.86,.65,.62),GRAPHITE,'transformer',transformer)
    for i in range(3):
        xx=tx-.28+i*.28
        cylinder('Transformer copper coil',(xx,ty,tz+.05),.17,.58,COPPER,'transformer',transformer,axis='Z')
        cylinder('HV insulator',(xx,ty,tz+.48),.055,.28,PEARL,'transformer',transformer,axis='Z')
    auxiliary=group('AuxiliaryEquipment','nacelle',root)
    if p['pitch_kind']=='cylinder':
        box('Hydraulic power unit',(-.3,-1.05,-.77),(.85,.45,.5),MAKER,'nacelle',auxiliary)
        for xx in [-.65,-.30]:
            cylinder('Pitch pressure accumulator',(xx,-1.03,-.3),.13,.58,GRAPHITE,'nacelle',auxiliary,axis='Z')
    else:
        box('Pitch electrical cabinet',(-.35,-1.04,-.6),(.68,.35,.75),PEARL,'nacelle',auxiliary)
        for j in range(4):cylinder('Supercapacitor module',(-.58+j*.15,-1.04,-.1),.06,.23,MAKER,'nacelle',auxiliary,axis='Z',segments=10)
    pipe('Cable trunk',[(x,y,-.9),(1,y,-.9),(0,y,-1.1),(0,0,-2.2)],.055,RUBBER,'nacelle',auxiliary)

def body(root,p):
    nacelle=group('Nacelle','nacelle',root);style=p['style']
    if style=='goldwind':
        xs=[-3.35,-2.3,-1.3,.5,2.5,4.2,4.8];ws=[2.9,4.25,4.45,3.2,2.95,2.45,1.9];hs=[2.8,4.15,4.2,2.8,2.6,2.3,2.1]
    elif style=='envision':
        xs=[-3.55,-3.25,-1.2,2.9,4.8,5.4];ws=[2.0,2.85,3.05,3.05,2.9,2.55];hs=[2.1,3.45,3.70,3.70,3.35,2.9]
    elif style=='gamesa':
        xs=[-3.55,-3.2,-1.8,.8,3.6,5.4,6.0];ws=[2.7,3.2,3.4,3.45,3.45,3.0,2.7];hs=[2.8,3.65,3.95,3.95,3.90,3.25,2.8]
    elif style=='nordex':
        xs=[-3.55,-3.15,-1.3,2.8,5.0,6.1,6.6];ws=[2.6,3.8,4.25,4.35,4.25,4.05,3.9];hs=[2.8,3.9,4.3,4.5,4.35,4.0,3.8]
    else:
        xs=[-3.5,-3.1,-1.6,1,4.5,6.5,6.9];ws=[2.6,3.5,3.5,3.5,3.36,3.0,2.8];hs=[2.7,4,4,4,3.88,3.6,3.4]
    if style=='nordex':
        rounded_shell(style,xs[:5],ws[:5],hs[:5],nacelle,shape=p['shape'])
        rounded_shell(style+'_rear',xs[4:],ws[4:],hs[4:],nacelle,shape=p['shape'],material_override=REAR_RED)
    else:
        rounded_shell(style,xs,ws,hs,nacelle,shape=p['shape'])
    p['sections']=(xs,ws,hs)
    for x in [-2.5,.3,3.2,p['end']-.4]:
        width=3.0 if style!='nordex' else 3.8
        beam('Interior roof support',(x,width/2,-1),(x,width/2,1.35),.045,PEARL,'nacelle',nacelle)
        beam('Interior roof support',(x,width/2,1.35),(x,-width/2,1.35),.045,PEARL,'nacelle',nacelle)
    if style=='nordex':
        red=globals()['REAR_RED']
        box('Shell_Nordex red rear',(6.62,0,-.02),(.055,3.74,3.3),red,'nacelle',nacelle,separate=True)
        rack=group('NordexRearRadiator','nacelle',nacelle)
        for y in [-1.16,0,1.16]:
            box('Radiator panel frame',(6.26,y,2.0),(.20,1.1,1.6),SILVER,'nacelle',rack)
            for j in range(8 if LOW else 18):box('Radiator lamella',(6.12,y-.5+j/(8 if LOW else 18),2.0),(.05,.025,1.45),GRAPHITE,'nacelle',rack)
        box('Shell_Nordex dark roof hatch',(1.2,0,2.22),(3.8,1.7,.055),GRAPHITE,'nacelle',nacelle,separate=True)
    elif style=='vestas':
        cooler=group('Shell_CoolerTop_Assembly','nacelle',nacelle)
        box('Shell_CoolerTop fairing',(5,0,2.61),(2.45,2.5,1.25),PEARL,'nacelle',cooler,separate=True)
        for i in range(10 if LOW else 20):box('CoolerTop radiator',(4.0+i*.1,0,3.28),(.035,2.25,.14),SILVER,'nacelle',cooler)
    elif style=='envision':
        for x in [1.5,3.5]:box('Shell_Envision roof hatch',(x,0,1.56),(1.45,1.45,.045),PEARL,'nacelle',nacelle,separate=True)
        for i in range(8):box('Shell_Envision tail vent',(5.44,-.85+i*.24,.7),(.045,.06,.8),GRAPHITE,'nacelle',nacelle,separate=True)
    elif style=='gamesa':
        for y in [-.8,.8]:box('Shell_G114 roof hatch',(3.5,y,1.61),(1.5,.6,.04),PEARL,'nacelle',nacelle,separate=True)
    mast_x=p['end']-1.1;mast_z=1.85 if style=='nordex' else 1.65
    beam('Instrument mast',(mast_x,0,mast_z),(mast_x+.28,0,mast_z+1.0),.027,SILVER,'nacelle',nacelle)
    anemo=group('Anemometer','nacelle',nacelle,(mast_x+.28,0,mast_z+1.04),ratio=7,axis='y')
    for i in range(3):
        a=math.tau*i/3
        beam('Wind sensor arm',(0,0,0),(.23*math.cos(a),.23*math.sin(a),0),.014,SILVER,'nacelle',anemo)
        cylinder('Wind sensor cup',(.23*math.cos(a),.23*math.sin(a),0),.065,.06,MAKER,'nacelle',anemo,axis='Z',segments=8)
    return nacelle

def trim(root,p):
    trim=group('Shell_IdentityDetails','nacelle',root)
    xs,ws,hs=p['sections']
    def side(x):
        for i in range(len(xs)-1):
            if xs[i]<=x<=xs[i+1]:return -(ws[i]+(ws[i+1]-ws[i])*(x-xs[i])/(xs[i+1]-xs[i]))/2-.025
        return -ws[-1]/2-.025
    for x in [-1.3,.6,2.5,p['end']-.7]:
        y=side(x)
        pipe('Shell_panel separation',[(x,y,-.65),(x,y,.75)],.009,GRAPHITE,'nacelle',trim)
    x=-.8;y=side(x)-.02
    label_mesh('Shell_manufacturer',p['maker'].upper() if p['style']!='gamesa' else 'Gamesa',(x,y,.45),.33 if p['style']=='nordex' else .29,trim,MAKER)
    label_mesh('Shell_model',p['label'],(x+.04,y,.10),.15,trim,GRAPHITE)
    doorx=p['end']-1.4;dy=side(doorx)
    box('Shell_Service door',(doorx,dy,.12),(.9,.035,.9),PEARL,'nacelle',trim)
    pipe('Shell_Service door seal',[(doorx-.46,dy-.03,-.34),(doorx-.46,dy-.03,.58),(doorx+.46,dy-.03,.58),(doorx+.46,dy-.03,-.34)],.013,RUBBER,'nacelle',trim)
    beam('Shell_Service handle',(doorx+.26,dy-.05,.1),(doorx+.26,dy-.05,.3),.017,SILVER,'nacelle',trim)
