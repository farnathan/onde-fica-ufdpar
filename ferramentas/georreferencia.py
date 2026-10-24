"""
Calcula a transformação entre as coordenadas da planta e coordenadas reais (GPS),
usando os contornos dos prédios no OpenStreetMap (fontes/campus-openstreetmap.osm).

Resultado: dados/georef.json = matriz M (3x2) que leva (x, y, 1) da planta a metros (leste, sul)
a partir do canto noroeste do terreno da UFDPar no OSM (lat -2.9068351, lon -41.755203).
No index.html isso é a constante GEO. Erro médio obtido: 3,4 m (máximo 7,2 m); escala 0,293 m por unidade; rotação ~1°.

Pares usados (retângulo na planta -> caixa do prédio no OSM, em metros):
Blocos 23, 22, 21, 24, o conjunto 25+Quadra+26, RU e Bloco 1.
Os Blocos 2 a 9 e a Escola de Aplicação não existem no OSM (outubro/2026); cadastrá-los melhora a precisão.
Uso: python3 georreferencia.py
"""
import os,json,math,xml.etree.ElementTree as ET,numpy as np
AQUI=os.path.dirname(os.path.abspath(__file__))
r=ET.parse(os.path.join(AQUI,'fontes','campus-openstreetmap.osm')).getroot()
N={n.get('id'):(float(n.get('lat')),float(n.get('lon'))) for n in r.iter('node')}
lat0,lon0=-2.9068351,-41.755203;k=math.cos(math.radians(lat0))
m=lambda ll:((ll[1]-lon0)*k*111320,(lat0-ll[0])*111320)
def caixa(way_id):
  w=[e for e in r.findall('way') if e.get('id')==way_id][0]
  p=[m(N[n.get('ref')]) for n in w.findall('nd')];xs=[a for a,b in p];ys=[b for a,b in p]
  return min(xs),max(xs),min(ys),max(ys)
pares=[([1185,272,278,58],'766653082'),   # Bloco 23
       ([1191,346,270,36],'766653081'),   # Bloco 22
       ([1185,394,274,71],'766653077'),   # Bloco 21
       ([1492,272,84,52],'766653076'),    # Bloco 24
       ([1501,351,109,223],'766653100'),  # 25 + Quadra + 26
       ([1482,585,165,87],'766653101'),   # RU
       ([1451,1120,166,65],'766653097')]  # Bloco 1
A=[];Bm=[]
for (x,y,w,h),wid in pares:
  mx0,mx1,my0,my1=caixa(wid)
  for px,mx in((x,mx0),(x+w,mx1)):
    for py,my in((y,my0),(y+h,my1)):A.append([px,py,1]);Bm.append([mx,my])
A=np.array(A,float);Bm=np.array(Bm,float)
M=np.linalg.lstsq(A,Bm,rcond=None)[0]
err=np.sqrt(((A@M-Bm)**2).sum(1))
print('erro médio %.1f m, máximo %.1f m'%(err.mean(),err.max()))
json.dump({'M':M.round(6).tolist(),'lat0':lat0,'lon0':lon0},open(os.path.join(AQUI,'dados','georef.json'),'w'))
