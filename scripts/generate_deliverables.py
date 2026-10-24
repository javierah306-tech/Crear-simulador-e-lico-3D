from pathlib import Path
import json,csv
root=Path(__file__).resolve().parents[1]
models=[json.loads(p.read_text(encoding='utf-8')) for p in (root/'src/data/models').glob('*.json')]
doc=root/'docs';doc.mkdir(exist_ok=True)
def fact_schema(kind):
    return {'type':'object','additionalProperties':False,'required':['value','source','scope','note'],'properties':{'value':{'type':[kind,'null']},'source':{'type':['string','null']},'scope':{'enum':['installed','family','missing']},'note':{'type':'string','minLength':1}},'allOf':[{'if':{'properties':{'scope':{'const':'missing'}}},'then':{'properties':{'value':{'type':'null'},'source':{'type':'null'}}},'else':{'properties':{'value':{'type':kind},'source':{'type':'string','minLength':1}}}}]}
numbers=['ratedPowerMW','rotorDiameterM','hubHeightM','bladeCount','cutInMS','ratedWindMS','cutOutMS']
strings=['generator','powerControl','converter']
specs={**{k:fact_schema('number') for k in numbers},**{k:fact_schema('string') for k in strings},'gearbox':fact_schema('boolean')}
simkeys=list(models[0]['simulation'])
schema={'$schema':'http://json-schema.org/draft-07/schema#','$id':'urn:smartwind:turbine-schema','title':'Aerogenerador documental y simulación educativa','type':'object','additionalProperties':False,'required':list(models[0]),'properties':{'id':{'type':'string','pattern':'^[a-z0-9-]+$'},'manufacturer':{'type':'string'},'model':{'type':'string'},'supplier':fact_schema('string'),'parks':{'type':'array','minItems':1,'items':{'type':'object','additionalProperties':False,'required':['name','references','evidence','note','hubHeightM','installationProvider'],'properties':{'name':{'type':'string'},'references':{'type':'array','items':{'type':'string'}},'evidence':{'type':'string'},'note':{'type':'string'},'hubHeightM':fact_schema('number'),'installationProvider':{'type':['string','null']}}}},'specs':{'type':'object','additionalProperties':False,'required':list(specs),'properties':specs},'notes':{'type':'array','items':{'type':'string'}},'simulation':{'type':'object','additionalProperties':False,'required':simkeys,'properties':{**{k:{'type':'number','exclusiveMinimum':0} for k in simkeys if k!='assumptions'},'assumptions':{'type':'array','minItems':1,'items':{'type':'string'}}}},'asset':{'type':'object','additionalProperties':False,'required':['glb','lod','schematic'],'properties':{'glb':{'type':'string','pattern':'^models/[a-z0-9-]+\\.glb$'},'lod':{'type':'string','pattern':'^models/[a-z0-9-]+\\.glb$'},'schematic':{'type':'boolean'}}}}}
engineering={'type':'object','additionalProperties':False,'required':list(models[0]['engineering']),'properties':{
'reviewDate':{'type':'string'},'geometryScope':{'type':'string'},'identity':{'type':'string'},'layoutCode':{'enum':['direct','one-planetary-two-parallel','two-planetary-one-parallel']},'layout':{'type':'string'},
'pitchDrive':fact_schema('string'),'gearRatio':fact_schema('number'),'generatorVoltageV':fact_schema('number'),'generatorSpeedRPM':fact_schema('number'),'transformer':fact_schema('string'),
'references':{'type':'array','minItems':1,'items':{'type':'object','additionalProperties':False,'required':['id','title','publisher','url','pages'],'properties':{k:{'type':'string','minLength':1} for k in ['id','title','publisher','url','pages']}}}}}
schema['properties']['engineering']=engineering
landscape_strings=['id','parkName','municipality','region','biome','description','sitingNote']
schema['properties']['landscapes']={'type':'array','minItems':1,'items':{'type':'object','additionalProperties':False,'required':landscape_strings+['preset','seed','sources'],'properties':{**{key:{'type':'string','minLength':1} for key in landscape_strings},'preset':{'enum':['valley-crops','alluvial-valley','coastal-forestry','rural-mosaic','interior-hills']},'seed':{'type':'integer'},'sources':{'type':'array','minItems':1,'items':{'type':'object','additionalProperties':False,'required':['title','url','publisher'],'properties':{key:{'type':'string','minLength':1} for key in ['title','url','publisher']}}}}}}

(root/'src/data/turbine.schema.json').write_text(json.dumps(schema,ensure_ascii=False,indent=2),encoding='utf-8')
labels={'ratedPowerMW':'P nominal (MW)','rotorDiameterM':'Rotor (m)','hubHeightM':'Buje instalado (m)','bladeCount':'Palas','generator':'Generador','gearbox':'Multiplicadora','powerControl':'Control','cutInMS':'Arranque (m/s)','ratedWindMS':'Nominal (m/s)','cutOutMS':'Corte (m/s)','converter':'Convertidor'}
def val(f):
    if f['value'] is None:return 'No documentado'
    v='Sí' if f['value'] is True else 'No' if f['value'] is False else str(f['value'])
    return v+(' [familia]' if f['scope']=='family' else ' [parque]')
lines=['# Modelos y proveedores del Biobío','','Fuente base: 02_PARQUES_COMPONENTES_BIOBIO.pdf, Smartwind v1.0, corte documental 03-10-2026. Corpus activo: Goldwind 1,5 MW, Vestas 2 MW, Nordex N149, Coener/Coordinador, Flender/Winergy y documentación OEM Gamesa. Se conserva el nivel de evidencia del informe; las referencias Bxx son las de ese informe, complementadas por referencias técnicas enlazadas en cada JSON.','','El catálogo seleccionado registra cinco modelos, uno por fabricante; revisión complementaria de fuentes primarias el 24-10-2026. No es un censo actualizado ni una certificación por número de serie. Se usa el Biobío actual.','','## Fabricantes, suministro y parques','','| Fabricante / modelo | Potencia unitaria documentada | Parque(s) | Evidencia | Proveedor de instalación mencionado |','|---|---|---|---|---|']
for m in models:lines.append('| '+ ' | '.join([m['manufacturer']+' '+m['model'],val(m['specs']['ratedPowerMW']),', '.join(p['name'] for p in m['parks']),'; '.join(p['name']+': '+p['evidence']+' '+','.join(p['references']) for p in m['parks']),'; '.join(p['name']+': '+p['installationProvider'] for p in m['parks'] if p['installationProvider']) or 'No documentado'])+' |')
lines+=['','Fabricante, operador e instalador son roles distintos. «Proveedor» se entrega como fabricante identificado; el corpus no demuestra un contratista de suministro independiente para todos los parques. Tecnorenova/Greenwork/CJR son referencias de instalación, no fabricantes.','','## Datos técnicos extraídos','','Cada valor incluye su alcance. Ausencia de un dato no se reemplaza por la cifra de otra variante. Alturas de torre se conservan por parque.']
for title,keys in [('Geometría y arquitectura',['rotorDiameterM','hubHeightM','bladeCount','generator','gearbox','powerControl']),('Umbrales de operación y conversión',['cutInMS','ratedWindMS','cutOutMS','converter'])]:
    lines+=['','### '+title,'','| Modelo | '+' | '.join(labels[k] for k in keys)+' |','|'+'---|'*(len(keys)+1)]
    for m in models:lines.append('| '+m['model']+' | '+' | '.join(val(m['specs'][k]) for k in keys)+' |')
lines+=['','### Alcance de las cinco fichas','','Envision: el informe del parque incluye una tabla de diseño preliminar; el comunicado OEM anuncia buje de 100 m, no una medición as-built. Gamesa: la referencia G114-2.0 no resuelve la discrepancia de Las Peñas. Vestas: las alturas comerciales no se asignan a Los Buenos Aires. Nordex y Goldwind: se distinguen parámetros de familia de la configuración instalada.','','La documentación complementaria y los esquemas consultados se enlazan en investigacion-tecnica.md y engineering.references. No se deducen especificaciones del nombre de los modelos.','','## Trazabilidad por campo','']
for m in models:
    lines+=['### '+m['manufacturer']+' '+m['model'],'']
    for k,f in m['specs'].items():lines.append('- '+labels[k]+': '+val(f)+'. '+(f['source'] or 'Sin fuente específica')+'. '+f['note'])
    lines+=['']+['- '+n for n in m['notes']]+['','Supuestos empleados en el escenario:','']+['- '+n for n in m['simulation']['assumptions']]+['']
(doc/'modelos-extraidos.md').write_text('\n'.join(lines),encoding='utf-8')
with (doc/'modelos-extraidos.csv').open('w',newline='',encoding='utf-8-sig') as file:
    writer=csv.writer(file);writer.writerow(['Fabricante','Modelo','Parques',*labels.values(),'Fuentes/alcance por campo'])
    for m in models:writer.writerow([m['manufacturer'],m['model'],', '.join(p['name'] for p in m['parks']),*[val(m['specs'][k]) for k in labels],json.dumps(m['specs'],ensure_ascii=False)])
print('Esquema JSON, tablas Markdown y CSV generados.')


