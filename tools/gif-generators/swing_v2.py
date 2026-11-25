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
    sc=.85;gray=(150,156,170,255);pur=(165,90,240,255) if on else (165,90,240,0)
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
    d.text((x0*SS+ (0),(y0+104)*SS),name,font=FS,fill=(235,240,250,255))
    if on:
        cx,cy=(x0+10)*SS,(y0+14)*SS
        d.ellipse([cx-9*SS,cy-9*SS,cx+9*SS,cy+9*SS],fill=(76,175,106,255))
        d.line([(cx-4*SS,cy),(cx-1*SS,cy+3*SS),(cx+5*SS,cy-4*SS)],fill=(255,255,255,255),width=2*SS)
def frame(P,label):
    im=BASE.copy();d=ImageDraw.Draw(im)
    ankle=(X0,FL-6);knee=(ankle[0]+LS*math.sin(rad(P["s"])),ankle[1]-LS*math.cos(rad(P["s"])))
    hip=(knee[0]-LT*math.sin(rad(P["t"])),knee[1]-LT*math.cos(rad(P["t"])))
    sh=up(hip,LTOR,P["tt"]);head=up(sh,30,P["tt"]*.6);el=pt(sh,LU,P["a"]);wr=pt(el,LF,P["f"])
    sk=(236,240,247,255);sk2=(196,204,218,255)
    capsule(d,sh,pt(sh,LU,P["a"]-4),12,9,sk2)
    capsule(d,hip,knee,26,18,sk);capsule(d,knee,ankle,17,11,sk);capsule(d,ankle,(ankle[0]+22,ankle[1]+3),10,8,sk)
    capsule(d,hip,sh,32,38,sk);capsule(d,sh,up(sh,14,P["tt"]*.6),13,13,sk)
    d.ellipse([(head[0]-15)*SS,(head[1]-15)*SS,(head[0]+15)*SS,(head[1]+15)*SS],fill=sk)
    capsule(d,sh,el,14,10,sk);capsule(d,el,wr,10,8,sk)
    c=pt(wr,20,P["f"])
    d.ellipse([(c[0]-17)*SS,(c[1]-17)*SS,(c[0]+17)*SS,(c[1]+17)*SS],fill=(24,24,30,255),outline=(220,220,225,255),width=2*SS)
    d.arc([(c[0]-11)*SS,(c[1]-33)*SS,(c[0]+11)*SS,(c[1]-8)*SS],180,360,fill=(220,220,225,255),width=3*SS)
    GR=(70,255,110)
    ov=Image.new("RGBA",im.size,(0,0,0,0));o=ImageDraw.Draw(ov)
    blob(o,sh,hip,1.0,10,.4,28,P["g"],GR);blob(o,hip,knee,.5,9,.8,15,P["h"],GR);blob(o,hip,knee,.5,-9,.7,14,P["q"],GR)
    blob(o,hip,sh,.32,-12,.5,14,P["b"],GR);blob(o,sh,el,.18,0,.5,18,P["d"],GR);blob(o,hip,sh,.5,12,.5,14,.2+.5*P["b"],GR)
    glow=ov.filter(ImageFilter.GaussianBlur(7*SS));im=Image.alpha_composite(im,glow);im=Image.alpha_composite(im,glow)
    sharp=ov.copy();sharp.putalpha(sharp.getchannel("A").point(lambda v:int(v*.55)));im=Image.alpha_composite(im,sharp)
    d=ImageDraw.Draw(im)
    for i,(k,v) in enumerate((("Glutes",P["g"]),("Hamstrings",P["h"]),("Lower back",P["b"]),("Shoulders",P["d"]))):
        mini(d,10+i*102,8,k,v>.5,k)
    d.text((14*SS,150*SS),"Kettlebell Swing",font=FB,fill=(255,255,255,255))
    d.text((14*SS,170*SS),label,font=FS,fill=(255,170,90,255))
    return im.convert("RGB").resize((W,H),Image.LANCZOS)
def kp(**k):
    b=dict(s=3,t=3,tt=3,a=88,f=88,g=0,h=0,q=0,b=0,d=0);b.update(k);return b
top=kp(g=1,h=.7,q=.7,b=.35,d=.7);bot=kp(s=18,t=58,tt=64,a=-12,f=-12,g=.35,h=.9,q=.2,b=.8,d=.15)
def lerp(a,b,t):
    t=ease(t);return{k:a[k]+(b[k]-a[k])*t for k in a}
fr=[];dur=[];per=24
fr.append((top,"Stand tall: squeeze glutes"));dur.append(2200)
for j in range(1,per):fr.append((lerp(top,bot,j/per),"1. Hips back, back flat"));dur.append(80)
fr.append((bot,"Hamstrings + back loaded"));dur.append(2200)
for j in range(1,per):fr.append((lerp(bot,top,j/per),"2. Snap hips forward!"));dur.append(60)
imgs=[frame(P,l) for P,l in fr]
imgs[0].save("img/swing-v2.gif",save_all=True,append_images=imgs[1:],duration=dur,loop=0,optimize=False)
print(len(imgs),sum(dur))
