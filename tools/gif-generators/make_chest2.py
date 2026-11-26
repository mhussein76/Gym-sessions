src=open('make_six.py',encoding='utf8').read()
exec(src[:src.index('# ---------- back exercises')])
exec(open('make_shoulder.py',encoding='utf8').read().split("def lateral")[0].split("exec(src")[1].split("\n",1)[1]) if False else None
WH=(34,34,42,255);RIM=(220,220,225,255)
def rect(d,x0,y0,x1,y1,col=MC,r=5):d.rounded_rectangle([x0*SS,y0*SS,x1*SS,y1*SS],radius=r*SS,fill=col)
def body(d):
    for s in (-1,1):
        hip=(cx+s*20,290);knee=(cx+s*24,345);ank=(cx+s*26,FL-8)
        capsule(d,hip,knee,26,19,SK);capsule(d,knee,ank,19,13,SK)
        d.ellipse([(ank[0]-15)*SS,(ank[1]-4)*SS,(ank[0]+15)*SS,(ank[1]+10)*SS],fill=SK)
    d.polygon([S(z) for z in [(cx-52,192),(cx+52,192),(cx+32,300),(cx-32,300)]],fill=SK)
    capsule(d,(cx,190),(cx,174),16,14,SK);d.ellipse([(cx-17)*SS,(148-17)*SS,(cx+17)*SS,(148+17)*SS],fill=SK)
run("flat-db-press",press("Flat Dumbbell Chest Press",True,False),0,1,"Dumbbells at chest sides, elbows about 45°","Arms straight, chest squeezed","1. Press up and slightly in","2. Lower slowly, with control")
def fly(p,label):
    im,d=mkimg()
    for s in (-1,1):rect(d,cx+s*140-6,96,cx+s*140+6,FL-4,MC,4)
    HS=[]
    for s in (-1,1):
        H=(cx+s*L(112,14,p),L(172,262,p));HS.append(H)
        d.line([S((cx+s*140,104)),S(H)],fill=STEEL,width=3*SS)
    body(d)
    for k,s in enumerate((-1,1)):
        sh=(cx+s*52,200);H=HS[k]
        E=((sh[0]+H[0])/2+s*L(8,18,p),(sh[1]+H[1])/2+L(-4,6,p))
        capsule(d,sh,E,17,12,SK2);capsule(d,E,H,12,10,SK2)
        d.rounded_rectangle([(H[0]-6)*SS,(H[1]-5)*SS,(H[0]+6)*SS,(H[1]+5)*SS],radius=4*SS,fill=WH,outline=RIM,width=2*SS)
    ov,o=newov(im);ci=L(.35,1,p)
    for s in (-1,1):el(o,cx+s*24,244,22,13,ci);el(o,cx+s*52,206,11,11,L(.2,.5,p))
    return finish(im,ov,"High-to-Low Cable Fly (front view)",label,[("Chest",ci),("Shoulders",L(.2,.5,p))])
run("cable-fly-high-low",fly,0,1,"Cables high, arms wide, slight bend","Hands meet low in front. Squeeze the lower chest","1. Sweep the hands down and in","2. Back up slowly, with control")
