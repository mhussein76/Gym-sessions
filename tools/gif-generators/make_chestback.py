import math
from gif_lib import *
from PIL import Image, ImageDraw, ImageFilter
SK=(236,240,247,255);SK2=(196,204,218,255);GR=(70,255,110)
def finish(im,ov,title,label,thumbs):
    glow=ov.filter(ImageFilter.GaussianBlur(7*SS));im=Image.alpha_composite(im,glow);im=Image.alpha_composite(im,glow)
    sharp=ov.copy();sharp.putalpha(sharp.getchannel("A").point(lambda v:int(v*.55)));im=Image.alpha_composite(im,sharp)
    d=ImageDraw.Draw(im)
    for i,(k,v) in enumerate(thumbs):mini(d,10+i*80,4,k,v>.5,k)
    d.text((14*SS,96*SS),title,font=FB,fill=(255,255,255,255))
    d.text((14*SS,114*SS),label,font=FS,fill=(255,170,90,255))
    return im.convert("RGB").resize((W,H),Image.LANCZOS)
def lerp(a,b,t):
    t=ease(t);return{k:a[k]+(b[k]-a[k])*t for k in a}
def seqframes(A,B,labA,labB,labMidAB,labMidBA,per=24):
    fr=[(A,labA,2200)]+[(lerp(A,B,j/per),labMidAB,80) for j in range(1,per)]
    fr+=[(B,labB,2200)]+[(lerp(B,A,j/per),labMidBA,70) for j in range(1,per)]
    return fr
def save(name,fr,fn):
    imgs=[fn(P,l) for P,l,_ in fr];dur=[d for _,_,d in fr]
    imgs[0].save(f"img/{name}.gif",save_all=True,append_images=imgs[1:],duration=dur,loop=0,optimize=False)
    n=len(imgs);sh=Image.new("RGB",(W*3,H))
    for k,i in enumerate((0,n//4,n//2)):sh.paste(imgs[i],(k*W,0))
    sh.save(f"/tmp/{name}.png");print(name,n)

# ---------- Pec Deck ----------
def pec(P,label):
    im=BASE.copy();d=ImageDraw.Draw(im)
    hip=(200,338);sh=up(hip,78,-4);head=up(sh,30,-2)
    # seat + back pad
    d.rounded_rectangle([(150*SS,338*SS),(250*SS,352*SS)],radius=6*SS,fill=(60,70,90,255))
    d.rounded_rectangle([(138*SS,238*SS),(160*SS,340*SS)],radius=8*SS,fill=(60,70,90,255))
    d.rectangle([(190*SS,352*SS),(200*SS,FL*SS)],fill=(60,70,90,255))
    knee=(hip[0]+66,hip[1]);ankle=(knee[0]+4,FL-6)
    capsule(d,hip,knee,26,18,SK);capsule(d,knee,ankle,17,11,SK);capsule(d,ankle,(ankle[0]+22,ankle[1]+3),10,8,SK)
    capsule(d,hip,sh,32,38,SK);capsule(d,sh,up(sh,14,-2),13,13,SK)
    d.ellipse([(head[0]-15)*SS,(head[1]-15)*SS,(head[0]+15)*SS,(head[1]+15)*SS],fill=SK)
    el=pt(sh,44,P["a"]);hand=(el[0],el[1]-42)
    capsule(d,sh,el,14,10,SK);capsule(d,el,hand,10,8,SK)
    d.rounded_rectangle([(hand[0]-7)*SS,(hand[1]-30)*SS,(hand[0]+7)*SS,(hand[1]+12)*SS],radius=6*SS,fill=(40,40,48,255),outline=(220,220,225,255),width=2*SS)
    ov=Image.new("RGBA",im.size,(0,0,0,0));o=ImageDraw.Draw(ov)
    blob(o,hip,sh,.8,11,.4,26,P["c"],GR);blob(o,sh,el,.2,0,.55,18,P["d"],GR)
    return finish(im,ov,"Pec Deck (Chest Fly Machine)",label,[("Chest",P["c"]),("Shoulders",P["d"])])
o=dict(a=-80,c=.45,d=.3);c=dict(a=82,c=1.0,d=.55)
save("pec-deck",seqframes(o,c,"Arms open: feel the chest stretch","Squeeze the chest in front","1. Bring the handles together","2. Open slowly, with control"),pec)

# ---------- Seated bench V-ups ----------
def vup(P,label):
    im=BASE.copy();d=ImageDraw.Draw(im)
    hip=(185,330)
    d.rounded_rectangle([(120*SS,330*SS),(240*SS,346*SS)],radius=6*SS,fill=(60,70,90,255))
    d.rectangle([(135*SS,346*SS),(148*SS,FL*SS)],fill=(60,70,90,255));d.rectangle([(215*SS,346*SS),(228*SS,FL*SS)],fill=(60,70,90,255))
    sh=up(hip,78,P["tt"]);head=up(sh,30,P["tt"]*.6)
    knee=pt(hip,66,P["leg"]);ankle=pt(knee,66,P["leg"])
    capsule(d,hip,knee,26,18,SK);capsule(d,knee,ankle,17,11,SK);capsule(d,ankle,(ankle[0]+math.cos(rad(P["leg"]))*-10+12,ankle[1]-8),9,8,SK)
    capsule(d,hip,sh,32,38,SK);capsule(d,sh,up(sh,14,P["tt"]*.6),13,13,SK)
    d.ellipse([(head[0]-15)*SS,(head[1]-15)*SS,(head[0]+15)*SS,(head[1]+15)*SS],fill=SK)
    el=pt(sh,42,P["a"]);wr=pt(el,40,P["a"]);capsule(d,sh,el,14,10,SK2);capsule(d,el,wr,10,8,SK2)
    ov=Image.new("RGBA",im.size,(0,0,0,0));o=ImageDraw.Draw(ov)
    blob(o,hip,sh,.5,12,.55,24,P["ab"],GR);blob(o,hip,knee,.22,-9,.45,17,P["hf"],GR);blob(o,hip,knee,.7,-8,.6,15,P["q"],GR)
    return finish(im,ov,"Seated Bench V-Ups",label,[("Abs",P["ab"]),("Hip flexors",P["hf"])])
op=dict(tt=-38,leg=68,a=4,ab=.4,hf=.35,q=.3);cl=dict(tt=8,leg=132,a=-14,ab=1.0,hf=.9,q=.6)
save("v-ups",seqframes(op,cl,"Lean back, legs low. Chest stays up","Legs and chest meet in a V. Breathe out","1. Bring knees and chest together","2. Go back slowly, back not arched"),vup)
