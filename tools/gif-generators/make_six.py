import math
from gif_lib import *
from PIL import Image, ImageDraw, ImageFilter
SK=(236,240,247,255);SK2=(205,212,225,255);GR=(70,255,110);MC=(60,70,90,255);STEEL=(170,180,196,255)
cx=262
def L(a,b,t):return a+(b-a)*t
def mkimg():
    im=BASE.copy();return im,ImageDraw.Draw(im)
def newov(im):
    ov=Image.new("RGBA",im.size,(0,0,0,0));return ov,ImageDraw.Draw(ov)
def el(o,x,y,rx,ry,i,rot=0):
    pts=[]
    for k in range(32):
        t=2*math.pi*k/32;px,py=rx*math.cos(t),ry*math.sin(t)
        pts.append(S((x+px*math.cos(rad(rot))-py*math.sin(rad(rot)),y+px*math.sin(rad(rot))+py*math.cos(rad(rot)))))
    o.polygon(pts,fill=GR+(int(255*max(0,min(1,i))),))
def finish(im,ov,title,label,thumbs):
    glow=ov.filter(ImageFilter.GaussianBlur(7*SS));im=Image.alpha_composite(im,glow);im=Image.alpha_composite(im,glow)
    sh=ov.copy();sh.putalpha(sh.getchannel("A").point(lambda v:int(v*.55)));im=Image.alpha_composite(im,sh)
    d=ImageDraw.Draw(im)
    for i,(k,v) in enumerate(thumbs):mini(d,10+i*80,4,k,v>.5,k)
    d.text((14*SS,96*SS),title,font=FB,fill=(255,255,255,255))
    d.text((14*SS,114*SS),label,font=FS,fill=(255,170,90,255))
    return im.convert("RGB").resize((W,H),Image.LANCZOS)
def run(name,fn,A,B,labA,labB,labAB,labBA,per=24):
    fr=[(0,labA,2200)]+[(j/per,labAB,80) for j in range(1,per)]+[(1,labB,2200)]+[(1-j/per,labBA,70) for j in range(1,per)]
    imgs=[fn(ease(p),l) for p,l,_ in fr];dur=[d for _,_,d in fr]
    imgs[0].save(f"img/{name}.gif",save_all=True,append_images=imgs[1:],duration=dur,loop=0,optimize=False)
    n=len(imgs);sh=Image.new("RGB",(W*3,H))
    for k,i in enumerate((0,n//4,n//2)):sh.paste(imgs[i],(k*W,0))
    sh.save(f"/tmp/{name}.png");print(name,n)
def head_seated(d,x,y):
    capsule(d,(x,y+28),(x,y+44),16,14,SK);d.ellipse([(x-17)*SS,(y-17+16)*SS,(x+17)*SS,(y+17+16)*SS],fill=SK)
def seat_legs(d):
    d.rounded_rectangle([((cx-52)*SS),(205*SS),((cx+52)*SS),(345*SS)],radius=10*SS,fill=MC)
    d.rounded_rectangle([((cx-70)*SS),(338*SS),((cx+70)*SS),(356*SS)],radius=8*SS,fill=MC)
    d.rectangle([((cx-8)*SS),(356*SS),((cx+8)*SS),(FL*SS)],fill=MC)
    for s in (-1,1):
        hip=(cx+s*20,338);knee=(cx+s*58,372);ank=(cx+s*62,FL-8)
        capsule(d,hip,knee,28,22,SK);capsule(d,knee,ank,20,13,SK)
        d.ellipse([(ank[0]-14)*SS,(ank[1]-4)*SS,(ank[0]+14)*SS,(ank[1]+10)*SS],fill=SK)

# ---------- pressing, seen from the front (lying) ----------
def press(title,db,incline):
    def fn(p,label):
        im,d=mkimg()
        by=250 if not incline else 240
        d.rounded_rectangle([((cx-58)*SS),((by-8)*SS),((cx+58)*SS),((by+112)*SS)],radius=10*SS,fill=MC)
        d.rectangle([((cx-34)*SS),((by+112)*SS),((cx+34)*SS),((by+128)*SS)],fill=MC)
        for s in (-1,1):
            hip=(cx+s*24,by+100);knee=(cx+s*52,by+128);ank=(cx+s*60,FL-8)
            capsule(d,hip,knee,26,20,SK);capsule(d,knee,ank,18,12,SK)
            d.ellipse([(ank[0]-15)*SS,(ank[1]-4)*SS,(ank[0]+15)*SS,(ank[1]+10)*SS],fill=SK)
        d.polygon([S(z) for z in [(cx-50,by+2),(cx+50,by+2),(cx+30,by+100),(cx-30,by+100)]],fill=SK)
        d.ellipse([(cx-16)*SS,(by-34)*SS,(cx+16)*SS,(by-2)*SS],fill=SK)
        for s in (-1,1):
            sh=(cx+s*50,by+6)
            hand=(cx+s*L(70 if not db else 52,66 if not db else 46,p),L(by+10,by-90,p))
            elb=(cx+s*L(86,60,p),L(by+52,by-38,p))
            capsule(d,sh,elb,18,13,SK2);capsule(d,elb,hand,13,11,SK2)
            if db:
                d.rounded_rectangle([(hand[0]-22)*SS,(hand[1]-6)*SS,(hand[0]+22)*SS,(hand[1]+6)*SS],radius=4*SS,fill=(40,40,48,255),outline=(220,220,225,255),width=2*SS)
                for q in (-1,1):d.rounded_rectangle([(hand[0]+q*20-6)*SS,(hand[1]-16)*SS,(hand[0]+q*20+6)*SS,(hand[1]+16)*SS],radius=3*SS,fill=(40,40,48,255),outline=(220,220,225,255),width=2*SS)
        if not db:
            hy=L(by+10,by-90,p);d.line([S((cx-118,hy)),S((cx+118,hy))],fill=STEEL,width=5*SS)
            for s in (-1,1):d.rounded_rectangle([(cx+s*108-6)*SS,(hy-34)*SS,(cx+s*108+6)*SS,(hy+34)*SS],radius=3*SS,fill=(40,40,48,255),outline=(220,220,225,255),width=2*SS)
        ov,o=newov(im)
        ci=L(.55,1,p)
        for s in (-1,1):
            el(o,cx+s*24,by+(18 if not incline else 12),26,16,ci);el(o,cx+s*52,by+8,11,11,L(.3,.6,p))
            el(o,(cx+s*L(86,60,p)+cx+s*50)/2,(by+6+L(by+52,by-38,p))/2,8,14,L(.25,.7,p),rot=0)
        return finish(im,ov,title,label,[("Upper chest" if False else "Chest",ci),("Shoulders",L(.3,.6,p)),("Triceps",L(.25,.7,p))])
    return fn
run("bench-press",press("Barbell Bench Press",False,False),0,1,"Bar on chest. Elbows about 45°","Arms straight, chest squeezed","1. Press up with force","2. Lower slowly to mid chest")
run("incline-press",press("Incline Dumbbell Press",True,True),0,1,"Dumbbells at chest sides","Dumbbells close above the chest","1. Press up and slightly in","2. Lower slowly, with control")

# ---------- back exercises, seen from behind ----------
def lat(p,label):
    im,d=mkimg();seat_legs(d)
    d.polygon([S(z) for z in [(cx-56,214),(cx+56,214),(cx+34,342),(cx-34,342)]],fill=SK);head_seated(d,cx,170)
    d.line([S((cx,128)),S((cx-L(88,74,p),L(146,222,p)))],fill=STEEL,width=3*SS);d.line([S((cx,128)),S((cx+L(88,74,p),L(146,222,p)))],fill=STEEL,width=3*SS)
    for s in (-1,1):
        sh=(cx+s*54,224);hand=(cx+s*L(88,74,p),L(146,222,p));elb=(cx+s*L(72,80,p),L(190,272,p))
        capsule(d,sh,elb,18,13,SK2);capsule(d,elb,hand,13,11,SK2)
    hy=L(146,222,p);d.line([S((cx-110,hy)),S((cx+110,hy))],fill=STEEL,width=6*SS)
    ov,o=newov(im);li=L(.45,1,p)
    for s in (-1,1):el(o,cx+s*30,282,18,40,li,rot=s*-8);el(o,cx+s*54,236,11,11,L(.3,.55,p))
    el(o,cx,228,28,14,L(.35,.75,p))
    return finish(im,ov,"Lat Pulldown (seen from behind)",label,[("Lats",li),("Upper back",L(.35,.75,p)),("Biceps",L(.3,.6,p))])
run("lat-pulldown",lat,0,1,"Arms up: feel the lats stretch","Bar at upper chest, elbows down","1. Pull down, elbows to the floor","2. Up slowly, arms straight")
def row(p,label):
    im,d=mkimg();seat_legs(d)
    d.polygon([S(z) for z in [(cx-L(46,58,p),214),(cx+L(46,58,p),214),(cx+34,342),(cx-34,342)]],fill=SK);head_seated(d,cx,L(176,170,p))
    for s in (-1,1):
        sh=(cx+s*L(46,56,p),228);hand=(cx+s*14,L(250,282,p));elb=(cx+s*L(40,92,p),L(262,274,p))
        capsule(d,sh,elb,18,13,SK2);capsule(d,elb,hand,13,11,SK2)
    ov,o=newov(im);li=L(.4,1,p)
    for s in (-1,1):el(o,cx+s*30,284,18,38,li,rot=s*-8);el(o,cx+s*18,238,14,12,L(.3,1,p));el(o,cx+s*54,238,10,10,L(.3,.7,p))
    return finish(im,ov,"Seated Cable Row (seen from behind)",label,[("Lats",li),("Upper back",L(.3,1,p)),("Biceps",L(.3,.6,p))])
run("cable-row",row,0,1,"Arms forward, back rounded a little","Elbows back, shoulder blades together","1. Pull elbows back, chest up","2. Return slowly, arms forward")
def dbrow(p,label):
    im,d=mkimg()
    d.rounded_rectangle([((cx-110)*SS),(300*SS),((cx-10)*SS),(318*SS)],radius=6*SS,fill=MC)
    d.rectangle([((cx-100)*SS),(318*SS),((cx-90)*SS),(FL*SS)],fill=MC);d.rectangle([((cx-30)*SS),(318*SS),((cx-20)*SS),(FL*SS)],fill=MC)
    d.polygon([S(z) for z in [(cx-56,236),(cx+50,236),(cx+34,330),(cx-26,330)]],fill=SK)
    capsule(d,(cx+4,236),(cx+8,214),18,16,SK);d.ellipse([(cx-8)*SS,(184)*SS,(cx+26)*SS,(218)*SS],fill=SK)
    capsule(d,(cx-52,244),(cx-60,292),18,13,SK2)
    sh=(cx+46,244);hand=(cx+L(58,64,p),L(344,278,p));elb=(cx+L(62,96,p),L(296,254,p))
    capsule(d,sh,elb,18,13,SK2);capsule(d,elb,hand,13,11,SK2)
    d.rounded_rectangle([(hand[0]-18)*SS,(hand[1]-6)*SS,(hand[0]+18)*SS,(hand[1]+6)*SS],radius=4*SS,fill=(40,40,48,255),outline=(220,220,225,255),width=2*SS)
    for q in (-1,1):d.rounded_rectangle([(hand[0]+q*17-6)*SS,(hand[1]-13)*SS,(hand[0]+q*17+6)*SS,(hand[1]+13)*SS],radius=3*SS,fill=(40,40,48,255),outline=(220,220,225,255),width=2*SS)
    for x in (cx-30,cx+30):d.rectangle([(x-9)*SS,(330)*SS,(x+9)*SS,(400)*SS],fill=SK)
    ov,o=newov(im);li=L(.4,1,p)
    el(o,cx+22,284,17,36,li,rot=-8);el(o,cx-6,258,24,12,L(.3,.8,p));el(o,cx+46,250,10,10,L(.3,.6,p))
    return finish(im,ov,"Single Dumbbell Row (seen from behind)",label,[("Lats",li),("Upper back",L(.3,.8,p)),("Biceps",L(.3,.6,p))])
run("db-row",dbrow,0,1,"Arm straight: lats stretched","Elbow high, squeeze the back","1. Pull the dumbbell to your waist","2. Lower slowly")

# ---------- pullover, side view ----------
def pull(p,label):
    im,d=mkimg()
    d.rounded_rectangle([((cx-86)*SS),(300*SS),((cx-44)*SS),(314*SS)],radius=6*SS,fill=MC)
    d.rectangle([((cx-76)*SS),(314*SS),((cx-66)*SS),(FL*SS)],fill=MC);d.rectangle([((cx-60)*SS),(314*SS),((cx-50)*SS),(FL*SS)],fill=MC)
    sh=(cx-62,292);hipp=(cx+30,336);knee=(cx+86,318);ank=(cx+96,FL-8)
    capsule(d,sh,hipp,34,30,SK);capsule(d,hipp,knee,26,19,SK);capsule(d,knee,ank,18,12,SK)
    d.ellipse([(ank[0]-8)*SS,(ank[1]-4)*SS,(ank[0]+22)*SS,(ank[1]+10)*SS],fill=SK)
    capsule(d,sh,(sh[0]-24,sh[1]-4),14,13,SK);d.ellipse([(sh[0]-62)*SS,(sh[1]-22)*SS,(sh[0]-26)*SS,(sh[1]+14)*SS],fill=SK)
    a=L(0,-112,p);hand=(sh[0]+88*math.sin(rad(a)),sh[1]-88*math.cos(rad(a)));mid=(sh[0]+44*math.sin(rad(a+6)),sh[1]-44*math.cos(rad(a+6)))
    capsule(d,sh,mid,14,11,SK2);capsule(d,mid,hand,11,9,SK2)
    d.rounded_rectangle([(hand[0]-8)*SS,(hand[1]-26)*SS,(hand[0]+8)*SS,(hand[1]+26)*SS],radius=4*SS,fill=(40,40,48,255),outline=(220,220,225,255),width=2*SS)
    ov,o=newov(im);ci=L(.5,1,1-p if False else p)
    el(o,sh[0]+22,sh[1]-4,22,15,L(.9,.5,p));el(o,sh[0]+8,sh[1]+8,14,18,L(.55,1,p),rot=-20);el(o,(sh[0]+mid[0])/2,(sh[1]+mid[1])/2,8,16,.4,rot=math.degrees(rad(a)))
    return finish(im,ov,"Cross-Bench Dumbbell Pullover",label,[("Chest",L(.9,.5,p)),("Lats",L(.5,1,p)),("Triceps",.4)])
run("pullover",pull,0,1,"Dumbbell above the chest","Arc behind the head, feel the stretch","1. Lower in an arc behind the head","2. Bring it back above the chest")
