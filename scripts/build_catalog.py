from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'src/data/models'
OUT.mkdir(parents=True, exist_ok=True)
def fact(value=None, source=None, scope='missing', note='No consta en los documentos disponibles.'):
    return dict(value=value, source=source, scope=scope, note=note)
def park(name, refs, level='A', note='', height=None, installer=None):
    return dict(name=name, references=refs, evidence=level, note=note, hubHeightM=fact(height, 'Informe p. 5 [B13]' if height else None, 'installed' if height else 'missing', 'Altura de torre reportada; confirmar definición de altura de buje.' if height else 'No consta una altura de buje instalada.'), installationProvider=installer)
def model(id, maker, name, power, parks, page=4):
    fields={k:fact() for k in ['ratedPowerMW','rotorDiameterM','hubHeightM','bladeCount','generator','gearbox','powerControl','cutInMS','ratedWindMS','cutOutMS','converter']}
    fields['ratedPowerMW']=fact(power, f'Informe p. {page}', 'installed', 'Potencia unitaria descrita en el catálogo; no equivale a potencia neta de conexión.') if power else fact(note='Discrepancia: 2 MW por unidad frente a 8,4 MW para cuatro unidades. No se fija variante.')
    return dict(id=id,manufacturer=maker,model=name,supplier=fact(maker,f'Informe p. {page}','installed','Fabricante documentado; proveedor contractual independiente no identificado.'),parks=parks,specs=fields,notes=[],simulation=dict(fixedWindMS=8,ratedPowerMW=power or 2,cutInMS=3,ratedWindMS=12,cutOutMS=20,tipSpeedRatio=7,maxRotorRPM=16,pitchBaseDeg=1.5,pitchGainDegPerMS=2,gearRatio=90,bladeCount=3,rotorDiameterM=110,hubHeightM=100,assumptions=['Viento fijo de 8 m/s, uniforme, alineado con el rotor.','Curva cúbica simplificada sin pérdidas; no es una curva medida ni certificada.','RPM estimadas con relación de velocidad de punta λ=7, límite de 16 RPM.','Pitch didáctico: 1,5° bajo viento nominal, +2° por m/s sobre nominal.','Proporciones y ubicación de componentes esquemáticas, sin planos por número de serie.','Altura visual normalizada; las posiciones del convertidor y transformador son didácticas.']),asset=dict(glb=f'models/{id}.glb',lod=f'models/{id}-low.glb',schematic=True))
def setf(m,key,value,source,scope='family',note='Referencia de familia; no certifica la revisión instalada.'):
    m['specs'][key]=fact(value,source,scope,note)

gw=model('goldwind-gw1500-87','Goldwind','GW1500-87',1.5,[park('Cuel',['B01'])])
for k,v in {'rotorDiameterM':87,'bladeCount':3,'generator':'PMSG · síncrono de imanes permanentes','gearbox':False,'powerControl':'pitch','cutInMS':3,'ratedWindMS':9.9,'cutOutMS':22,'converter':'Escala completa (IGBT)'}.items(): setf(gw,k,v,'Goldwind 1.5 MW, tabla de datos p. PDF 6 [B19]')
gw['notes']=['GW1500-87 es la denominación del parque; GW 87/1500 es la nomenclatura del folleto.','La altura instalada de Cuel no consta en el corpus.']
v42=model('vestas-v150-42','Vestas','V150 Mk3B · 4,2 MW',4.2,[park('Lomas de Duqueco',['B02','B04'])])
v43=model('vestas-v150-43','Vestas','V150 · 4,3 MW',4.3,[park('Campo Lindo',['B11'],note='Alcance de quince unidades ensayadas en 2023.'),park('San Matías',['B12','B13'],note='Inconsistencia «N163 V150» conciliada como Vestas V150 por B13.',height=140)])
for m in [v42,v43]:
    for k,v in {'rotorDiameterM':150,'bladeCount':3,'gearbox':True,'powerControl':'pitch','converter':'Escala completa'}.items():setf(m,k,v,'Informe p. 7; Vestas 4 MW p. 9 [B25]')
    m['notes'].append('El folleto V150-4.2/4.5 no documenta una variante 4,3 MW ni confirma umbrales de las unidades chilenas.')
setf(v42,'generator','Inducción · subtipo no indicado','Informe p. 7 [B04]','installed','Generador de inducción y convertidor completo documentados para Mk3B. No se etiqueta DFIG.')
v43['notes'].append('El generador de inducción del Mk3B de 4,2 MW no se transfiere a las variantes de 4,3 MW: su tipo queda sin documentar.')
v136=model('vestas-v136-36','Vestas','V136 CP3.6 · PO1 · 50 Hz',3.6,[park('Negrete',['B02','B05'],note='Diez unidades de 3,6 MW; publicación de instalador difiere (11 × 3,45 MW).',installer='Tecnorenova (referencia discrepante B23)')])
setf(v136,'generator','Inducción · subtipo no indicado','Informe p. 7 [B05]','installed','Inducción con convertidor de escala completa; no se infiere DFIG.')
setf(v136,'converter','Escala completa','Informe p. 7 [B05]','installed','Configuración ensayada de Negrete.')
v136['notes']=['No se transfieren diámetro, umbrales, transmisión ni opciones del folleto V136-4.2 a CP3.6. El interior muestra únicamente la cadena funcional conocida.']
n149=model('nordex-n149-48','Nordex','N149 / Delta4000 · 4,8 MW',4.8,[park('Alena',['B03','B06'],'B','Pedido 2019; presencia en registro 2023. Reconfirmar inventario.'),park('Los Olmos',['B07','B08'],'A/B','A plataforma y cantidad; B identificación N149.',installer='Greenwork'),park('Mesamavida',['B09','B10'],'A/B','A plataforma/etapa III; B N149. Montaje parcial.',installer='Tecnorenova')])
for k,v in {'rotorDiameterM':149.1,'generator':'DFIG · asíncrono doblemente alimentado','gearbox':True,'powerControl':'pitch','cutInMS':3,'cutOutMS':20}.items():setf(n149,k,v,'Nordex N149/4.X, HTML local [B24]')
n149['specs']['cutOutMS']['note']='Base de familia 20 m/s; opciones específicas hasta 26 m/s. Umbral de cada parque sin confirmar.'
n149['notes']=['N149 confirmado por suministro/montaje; Delta4000 es la plataforma confirmada en Los Olmos y Mesamavida.','Multiplicadora de dos etapas planetarias y una cilíndrica; relación de transmisión no documentada.','Alturas comerciales hasta 164 m no identifican la torre instalada.']
v110=model('vestas-v110-20','Vestas','V110 · 2,0 MW',2,[park('Los Buenos Aires',['B14','B20'],note='Antecedente de 2019; reconfirmar configuración por unidad.')])
for k,v in {'rotorDiameterM':110,'bladeCount':3,'generator':'DFIG · doblemente alimentado con anillos rozantes','gearbox':True,'powerControl':'pitch','cutInMS':3,'cutOutMS':21}.items():setf(v110,k,v,'Vestas 2 MW, ficha V110 p. PDF 6 [B26]')
v110['notes']=['Opciones comerciales de altura: 75, 80, 95, 110, 120 y 125 m; no prueban la altura instalada.','Los ~90 m del relato de un incidente no se usan como altura de buje.']
v112=model('vestas-v112-30','Vestas','V112 · 3,0 MW',3,[park('Raki',['B15']),park('Huajache',['B15'])])
setf(v112,'gearbox',True,'Informe p. 8; Vestas LCA 2011 p. PDF 72 [B27]')
v112['notes']=['LCA histórica confirma componentes, sin certificar generador ni etapas de transmisión de Raki/Huajache. No se deduce diámetro del nombre del modelo.']
e110=model('envision-e110-21','Envision','E110 · 2,1 MW',2.1,[park('La Esperanza',['B03','B16'],'B','Cinco máquinas documentadas en montaje 2016.',installer='Tecnorenova')])
e110['notes']=['Sin ficha OEM verificable de esta variante en el corpus. Geometría exterior genérica y cadena de conversión abstracta; no se inventa arquitectura.']
g114=model('gamesa-g114','Gamesa','G114 · variante pendiente',None,[park('Las Peñas',['B17','B18'],'B','Cuatro unidades; discrepancia 2 MW / 8,4 MW.',installer='CJR Renewables')],5)
g114['notes']=['La variante G114/2000 aparece en el informe, pero no resuelve la discrepancia de potencia del parque.','Potencia de 2 MW usada SOLO como supuesto del escenario, no como ficha instalada.']
models=[gw,v42,v136,n149,v43,v110,v112,e110,g114]
for m in models:
    for k in ['rotorDiameterM','cutInMS','ratedWindMS','cutOutMS','bladeCount']:
        f=m['specs'][k]
        if f['value'] is not None: m['simulation'][k]=f['value']
        else: m['simulation']['assumptions'].append(f'{k}={m["simulation"][k]}: supuesto para animación; dato documental ausente.')
    if m['specs']['gearbox']['value'] is True: m['simulation']['assumptions'].append('Relación de transmisión ilustrativa 90:1, no documentada.')
    if m['specs']['ratedPowerMW']['value'] is None: m['simulation']['assumptions'].append('ratedPowerMW=2: capacidad ilustrativa sin variante confirmada.')
    (OUT / (m['id']+'.json')).write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
print('Catálogo:',len(models),'modelos')
