import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,SS=420,430,2
FL=412; X0=225
LT=LS=66; LTOR,LU,LF=78,46,44
rad=math.radians
F=lambda p,s:ImageFont.truetype(p,s*SS)
FB=F("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",14)
FS=F("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",12)
def pt(o,L,a):return(o[0]+L*math.sin(rad(a)),o[1]+L*math.cos(rad(a)))
def up(o,L,a):return(o[0]+L*math.sin(rad(a)),o[1]-L*math.cos(rad(a)))
def ease(t):return t*t*(3-2*t)
S=lambda p:(p[0]*SS,p[1]*SS)
def norm(p,q):
    dx,dy=q[0]-p[0],q[1]-p[1];L=math.hypot(dx,dy) or 1;return(-dy/L,dx/L),L
def capsule(d,p,q,w1,w2,col):
    n,L=norm(p,q)
    poly=[(p[0]+n[0]*w1/2,p[1]+n[1]*w1/2),(q[0]+n[0]*w2/2,q[1]+n[1]*w2/2),(q[0]-n[0]*w2/2,q[1]-n[1]*w2/2),(p[0]-n[0]*w1/2,p[1]-n[1]*w1/2)]
    d.polygon([S(z) for z in poly],fill=col)
    for c,w in((p,w1),(q,w2)):d.ellipse([(c[0]-w/2)*SS,(c[1]-w/2)*SS,(c[0]+w/2)*SS,(c[1]+w/2)*SS],fill=col)
def blob(d,p,q,f,off,lenf,wid,inten,col):
    n,L=norm(p,q);cx=p[0]+(q[0]-p[0])*f+n[0]*off;cy=p[1]+(q[1]-p[1])*f+n[1]*off
    ux,uy=(q[0]-p[0])/L,(q[1]-p[1])/L;a,b=L*lenf/2,wid/2;pts=[]
    for i in range(28):
        t=2*math.pi*i/28;x,y=a*math.cos(t),b*math.sin(t);pts.append(S((cx+x*ux+y*n[0],cy+x*uy+y*n[1])))
    d.polygon(pts,fill=col+(int(255*max(0,min(1,inten))),))
def bg():
    im=Image.new("RGBA",(W*SS,H*SS));d=ImageDraw.Draw(im)
    for y in range(H*SS):
        t=y/(H*SS);d.line([(0,y),(W*SS,y)],fill=(int(8+10*t),int(22+14*t),int(58+22*t),255))
    d.rectangle([0,FL*SS,W*SS,H*SS],fill=(16,30,64,255));d.line([(0,FL*SS),(W*SS,FL*SS)],fill=(60,86,140,255),width=2*SS)
    return im
BASE=bg()
def mini(d,x0,y0,kind,on,name):
    sc=.62;gray=(150,156,170,255);pur=(165,90,240,255) if on else (165,90,240,0)
    def P(x,y):return((x0+x*sc)*SS,(y0+y*sc)*SS)
    def cap(a,b,w):
        (ax,ay),(bx,by)=P(*a),P(*b);d.line([(ax,ay),(bx,by)],fill=gray,width=int(w*sc*SS))
        for c in((ax,ay),(bx,by)):d.ellipse([c[0]-w*sc*SS/2,c[1]-w*sc*SS/2,c[0]+w*sc*SS/2,c[1]+w*sc*SS/2],fill=gray)
    d.ellipse([*P(40,4),*P(60,24)],fill=gray)
    d.polygon([P(28,28),P(72,28),P(66,66),P(34,66)],fill=gray)
    d.polygon([P(34,64),P(66,64),P(70,84),P(30,84)],fill=gray)
    cap((28,32),(14,64),10);cap((72,32),(86,64),10);cap((40,82),(38,118),16);cap((60,82),(62,118),16)
    hl=(165,90,240,255) if on else (200,205,215,255)
    def el(cx,cy,rx,ry):d.ellipse([*P(cx-rx,cy-ry),*P(cx+rx,cy+ry)],fill=hl)
    if kind=="Glutes":el(41,76,10,9);el(59,76,10,9)
    if kind=="Hamstrings":el(40,100,7,16);el(60,100,7,16)
    if kind=="Lower back":el(42,56,7,9);el(58,56,7,9)
    if kind=="Shoulders":el(27,34,9,9);el(73,34,9,9)
    if kind=="Triceps":el(20,48,6,13);el(80,48,6,13)
    if kind=="Biceps":el(20,46,6,11);el(80,46,6,11)
    if kind=="Lats":el(37,52,8,15);el(63,52,8,15)
    if kind=="Upper back":el(50,38,16,8)
    if kind=="Chest":el(41,42,10,8);el(59,42,10,8)
    if kind=="Forearms":el(18,56,5,9);el(82,56,5,9)
    if kind=="Quads":el(41,96,6,14);el(59,96,6,14)
    if kind=="Adductors":el(46,92,3,12);el(54,92,3,12)
    if kind=="Calves":el(39,110,6,7);el(61,110,6,7)
    if kind=="Abs":el(50,58,8,12)
    if kind=="Hip flexors":el(40,80,7,7);el(60,80,7,7)
    d.text((x0*SS+ (0),(y0+73)*SS),name,font=FS,fill=(235,240,250,255))
    if on:
        cx,cy=(x0+9)*SS,(y0+10)*SS
        d.ellipse([cx-7*SS,cy-7*SS,cx+7*SS,cy+7*SS],fill=(76,175,106,255))
        d.line([(cx-4*SS,cy),(cx-1*SS,cy+3*SS),(cx+5*SS,cy-4*SS)],fill=(255,255,255,255),width=2*SS)
