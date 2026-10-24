"""
Limpa a ilustração oficial "Localize-se!" e gera a base do mapa (planta-campus.webp).

O que faz, em ordem:
1. Recorta a planta do campus da imagem oficial (8000 x 5656 px) e reduz para 3 px por unidade da planta.
2. Detecta os ícones azuis (estacionamento, motos, bicicletas) e roxos (alimentação) e guarda as posições em dados/icones.json.
3. Apaga pinos vermelhos, etiquetas laranja e ícones, reconstruindo o fundo (inpainting). Preserva a pista vermelha/azul do Espaço de Convivência.
   O TELEA (borra a partir da borda) é a base. Por cima dele, onde fica melhor:
   - telhados de textura contínua: cópia de amostras do próprio telhado (exemplar.py);
   - pinos que cobriam uma borda: preenchimento guiado por estrutura (estrutura.py).
   As listas REFAZER e ESTRUTURA foram conferidas bloco a bloco; os demais ficam com o TELEA.
4. Torna transparente tudo o que fica fora da ilustração, alisando o contorno, e estende a Av. São Sebastião até a borda esquerda.
5. Salva planta-campus.webp (qualidade 80, com transparência) e duas imagens auxiliares para o script de contornos.

Coordenadas: 1 unidade da planta = 4 px da imagem oficial; a planta vai de x 760-1860 e y 160-1300.
Uso:  python3 limpar_planta.py      (roda a partir da pasta ferramentas/)
Requer: pip install opencv-python-headless numpy   (exemplar.py e estrutura.py ficam nesta mesma pasta)
Demora uns 4 minutos.
"""
import os
AQUI=os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)),'saida'),exist_ok=True)
import cv2,numpy as np
img=cv2.imread(os.path.join(AQUI,'fontes','mapa-localize-se.jpg'))
X0,Y0,X1,Y1=760,160,1860,1300;PPU=3;S=PPU/4
c=cv2.resize(img[Y0*4:Y1*4,X0*4:X1*4],None,fx=S,fy=S,interpolation=cv2.INTER_AREA)
raw=c.copy()
u=lambda v:int(round(v*PPU));k=lambda n:max(3,int(n*PPU/2)|1)
P=lambda x,y:(u(x-X0),u(y-Y0))
hsv=cv2.cvtColor(c,cv2.COLOR_BGR2HSV);H,Sa,V=hsv[...,0],hsv[...,1],hsv[...,2]
m=(((H<=8)|(H>=170))&(Sa>165)&(V>120)|(H>=9)&(H<=24)&(Sa>165)&(V>170)).astype(np.uint8)*255
m[u(335-Y0):u(575-Y0),u(1478-X0):u(1504-X0)]=0
m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k(25),k(25))))
cnts,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);mm=np.zeros_like(m)
for q in cnts:
  if cv2.contourArea(q)>120*(PPU/2)**2:cv2.drawContours(mm,[q],-1,255,-1)
mm=cv2.dilate(mm,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k(9),k(9))))
def blank(x0,y0,x1,y1):cv2.rectangle(c,P(x0,y0),P(x1,y1),(255,255,255),-1);cv2.rectangle(mm,P(x0,y0),P(x1,y1),0,-1)
blank(760,160,1020,262);blank(760,262,960,450);blank(760,485,1078,660);blank(760,450,1040,485);blank(760,1100,960,1300)
# ---- ícones (estacionamento/motos/bicicletas em azul, alimentação em roxo) ----
import json
hsv=cv2.cvtColor(raw,cv2.COLOR_BGR2HSV);H,Sa,V=hsv[...,0],hsv[...,1],hsv[...,2]
blue=((H>=95)&(H<=115)&(Sa>120)&(V>120)).astype(np.uint8)
purp=((H>=140)&(H<=172)&(Sa>60)&(V>90)).astype(np.uint8)
for q in (blue,purp):
  q[u(335-Y0):u(575-Y0),u(1474-X0):u(1508-X0)]=0
ICONS=[];im2=np.zeros(c.shape[:2],np.uint8)
KNOWN={'moto':[(1163,276),(1572,948)],'bike':[(1416,1026)]}
for kind,q in (('blue',blue),('food',purp)):
  q=cv2.morphologyEx(q,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k(9),k(9))))
  n,lab,st,cen=cv2.connectedComponentsWithStats(q)
  for i in range(1,n):
    x,y,w,h,a_=st[i]
    if a_<(8*PPU)**2 or w>50*PPU or h>50*PPU or X0+x/PPU<900:continue
    blob=(lab==i).astype(np.uint8);cnts,_=cv2.findContours(blob,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(im2,cnts,-1,255,-1)
    cx,cy=X0+cen[i][0]/PPU,Y0+(y+h)/PPU  # ponta inferior = ponto de referência
    t='food' if kind=='food' else 'park'
    if kind=='blue':
      for kk,pts in KNOWN.items():
        if any(abs(px-X0-cen[i][0]/PPU)<15 and abs(py-Y0-cen[i][1]/PPU)<15 for px,py in pts):t=kk
    ICONS.append([t,round(cx,1),round(cy,1),round(w/PPU,1),round(h/PPU,1)])
im2=cv2.dilate(im2,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k(7),k(7))))
mm=cv2.bitwise_or(mm,im2)
c=cv2.inpaint(c,mm,int(9*PPU/2),cv2.INPAINT_TELEA)
# ---- telhados: troca o borrão do TELEA por cópia de amostras reais (exemplares) ----
# O TELEA espalha a cor da borda e deixa uma "mancha" com o formato do pino antigo.
# Nos telhados de textura contínua, copiar pedaços do próprio telhado na vertical
# (mesmas colunas) recompõe telhas e cumeeira. Onde o pino antigo invadia grama,
# árvore ou outro telhado, a cópia cria defeitos, então lá o TELEA continua.
import sys;sys.path.insert(0,AQUI);from exemplar import _fill_region
# posição dos pinos lida do próprio site (constante PIN do index.html), para não divergir
import re as _re
_html=open(os.path.join(AQUI,'..','index.html'),encoding='utf8').read()
_pins={int(k):(int(x),int(y)) for k,x,y in _re.findall(r'(\d+):\[(\d+),(\d+)\]',_re.search(r'const PIN=\{[^}]*\}',_html).group(0))}
REFAZER=[2,3,4,6,8,9,10,11,12,13,16,17,26]  # telhados de textura contínua (conferidos um a um)
PIN={b:_pins[b] for b in REFAZER}
DIVISA={12:2310,13:2310}  # linha (px) da borda do Auditório Central: preenche cada lado só com o próprio lado
ncomp,lab=cv2.connectedComponents(mm)
for b,(x,y) in PIN.items():
  i=lab[min(u(y-Y0)-u(15),lab.shape[0]-1),u(x-X0)]
  if i==0:print('pino',b,'sem região apagada');continue
  ys,xs=np.nonzero(lab==i);M=150
  y0,y1=max(ys.min()-M,0),min(ys.max()+M,c.shape[0]);x0,x1=max(xs.min()-M,0),min(xs.max()+M,c.shape[1])
  comp=(lab[y0:y1,x0:x1]==i);other=(lab[y0:y1,x0:x1]>0)&~comp
  rows=np.arange(y0,y1)[:,None]*np.ones((1,x1-x0),bool)
  partes=[comp] if b not in DIVISA else [comp&(rows<DIVISA[b]),comp&(rows>=DIVISA[b])]
  sub=c[y0:y1,x0:x1].copy()
  for j,p in enumerate(partes):
    proib=other.copy()
    if b in DIVISA:proib|=(rows>=DIVISA[b]) if j==0 else (rows<DIVISA[b])
    sub=_fill_region(sub,(p*255).astype(np.uint8),15,150,proib,'vertical')
  c[y0:y1,x0:x1][comp]=sub[comp]
  print('pino',b,'refeito')
# ---- pinos que cobriam uma borda: preenchimento guiado por estrutura ----
from estrutura import preencher
ESTRUTURA=[1,5,15,19,20,23,25]  # conferidos um a um; 7, 14, 18, 21, 22 e 24 pioravam e ficam com o TELEA
for b in ESTRUTURA:
  x,y=_pins[b];i=lab[min(u(y-Y0)-u(15),lab.shape[0]-1),u(x-X0)]
  if i==0:print('pino',b,'sem região apagada');continue
  ys,xs=np.nonzero(lab==i);M=150
  y0,y1=max(ys.min()-M,0),min(ys.max()+M,c.shape[0]);x0,x1=max(xs.min()-M,0),min(xs.max()+M,c.shape[1])
  hole=lab[y0:y1,x0:x1]==i;outros=(lab[y0:y1,x0:x1]>0)&~hole
  sub,_m=preencher(c[y0:y1,x0:x1].copy(),hole,outros)
  c[y0:y1,x0:x1][hole]=sub[hole];print('pino',b,'estrutura')

json.dump([[t,float(x),float(y),float(w),float(h)] for t,x,y,w,h in ICONS],open(os.path.join(AQUI,'dados','icones.json'),'w'));print('ícones encontrados:',len(ICONS))
# fora da ilustração = brancos ligados à borda
white=np.all(c>232,axis=2).astype(np.uint8);n,lab=cv2.connectedComponents(white,connectivity=4)
border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
out=np.isin(lab,list(border)).astype(np.uint8)
out=cv2.dilate(out,np.ones((k(5),k(5)),np.uint8))&(np.mean(c,axis=2)>200).astype(np.uint8)|np.isin(lab,list(border)).astype(np.uint8)
# alisa "um tiquinho": tira pontas finas e fecha dentes pequenos do contorno
inside=(1-out).astype(np.uint8)*255
inside=cv2.morphologyEx(inside,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k(14),k(14))))
inside=cv2.morphologyEx(inside,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k(14),k(14))))
# a avenida até a borda esquerda continua opaca
a,b=P(1300,1235);d,e=P(1400,1260);asph=np.median(c[b:e,a:d].reshape(-1,3),0).astype(int)
colx=P(1400,0)[0];rows=[y for y in range(P(0,1150)[1],c.shape[0]) if np.abs(c[y,colx].astype(int)-asph).sum()<45]
y0,y1=min(rows),max(rows);seg=c[y0:y1+1,:P(1100,0)[0]];seg[np.abs(seg.astype(int)-asph).sum(axis=2)>45]=asph
inside[y0:y1+1,:P(1100,0)[0]]=255
# pixels de borda: troca o branco por grama para não ficar halo claro
grass=np.array([39,137,105]);edge=cv2.dilate((inside==0).astype(np.uint8),np.ones((k(5),k(5)),np.uint8)).astype(bool)&(inside>0)&(np.mean(c,axis=2)>215)
c[edge]=grass
cv2.imwrite(os.path.join(AQUI,'dados','planta-limpa.png'),c);cv2.imwrite(os.path.join(AQUI,'dados','planta-mascara.png'),inside)
alpha=cv2.GaussianBlur(inside,(k(3),k(3)),0)
rgba=np.dstack([c,alpha])
ok,buf=cv2.imencode('.webp',rgba,[cv2.IMWRITE_WEBP_QUALITY,80]);open(os.path.join(AQUI,'saida','planta-campus.webp'),'wb').write(buf.tobytes());print(rgba.shape,len(buf)//1024,'KB')
