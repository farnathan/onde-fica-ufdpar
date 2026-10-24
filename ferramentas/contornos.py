"""
Recorta o contorno real do telhado dos prédios de telhado branco (e da Escola de Aplicação, de telha)
e grava dados/contornos.json, que vira a constante OUTLINE do index.html.

Precisa de dados/planta-limpa.png, gerado por limpar_planta.py.
Os Blocos 2 a 17 (miolo cinza, prédios em "H" interligados) e o Bloco 18 ficam com retângulo:
nesses casos a cor do telhado é igual à dos pátios e o recorte automático não é confiável.
Uso: python3 contornos.py
"""
import os,json,cv2,numpy as np
AQUI=os.path.dirname(os.path.abspath(__file__))
c=cv2.imread(os.path.join(AQUI,'dados','planta-limpa.png'))
hsv=cv2.cvtColor(c,cv2.COLOR_BGR2HSV);H,S,V=[hsv[...,i].astype(int) for i in range(3)]
white=((S<16)&(V>212)).astype(np.uint8)                       # telhado branco/claro
tile=((((H<=16)|(H>=168))&(S>=50)&(V>=110))).astype(np.uint8)  # telha da Escola de Aplicação
X0,Y0,PPU=760,160,3
# retângulos aproximados atuais (unidades da planta) usados como "semente" de cada prédio
R={"1":[1451,1120,166,65],"14":[1182,845,165,84],"19":[1185,569,267,69],"20":[1185,488,267,69],
   "21":[1185,394,274,71],"22":[1191,346,270,36],"23":[1185,272,278,58],"24":[1492,272,84,52],
   "RU":[1482,585,165,87],"BC":[1341,773,125,84],"EA":[844,701,197,32]}
out={}
for k_,(x,y,w,h) in R.items():
  m=tile if k_=="EA" else white
  pad=60 if k_=="EA" else 14
  ax,ay=int((x-pad-X0)*PPU),int((y-pad-Y0)*PPU);bx,by=int((x+w+pad-X0)*PPU),int((y+h+pad-Y0)*PPU)
  sub=m[ay:by,ax:bx].copy()*255
  sub=cv2.morphologyEx(sub,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_RECT,(9,9)))
  sub=cv2.morphologyEx(sub,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)))
  n,lab,st,cen=cv2.connectedComponentsWithStats(sub)
  rx0=ry0=int(pad*PPU);rx1,ry1=rx0+int(w*PPU),ry0+int(h*PPU)
  best=max(((lab[ry0:ry1,rx0:rx1]==i).sum(),i) for i in range(1,n))
  if best[0]<0.3*w*h*PPU*PPU:print(k_,'sem contorno confiável');continue
  comp=(lab==best[1]).astype(np.uint8)*255
  if k_=="EA":comp=cv2.morphologyEx(comp,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_RECT,(31,31)))
  cnt=max(cv2.findContours(comp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0],key=cv2.contourArea)
  ap=cv2.approxPolyDP(cnt,2.2*PPU/(1 if k_!="EA" else 0.6),True)[:,0,:]
  a=np.array([[X0+(ax+px)/PPU,Y0+(ay+py)/PPU] for px,py in ap],np.float32)
  if k_!="EA":   # contorno externo: fecha os "dentes" deixados pela limpeza dos pinos
    a=cv2.approxPolyDP(cv2.convexHull(a)[:,0,:],1.2,True)[:,0,:]
  out[k_]=[[round(float(px),1),round(float(py),1)] for px,py in a]
  print(f'{k_:3s} {len(out[k_])} pontos')
json.dump(out,open(os.path.join(AQUI,'dados','contornos.json'),'w'),separators=(',',':'))
