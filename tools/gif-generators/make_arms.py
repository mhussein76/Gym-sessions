src=open('make_six.py',encoding='utf8').read()
exec(src[:src.index('# ---------- pressing')])
WH=(34,34,42,255);RIM=(220,220,225,255)
def rect(d,x0,y0,x1,y1,col=MC,r=5):d.rounded_rectangle([x0*SS,y0*SS,x1*SS,y1*SS],radius=r*SS,fill=col)
def disc(d,c,r):
    d.ellipse([(c[0]-r)*SS,(c[1]-r)*SS,(c[0]+r)*SS,(c[1]+r)*SS],fill=WH,outline=RIM,width=2*SS)
def stand(d,lean):
    ank=(cx,404);knee=(cx+3,340);hip=(cx,276)
    capsule(d,hip,knee,28,19,SK);capsule(d,knee,ank,19,13,SK);capsule(d,ank,(cx+22,404),11,9,SK)
    sh=up(hip,78,lean);head=up(sh,32,lean*.6)
    capsule(d,hip,sh,34,36,SK);d.ellipse([(head[0]-16)*SS,(head[1]-16)*SS,(head[0]+16)*SS,(head[1]+16)*SS],fill=SK)
    return hip,sh
def sit(d):
    rect(d,cx-70,352,cx+30,366);rect(d,cx-50,366,cx-40,FL);rect(d,cx+10,366,cx+20,FL)
    rect(d,cx-78,250,cx-66,356,MC,5)
    hip=(cx-30,342);knee=(cx+38,346);ank=(cx+44,FL-8)
    capsule(d,hip,knee,28,19,SK);capsule(d,knee,ank,19,13,SK);capsule(d,ank,(ank[0]+20,ank[1]),11,9,SK)
    sh=up(hip,78,-2);head=up(sh,32,-2)
    capsule(d,hip,sh,34,36,SK);d.ellipse([(head[0]-16)*SS,(head[1]-16)*SS,(head[0]+16)*SS,(head[1]+16)*SS],fill=SK)
    return hip,sh

def curl(title,close):
    def f(p,label):
        im,d=mkimg();hip,sh=stand(d,0)
        a=4;E=pt(sh,44,a);fa=L(6,150,p);Hh=pt(E,42,fa)
        capsule(d,sh,E,17,12,SK2);capsule(d,E,Hh,12,10,SK2);disc(d,Hh,11)
        ov,o=newov(im);bi=L(.35,1,p)
        mid=((sh[0]+E[0])/2+7,(sh[1]+E[1])/2);el(o,mid[0],mid[1],7,19,bi,rot=-a)
        fm=((E[0]+Hh[0])/2,(E[1]+Hh[1])/2);el(o,fm[0],fm[1],6,15,L(.2,.7,p),rot=-fa+180)
        return finish(im,ov,title,label,[("Biceps",bi),("Forearms",L(.2,.7,p))])
    return f
run("ez-curl-close",curl("EZ-Bar Curl - Close Grip (side view)",1),0,1,"Hands close together, elbows at your sides","Squeeze the biceps at the top","1. Curl the bar up, elbows stay still","2. Lower slowly, arms almost straight")
run("ez-curl-wide",curl("EZ-Bar Curl - Wide Grip (side view)",0),0,1,"Hands wide on the outer curves","Squeeze the biceps at the top","1. Curl the bar up, elbows stay still","2. Lower slowly, arms almost straight")

def hammer(p,label):
    im,d=mkimg();hip,sh=sit(d)
    a=3;E=pt(sh,44,a);fa=L(6,150,p);Hh=pt(E,42,fa)
    capsule(d,sh,E,17,12,SK2);capsule(d,E,Hh,12,10,SK2)
    d.rounded_rectangle([(Hh[0]-18)*SS,(Hh[1]-7)*SS,(Hh[0]+18)*SS,(Hh[1]+7)*SS],radius=4*SS,fill=WH,outline=RIM,width=2*SS)
    ov,o=newov(im);bi=L(.35,.9,p);fo=L(.3,1,p)
    mid=((sh[0]+E[0])/2+7,(sh[1]+E[1])/2);el(o,mid[0],mid[1],7,19,bi,rot=-a)
    fm=((E[0]+Hh[0])/2,(E[1]+Hh[1])/2);el(o,fm[0],fm[1],7,17,fo,rot=-fa+180)
    return finish(im,ov,"Seated Hammer Curl (side view)",label,[("Biceps",bi),("Forearms",fo)])
run("hammer-curl",hammer,0,1,"Palms face each other, elbows at your sides","Squeeze at the top. No swinging","1. Curl the dumbbells up","2. Lower slowly, with control")

def pushdown(title,lean):
    def f(p,label):
        im,d=mkimg();hip,sh=stand(d,lean)
        a=6;E=pt(sh,44,a);fa=L(108,6,p);Hh=pt(E,42,fa)
        pul=(cx+62,46);rect(d,cx+50,40,cx+74,52,MC,4);d.line([S(pul),S(Hh)],fill=STEEL,width=3*SS)
        capsule(d,sh,E,17,12,SK2);capsule(d,E,Hh,12,10,SK2);disc(d,Hh,7)
        ov,o=newov(im);tr=L(.35,1,p)
        mid=((sh[0]+E[0])/2-7,(sh[1]+E[1])/2);el(o,mid[0],mid[1],7,19,tr,rot=-a)
        return finish(im,ov,title,label,[("Triceps",tr),("Forearms",L(.2,.6,p))])
    return f
run("rope-pushdown",pushdown("Rope Pushdown (side view)",8),0,1,"Elbows pinned to your sides, hands up","Arms straight. Spread the rope apart","1. Push the rope down, elbows stay still","2. Come back up slowly")
run("bar-pushdown",pushdown("Straight-Bar Pushdown (side view)",12),0,1,"Elbows pinned to your sides, hands up","Arms straight. Squeeze the triceps","1. Push the bar down, elbows stay still","2. Come back up slowly")

def overhead(p,label):
    im,d=mkimg();hip,sh=stand(d,22)
    a=162;E=pt(sh,44,a);fa=L(-25,-210,p);Hh=pt(E,42,fa)
    low=(cx-120,380);rect(d,low[0]-10,330,low[0]+10,FL,MC,4);d.line([S(low),S(Hh)],fill=STEEL,width=3*SS)
    capsule(d,sh,E,17,12,SK2);capsule(d,E,Hh,12,10,SK2);disc(d,Hh,7)
    ov,o=newov(im);tr=L(.4,1,p)
    mid=((sh[0]+E[0])/2-7,(sh[1]+E[1])/2);el(o,mid[0],mid[1],7,19,tr,rot=-a)
    return finish(im,ov,"Overhead Cable Extension (side view)",label,[("Triceps",tr),("Shoulders",.2)])
run("overhead-extension",overhead,0,1,"Elbows point forward, rope behind the head","Arms straight. Squeeze the triceps","1. Straighten the arms up and forward","2. Bend slowly, elbows stay still")

def wrist(reverse):
    def f(p,label):
        im,d=mkimg()
        rect(d,cx-150,300,cx+20,330,MC,8);rect(d,cx-120,330,cx-108,FL,MC);rect(d,cx-20,330,cx-8,FL,MC)
        wr=(cx+40,292);el0=(cx-150,292)
        capsule(d,el0,wr,28,20,SK2)
        th=L(-58,52,p);th=th if not reverse else L(-58,52,p)
        end=(wr[0]+40*math.cos(rad(th)),wr[1]-40*math.sin(rad(th)))
        capsule(d,wr,end,20,16,SK);disc(d,(end[0]+ (6 if True else 0),end[1]),12)
        ov,o=newov(im);fo=L(.35,1,p)
        yoff=-10 if reverse else 11
        el(o,cx-55,292+yoff,52,7,fo,rot=0)
        return finish(im,ov,("Reverse " if reverse else "")+"Wrist Curl (side view)",label,[("Forearms",fo)])
    return f
run("wrist-curl",wrist(False),0,1,"Forearm on the bench, hand dropped down","Wrist curled up. Squeeze the forearm","1. Curl the wrist up, palm facing up","2. Lower slowly, fingers open a little")
run("reverse-wrist-curl",wrist(True),0,1,"Forearm on the bench, palm down, hand dropped","Wrist lifted up. Squeeze the forearm","1. Lift the back of the hand up","2. Lower slowly, with control")
