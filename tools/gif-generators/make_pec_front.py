import math
from gif_lib import *
from PIL import Image, ImageDraw, ImageFilter
SK=(236,240,247,255);SK2=(205,212,225,255);GR=(70,255,110);MC=(60,70,90,255)
def lerp(a,b,t):
    t=ease(t);return a+(b-a)*t
def draw(p,label,c_int,d_int):
    im=BASE.copy();d=ImageDraw.Draw(im)
    cx=262
    # machine: back pad, seat, legs
    d.rounded_rectangle([((cx-52)*SS),(205*SS),((cx+52)*SS),(345*SS)],radius=10*SS,fill=MC)
    d.rounded_rectangle([((cx-70)*SS),(338*SS),((cx+70)*SS),(356*SS)],radius=8*SS,fill=MC)
    d.rectangle([((cx-8)*SS),(356*SS),((cx+8)*SS),(FL*SS)],fill=MC)
    # legs (seated, front view)
    for s in (-1,1):
        hip=(cx+s*20,338);knee=(cx+s*58,372);ank=(cx+s*62,FL-8)
        capsule(d,hip,knee,28,22,SK);capsule(d,knee,ank,20,13,SK)
        d.ellipse([(ank[0]-14)*SS,(ank[1]-4)*SS,(ank[0]+14)*SS,(ank[1]+10)*SS],fill=SK)
    # torso
    d.polygon([S(z) for z in [(cx-50,215),(cx+50,215),(cx+30,340),(cx-30,340)]],fill=SK)
    capsule(d,(cx,200),(cx,184),16,14,SK)
    d.ellipse([(cx-17)*SS,(160-17)*SS,(cx+17)*SS,(160+17)*SS],fill=SK)
    # arms: open (p=0) -> closed (p=1)
    hands={}
    for s in (-1,1):
        sh=(cx+s*50,222)
        hand=(cx+s*lerp(112,14,p),lerp(206,232,p))
        el=((sh[0]+hand[0])/2+s*lerp(4,26,p),(sh[1]+hand[1])/2+lerp(12,16,p))
        # machine lever
        piv=(cx+s*128,96)
        d.line([S(hand),S((hand[0]+s*6,hand[1]-40)),S(piv)],fill=(150,160,180,255),width=4*SS)
        capsule(d,sh,el,18,13,SK2);capsule(d,el,hand,13,11,SK2)
        hands[s]=hand
        d.rounded_rectangle([(hand[0]-6)*SS,(hand[1]-30)*SS,(hand[0]+6)*SS,(hand[1]+30)*SS],radius=5*SS,fill=(40,40,48,255),outline=(220,220,225,255),width=2*SS)
    ov=Image.new("RGBA",im.size,(0,0,0,0));o=ImageDraw.Draw(ov)
    def el(x,y,rx,ry,i):
        o.ellipse([(x-rx)*SS,(y-ry)*SS,(x+rx)*SS,(y+ry)*SS],fill=GR+(int(255*i),))
    for s in (-1,1):
        el(cx+s*24,238,26,15,c_int);el(cx+s*54,222,11,11,d_int)
    glow=ov.filter(ImageFilter.GaussianBlur(7*SS));im=Image.alpha_composite(im,glow);im=Image.alpha_composite(im,glow)
    sh_=ov.copy();sh_.putalpha(sh_.getchannel("A").point(lambda v:int(v*.55)));im=Image.alpha_composite(im,sh_)
    d=ImageDraw.Draw(im)
    for i,(k,v) in enumerate((("Chest",c_int),("Shoulders",d_int))):mini(d,10+i*80,4,k,v>.5,k)
    d.text((14*SS,96*SS),"Pec Deck (Chest Fly Machine)",font=FB,fill=(255,255,255,255))
    d.text((14*SS,114*SS),label,font=FS,fill=(255,170,90,255))
    return im.convert("RGB").resize((W,H),Image.LANCZOS)
per=24;fr=[]
fr.append((0,"Arms open: feel the chest stretch",.45,.3,2200))
for j in range(1,per):
    t=ease(j/per);fr.append((t,"1. Bring the handles together",.45+.55*t,.3+.25*t,80))
fr.append((1,"Squeeze the chest in front",1,.55,2200))
for j in range(1,per):
    t=ease(j/per);fr.append((1-t,"2. Open slowly, with control",1-.55*t,.55-.25*t,70))
imgs=[draw(p,l,c,d_) for p,l,c,d_,_ in fr];dur=[x[-1] for x in fr]
imgs[0].save("img/pec-deck-front.gif",save_all=True,append_images=imgs[1:],duration=dur,loop=0,optimize=False)
n=len(imgs);s=Image.new("RGB",(W*3,H))
for k,i in enumerate((0,n//4,n//2)):s.paste(imgs[i],(k*W,0))
s.save("/tmp/pecfront.png");print(n)
