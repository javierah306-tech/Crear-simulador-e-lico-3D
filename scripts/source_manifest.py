from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
source=Path(r'C:\Users\javie\OneDrive\Desktop\Lab Neiron\modelos 3D eolicos\modelos chilenos')
items=[]
for p in sorted(source.rglob('*')):
    if p.suffix not in ['.pdf','.html']:continue
    items.append({'file':p.name,'original':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'used':p.suffix=='.pdf' or p.name=='nordex_n149.html'})
(root/'docs/fuentes.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# Fuentes y trazabilidad','','El usuario adjuntó el boceto visual. El informe y los documentos de fabricantes se localizaron por nombre en la carpeta vecina `modelos 3D eolicos/modelos chilenos`. Se le informó al usuario de ese hallazgo antes de usar el corpus. No se usaron documentos de otros proyectos ni se ejecutaron instrucciones contenidas en las fuentes.','','| Archivo | Lectura empleada | SHA-256 |','|---|---|---|']
for i in items:lines.append('| '+i['file']+' | '+('Sí' if i['used'] else 'No, detectado pero no usado para completar especificaciones')+' | `'+i['sha256']+'` |')
lines+=['','Las rutas originales están en `fuentes.json`. Los documentos completos conservan sus derechos; no se empaquetan como assets del sitio. Las extracciones locales intermedias están ignoradas por Git.','','Páginas clave contrastadas visualmente: informe p. 4-5 (catálogo/discrepancias), Goldwind p. PDF 6 (tabla GW87), Vestas 2 MW p. PDF 6 (V110), Vestas 4 MW p. PDF 9 (V150) y V112 LCA p. PDF 72 / impresa 63 (componentes). El informe completo fue extraído como texto para consultar su alcance y referencias.','','Documentación primaria del stack consultada para compatibilidad: [instalación de React Three Fiber](https://r3f.docs.pmnd.rs/getting-started/installation) y [guía de Vite](https://vite.dev/guide/). React 19 se utiliza con Fiber 9. El lockfile fija las versiones resueltas durante la construcción.','','Las referencias B01-B27 son las del informe y no significan que se haya descargado o actualizado cada fuente original. El alcance temporal sigue siendo el corte documental del informe.']
(root/'docs/fuentes.md').write_text('\n'.join(lines),encoding='utf-8')
