src=open('make_six.py',encoding='utf8').read()
exec(src[:src.index('# ---------- pressing')])
WH=(34,34,42,255);RIM=(220,220,225,255)
def rect(d,x0,y0,x1,y1,col=MC,r=5):d.rounded_rectangle([x0*SS,y0*SS,x1*SS,y1*SS],radius=r*SS,fill=col)
def body(d):
    # standing, front view
    for s in (-1,1):
        hip=(cx+s*20,290);knee=(cx+s*24,345);ank=(cx+s*26,FL-8)
        capsule(d,hip,knee,26,19,SK);capsule(d,knee,ank,19,13,SK)
        d.ellipse([(ank[0]-15)*SS,(ank[1]-4)*SS,(ank[0]+15)*SS,(ank[1]+10)*SS],fill=SK)
    d.polygon([S(z) for z in [(cx-52,192),(cx+52,192),(cx+32,300),(cx-32,300)]],fill=SK)
    capsule(d,(cx,190),(cx,174),16,14,SK)
    d.ellipse([(cx-17)*SS,(148-17)*SS,(cx+17)*SS,(148+17)*SS],fill=SK)
def handle(d,c,r=8):
    d.rounded_rectangle([(c[0]-r)*SS,(c[1]-5)*SS,(c[0]+r)*SS,(c[1]+5)*SS],radius=4*SS,fill=WH,outline=RIM,width=2*SS)
def ang(c,a,l):return (c[0]+l*math.sin(rad(a)),c[1]+l*math.cos(rad(a)))
def lateral(p,label):
    im,d=mkimg();body(d)
    rect(d,cx-132,300,cx-116,FL,MC,4);d.ellipse([(cx-132)*SS,(380)*SS,(cx-116)*SS,(396)*SS],fill=STEEL)
    sh=(cx+52,200);a=L(8,88,p)       # arm angle from straight down, outward
    E=ang(sh,a,40);H=ang(E,L(8,88,p)-2,38)
    # cable from low pulley (left) across the body to the working hand
    d.line([S((cx-124,388)),S(H)],fill=STEEL,width=3*SS)
    capsule(d,sh,E,17,12,SK2);capsule(d,E,H,12,10,SK2);handle(d,H,7)
    sh2=(cx-52,200);capsule(d,sh2,(cx-58,248),17,12,SK2);capsule(d,(cx-58,248),(cx-56,290),12,10,SK2)
    ov,o=newov(im);dl=L(.3,1,p)
    el(o,sh[0]+8,sh[1]+4,13,12,dl)
    return finish(im,ov,"Single-Arm Cable Lateral Raise (front view)",label,[("Shoulders",dl),("Upper back",L(.1,.4,p))])
run("cable-lateral-raise",lateral,0,1,"Hand by your side, slight bend in the elbow","Arm up to shoulder height. Squeeze the side shoulder","1. Raise the arm out to the side","2. Lower slowly, with control")

def rear(p,label):
    im,d=mkimg()
    # cable tower in front of him (behind the body in this back view)
    rect(d,cx-8,96,cx+8,FL-4,MC,4);d.ellipse([(cx-9)*SS,(92)*SS,(cx+9)*SS,(110)*SS],fill=STEEL)
    HS=[]
    for s_ in (-1,1):
        H=(cx+s_*L(26,118,p),L(222,204,p));HS.append(H)
        d.line([S((cx,104)),S(H)],fill=STEEL,width=3*SS)
    body(d)
    d.pieslice([(cx-18)*SS,(128)*SS,(cx+18)*SS,(166)*SS],180,360,fill=(60,66,84,255))  # hair: back of head
    d.line([S((cx,176)),S((cx,296))],fill=SK2,width=2*SS)                              # spine
    for s_ in (-1,1):
        d.line([S((cx+s_*14,208)),S((cx+s_*34,250))],fill=SK2,width=2*SS)               # shoulder blades
    for k,s_ in enumerate((-1,1)):
        sh=(cx+s_*52,200);H=HS[k]
        E=((sh[0]+H[0])/2+s_*L(10,0,p),(sh[1]+H[1])/2+L(22,10,p))
        capsule(d,sh,E,17,12,SK2);capsule(d,E,H,12,10,SK2);handle(d,H,5)
    ov,o=newov(im);dl=L(.3,1,p);ub=L(.3,.9,p)
    for s_ in (-1,1):el(o,cx+s_*58,204,13,12,dl);el(o,cx+s_*24,224,16,10,ub)
    return finish(im,ov,"Rear-Delt Cable Raise (back view)",label,[("Shoulders",dl),("Upper back",ub)])
run("rear-delt-raise",rear,0,1,"Handles crossed in front of you (back view)","Arms wide. Squeeze rear shoulders + upper back","1. Pull the handles out and back","2. Come back slowly, with control")

def upright(p,label):
    im,d=mkimg();body(d)
    rect(d,cx-8,380,cx+8,FL-4,MC,4);d.ellipse([(cx-9)*SS,(386)*SS,(cx+9)*SS,(402)*SS],fill=STEEL)
    for s in (-1,1):
        sh=(cx+s*52,200)
        H=(cx+s*L(14,16,p),L(296,190,p))
        E=(cx+s*L(60,90,p),L(250,214,p))
        capsule(d,sh,E,17,12,SK2);capsule(d,E,H,12,10,SK2)
    H0=(cx,L(296,190,p));d.line([S((cx,392)),S((cx,H0[1]))],fill=STEEL,width=3*SS)
    d.rounded_rectangle([(cx-26)*SS,(H0[1]-5)*SS,(cx+26)*SS,(H0[1]+5)*SS],radius=4*SS,fill=WH,outline=RIM,width=2*SS)
    ov,o=newov(im);dl=L(.3,1,p);tr=L(.2,.9,p)
    for s in (-1,1):el(o,cx+s*60,204,12,12,dl);el(o,cx+s*20,186,14,8,tr)
    return finish(im,ov,"Cable Upright Row (front view)",label,[("Shoulders",dl),("Upper back",tr)])
run("cable-upright-row",upright,0,1,"Hands low, bar close to the body","Elbows up, but below the shoulders","1. Pull up to chest height, elbows lead","2. Lower slowly, with control")
