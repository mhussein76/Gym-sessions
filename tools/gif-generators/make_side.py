src=open('make_six.py',encoding='utf8').read()
exec(src[:src.index('# ---------- pressing')])
def rect(d,x0,y0,x1,y1,col=MC,r=5):d.rounded_rectangle([x0*SS,y0*SS,x1*SS,y1*SS],radius=r*SS,fill=col)
def plate(d,c,r=24):
    d.ellipse([(c[0]-r)*SS,(c[1]-r)*SS,(c[0]+r)*SS,(c[1]+r)*SS],fill=(34,34,42,255),outline=(220,220,225,255),width=2*SS)
    d.ellipse([(c[0]-5)*SS,(c[1]-5)*SS,(c[0]+5)*SS,(c[1]+5)*SS],fill=(190,190,195,255))
def foot(d,a):d.ellipse([(a[0]-6)*SS,(a[1]-5)*SS,(a[0]+22)*SS,(a[1]+9)*SS],fill=SK)

# ---- Bench press, side view (head left, feet right) ----
def bench(p,label):
    im,d=mkimg()
    rect(d,cx-120,382,cx+62,394);rect(d,cx-104,394,cx-94,FL);rect(d,cx+40,394,cx+50,FL)
    rect(d,cx-50,292,cx-44,394,(80,92,115,255),2);rect(d,cx-50,292,cx-30,298,(80,92,115,255),2)
    hip=(cx,372);knee=(cx+55,342);ank=(cx+62,FL-8)
    capsule(d,hip,knee,28,19,SK);capsule(d,knee,ank,19,13,SK);foot(d,ank)
    capsule(d,(cx-76,368),hip,34,30,SK);capsule(d,(cx-96,366),(cx-84,367),14,14,SK)
    d.ellipse([(cx-132)*SS,(350)*SS,(cx-100)*SS,(382)*SS],fill=SK)
    S0=(cx-70,362);E=(cx+L(-90,-66,p),L(384,324,p));H=(cx+L(-52,-60,p),L(348,276,p))
    plate(d,H)
    capsule(d,S0,E,17,12,SK2);capsule(d,E,H,12,10,SK2)
    ov,o=newov(im);ci=L(.55,1,p)
    el(o,cx-50,358,24,12,ci);el(o,cx-68,356,11,11,L(.3,.6,p));el(o,(S0[0]+E[0])/2,(S0[1]+E[1])/2,8,15,L(.3,.7,p),rot=0)
    return finish(im,ov,"Barbell Bench Press (side view)",label,[("Chest",ci),("Shoulders",L(.3,.6,p)),("Triceps",L(.3,.7,p))])
run("bench-press",bench,0,1,"Bar touches the chest. Elbows about 45°","Arms straight, chest squeezed","1. Press the bar up with force","2. Lower slowly to the chest")

# ---- Incline dumbbell press, side view ----
def incl(p,label):
    im,d=mkimg()
    hip=(cx+10,372);sh=(cx-45,320);head=(cx-68,296)
    rect(d,cx-20,382,cx+50,394);rect(d,cx+10,394,cx+20,FL)
    capsule(d,(cx-52,326),(cx+4,378),22,22,MC)   # backrest
    knee=(cx+68,352);ank=(cx+76,FL-8)
    capsule(d,hip,knee,28,19,SK);capsule(d,knee,ank,19,13,SK);foot(d,ank)
    capsule(d,hip,sh,34,36,SK);d.ellipse([(head[0]-16)*SS,(head[1]-16)*SS,(head[0]+16)*SS,(head[1]+16)*SS],fill=SK)
    E=(cx+L(-72,-34,p),L(342,290,p));H=(cx+L(-34,-28,p),L(300,238,p))
    capsule(d,sh,E,17,12,SK2);capsule(d,E,H,12,10,SK2)
    d.rounded_rectangle([(H[0]-4)*SS,(H[1]-22)*SS,(H[0]+4)*SS,(H[1]+22)*SS],radius=3*SS,fill=(34,34,42,255),outline=(220,220,225,255),width=2*SS)
    ov,o=newov(im);ci=L(.55,1,p)
    el(o,cx-30,330,22,12,ci,rot=45);el(o,sh[0]-2,sh[1]-2,11,11,L(.3,.6,p));el(o,(sh[0]+E[0])/2,(sh[1]+E[1])/2,8,15,L(.3,.7,p))
    return finish(im,ov,"Incline Dumbbell Press (side view)",label,[("Chest",ci),("Shoulders",L(.3,.6,p)),("Triceps",L(.3,.7,p))])
run("incline-press",incl,0,1,"Dumbbells at the sides of the chest","Dumbbells above the upper chest","1. Press up and slightly in","2. Lower slowly, with control")

# ---- Seated cable row, side view ----
def crow(p,label):
    im,d=mkimg()
    rect(d,cx-30,382,cx+40,394);rect(d,cx-10,394,cx,FL)
    rect(d,cx+150,330,cx+160,FL,(80,92,115,255),2)   # foot plate / machine
    hip=(cx,372);knee=(cx+66,360);ank=(cx+132,368)
    capsule(d,hip,knee,28,19,SK);capsule(d,knee,ank,19,13,SK);foot(d,ank)
    tt=L(24,-6,p);sh=up(hip,78,tt);head=up(sh,32,tt*.6)
    capsule(d,hip,sh,34,36,SK);d.ellipse([(head[0]-16)*SS,(head[1]-16)*SS,(head[0]+16)*SS,(head[1]+16)*SS],fill=SK)
    a=L(78,-38,p);f=L(88,86,p)
    E=pt(sh,44,a);Hh=pt(E,42,f)
    d.line([S(Hh),S((cx+158,Hh[1]+4))],fill=STEEL,width=3*SS)
    capsule(d,sh,E,17,12,SK2);capsule(d,E,Hh,12,10,SK2)
    d.rounded_rectangle([(Hh[0]-4)*SS,(Hh[1]-10)*SS,(Hh[0]+4)*SS,(Hh[1]+10)*SS],radius=3*SS,fill=(34,34,42,255),outline=(220,220,225,255),width=2*SS)
    ov,o=newov(im);li=L(.45,1,p)
    mid=((hip[0]+sh[0])/2,(hip[1]+sh[1])/2)
    el(o,mid[0]-12-tt*.2,mid[1]+4,12,34,li,rot=-tt);el(o,sh[0]-10,sh[1]+8,12,16,L(.35,1,p),rot=-tt);el(o,(sh[0]+E[0])/2,(sh[1]+E[1])/2,7,14,L(.3,.6,p))
    return finish(im,ov,"Seated Cable Row (side view)",label,[("Lats",li),("Upper back",L(.35,1,p)),("Biceps",L(.3,.6,p))])
run("cable-row",crow,0,1,"Arms forward, back a little rounded","Elbows back, shoulder blades together","1. Pull the elbows back, chest up","2. Return slowly, arms forward")

# ---- Single dumbbell row, side view ----
def drow(p,label):
    im,d=mkimg()
    rect(d,cx+14,352,cx+130,364);rect(d,cx+24,364,cx+34,FL);rect(d,cx+110,364,cx+120,FL)
    hip=(cx-62,330);sh=up(hip,78,74);head=up(sh,32,60)
    knee=(cx-54,368);ank=(cx-58,FL-8)
    capsule(d,hip,knee,28,19,SK);capsule(d,knee,ank,19,13,SK);foot(d,ank)
    capsule(d,hip,sh,34,36,SK);d.ellipse([(head[0]-16)*SS,(head[1]-16)*SS,(head[0]+16)*SS,(head[1]+16)*SS],fill=SK)
    capsule(d,(sh[0]+4,sh[1]+6),(cx+30,352),15,12,SK2)   # supporting arm
    E=(sh[0]+L(8,-34,p),L(sh[1]+40,sh[1]-2,p));H=(sh[0]+L(12,-14,p),L(sh[1]+84,sh[1]+30,p))
    capsule(d,sh,E,17,12,SK2);capsule(d,E,H,12,10,SK2)
    d.rounded_rectangle([(H[0]-4)*SS,(H[1]-22)*SS,(H[0]+4)*SS,(H[1]+22)*SS],radius=3*SS,fill=(34,34,42,255),outline=(220,220,225,255),width=2*SS)
    plate(d,(H[0],H[1]),r=13)
    ov,o=newov(im);li=L(.45,1,p)
    mid=((hip[0]+sh[0])/2,(hip[1]+sh[1])/2)
    el(o,mid[0],mid[1]-9,32,12,li,rot=-17);el(o,sh[0]-6,sh[1]-4,14,10,L(.3,.8,p),rot=-17);el(o,(sh[0]+E[0])/2,(sh[1]+E[1])/2,7,14,L(.3,.6,p))
    return finish(im,ov,"Single Dumbbell Row (side view)",label,[("Lats",li),("Upper back",L(.3,.8,p)),("Biceps",L(.3,.6,p))])
run("db-row",drow,0,1,"Arm straight: lats stretched","Elbow high, squeeze the back","1. Pull the dumbbell to your waist","2. Lower slowly")
