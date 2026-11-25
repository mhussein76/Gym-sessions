src=open('make_six.py',encoding='utf8').read()
exec(src[:src.index('# ---------- pressing')])
import math
def rect(d,x0,y0,x1,y1,col=MC,r=5):d.rounded_rectangle([x0*SS,y0*SS,x1*SS,y1*SS],radius=r*SS,fill=col)
def disc(d,c,r,col=(34,34,42,255)):
    d.ellipse([(c[0]-r)*SS,(c[1]-r)*SS,(c[0]+r)*SS,(c[1]+r)*SS],fill=col,outline=(220,220,225,255),width=2*SS)
def ik2(P,Q,l1,l2,key):
    dx,dy=Q[0]-P[0],Q[1]-P[1];D=max(math.hypot(dx,dy),1e-3);D=min(D,l1+l2-0.5)
    ux,uy=dx/math.hypot(dx,dy),dy/math.hypot(dx,dy)
    a=(l1*l1-l2*l2+D*D)/(2*D);h=math.sqrt(max(l1*l1-a*a,0))
    mx,my=P[0]+ux*a,P[1]+uy*a
    cs=[(mx-uy*h,my+ux*h),(mx+uy*h,my-ux*h)]
    return min(cs,key=key)
def poly(d,pts,col):d.polygon([S(p) for p in pts],fill=col)
def deg(a,b):return math.degrees(math.atan2(b[1]-a[1],b[0]-a[0]))
def addv(*vs):return (sum(v[0] for v in vs),sum(v[1] for v in vs))
def mul(v,k):return (v[0]*k,v[1]*k)
R=(0.7071,-0.7071);PN=(0.7071,0.7071)
T_=66
def inset(d,kind):
    x0,y0,x1,y1=292,6,408,80
    d.rounded_rectangle([x0*SS,y0*SS,x1*SS,y1*SS],radius=6*SS,fill=(120,128,140,255),outline=(220,225,235,255),width=2*SS)
    pos={"mid":[(.36,.5,0),(.64,.5,0)],"high":[(.40,.26,0),(.60,.26,0)],"wide":[(.2,.46,-28),(.8,.46,28)],"calf":[(.40,.9,0),(.60,.9,0)]}[kind]
    for fx,fy,rot in pos:
        cxx=x0+(x1-x0)*fx;cyy=y0+(y1-y0)*fy;pts=[]
        for k in range(28):
            t=2*math.pi*k/28;px,py=7*math.cos(t),14*math.sin(t)
            r=math.radians(rot);pts.append(S((cxx+px*math.cos(r)-py*math.sin(r),cyy+px*math.sin(r)+py*math.cos(r))))
        d.polygon(pts,fill=(255,150,70,255))
    d.text((x0*SS,(y1+2)*SS),"Feet on the plate",font=FS,fill=(235,240,250,255))

def leg_press(title,u,kind,glow,thumbs,s0=58,s1=124,calf=False):
    def f(p,label):
        im,d=mkimg()
        H=(150,345)
        s=L(s0,s1,p)
        # frame / rail
        d.rounded_rectangle([70*SS,406*SS,350*SS,414*SS],radius=3*SS,fill=MC)
        r0=addv(H,mul(R,-20),mul(PN,75));r1=addv(H,mul(R,190),mul(PN,75))
        d.line([S(r0),S(r1)],fill=STEEL,width=6*SS)
        # seat + back pad
        tt=(-0.7071,-0.7071);sh=addv(H,mul(tt,78));head=addv(sh,mul(tt,30),(-2,-2))
        sft=(-0.7071*22*-1*0,0)
        bk=(-0.7071,0.7071)
        b0=addv(H,mul(bk,20));b1=addv(sh,mul(bk,20),mul(tt,16))
        capsule(d,b0,b1,12,12,MC)
        rect(d,H[0]-34,H[1]+18,H[0]+18,H[1]+30,MC,4)
        rect(d,H[0]-14,H[1]+30,H[0]-4,408,MC,3)
        capsule(d,b1,(b1[0]-26,408),8,8,MC)
        # sled plate
        S0=s+14
        c=[addv(H,mul(R,S0),mul(PN,-72)),addv(H,mul(R,S0),mul(PN,72)),addv(H,mul(R,S0+16),mul(PN,72)),addv(H,mul(R,S0+16),mul(PN,-72))]
        poly(d,c,(176,184,198,255))
        # weight plates behind
        for k,off in enumerate((24,38)):
            w=[addv(H,mul(R,S0+off),mul(PN,-34)),addv(H,mul(R,S0+off),mul(PN,34)),addv(H,mul(R,S0+off+10),mul(PN,34)),addv(H,mul(R,S0+off+10),mul(PN,-34))]
            poly(d,w,(34,34,42,255))
        # carriage to rail
        capsule(d,addv(H,mul(R,S0+4),mul(PN,70)),addv(H,mul(R,S0+4),mul(PN,75)),9,9,STEEL)
        # legs
        A=addv(H,mul(R,s),mul(PN,u))
        K=ik2(H,A,T_,T_,key=lambda c:c[0]+c[1])
        capsule(d,H,K,28,19,SK);capsule(d,K,A,19,13,SK)
        if calf:
            ang=L(0,28,p)
        toe=addv(A,mul(R,12),mul(PN,-22))
        if calf:
            toe=addv(A,mul(R,12+L(0,0,p)),mul(PN,-22))
        capsule(d,A,toe,12,9,SK)
        # torso, head, arm
        capsule(d,H,sh,34,36,SK);d.ellipse([(head[0]-16)*SS,(head[1]-16)*SS,(head[0]+16)*SS,(head[1]+16)*SS],fill=SK)
        hand=addv(H,(-4,-12));capsule(d,sh,hand,15,11,SK2)
        # glow
        ov,o=newov(im)
        v=(K[0]-H[0],K[1]-H[1]);vl=math.hypot(*v);n1=(-v[1]/vl,v[0]/vl)
        nf=n1 if (n1[0]*(A[0]-H[0])+n1[1]*(A[1]-H[1]))<0 else (-n1[0],-n1[1])
        mid=((H[0]+K[0])/2,(H[1]+K[1])/2);ang=deg(H,K)
        gl=glow(p)
        for name,val in gl.items():
            if name=="quad":el(o,mid[0]+nf[0]*6,mid[1]+nf[1]*6,30,9,val,rot=ang)
            if name=="ham":el(o,mid[0]-nf[0]*6,mid[1]-nf[1]*6,30,9,val,rot=ang)
            if name=="glute":el(o,H[0]-3,H[1]+4,14,13,val)
            if name=="inner":el(o,mid[0],mid[1],27,6,val,rot=ang)
            if name=="calf":
                m2=((K[0]+A[0])/2,(K[1]+A[1])/2);a2=deg(K,A)
                el(o,m2[0]-nf[0]*6,m2[1]-nf[1]*6,26,8,val,rot=a2)
        inset(d,kind)
        return finish(im,ov,title,label,thumbs(p))
    return f

mid_glow=lambda p:{"quad":L(.4,1,p)}
run("leg-press-mid",leg_press("Leg Press - Feet in the Middle",0,"mid",mid_glow,lambda p:[("Quads",L(.4,1,p)),("Glutes",L(.2,.6,p))]),0,1,"Feet in the middle, shoulder-width apart","Legs almost straight. Do not lock the knees","1. Push the plate away with your whole foot","2. Lower slowly until the knees are about 90")
high_glow=lambda p:{"glute":L(.4,1,p),"ham":L(.4,1,p)}
run("leg-press-high",leg_press("Leg Press - Feet High",-26,"high",high_glow,lambda p:[("Glutes",L(.4,1,p)),("Hamstrings",L(.4,1,p))]),0,1,"Feet high on the plate, shoulder-width apart","Push through the heels. Squeeze the glutes","1. Push the plate away through your heels","2. Lower slowly, knees stay in line with toes")
wide_glow=lambda p:{"inner":L(.4,1,p),"quad":L(.2,.5,p)}
run("leg-press-wide",leg_press("Leg Press - Wide Feet",0,"wide",wide_glow,lambda p:[("Adductors",L(.4,1,p)),("Quads",L(.2,.5,p))]),0,1,"Feet wide, toes turned out a little","Legs almost straight. Do not lock the knees","1. Push the plate away, knees follow the toes","2. Lower slowly, feel the inner thigh stretch")
calf_glow=lambda p:{"calf":L(.4,1,p)}
run("leg-press-calf",leg_press("Leg Press Calf Raise",46,"calf",calf_glow,lambda p:[("Calves",L(.4,1,p))],s0=114,s1=124,calf=True),0,1,"Toes on the bottom edge, legs almost straight","Pushed up on the toes. Squeeze the calves","1. Push up on your toes, knees stay still","2. Lower the heels slowly for a full stretch")

def seat_back(d,hipx):
    rect(d,hipx-48,354,hipx+54,368,MC,5);rect(d,hipx-8,368,hipx+4,408,MC,3)
    capsule(d,(hipx-44,366),(hipx-38,236),12,12,MC)
    rect(d,hipx-60,406,hipx+110,414,MC,3)

def torso(d,hip,lean=-8):
    sh=up(hip,78,lean);head=up(sh,32,lean*.6)
    capsule(d,hip,sh,34,36,SK);d.ellipse([(head[0]-16)*SS,(head[1]-16)*SS,(head[0]+16)*SS,(head[1]+16)*SS],fill=SK)
    capsule(d,sh,(hip[0]+14,hip[1]-6),15,11,SK2)
    return sh

def leg_curl(p,label):
    im,d=mkimg()
    hip=(cx-34,336);seat_back(d,hip[0])
    knee=pt(hip,66,86);A_=L(80,-18,p);ank=pt(knee,64,A_)
    torso(d,hip)
    capsule(d,hip,knee,28,19,SK);capsule(d,knee,ank,19,13,SK)
    capsule(d,ank,(ank[0]+math.cos(rad(A_))*0+14,ank[1]+4),11,9,SK)
    # thigh hold-down pad
    rect(d,knee[0]-36,knee[1]-32,knee[0]+4,knee[1]-18,MC,5);capsule(d,(knee[0]-16,knee[1]-32),(knee[0]-16,knee[1]-72),9,9,MC)
    # ankle pad on lever
    n=(-math.cos(rad(A_)),math.sin(rad(A_)));pad=(ank[0]+n[0]*11,ank[1]+n[1]*11)
    capsule(d,pad,(cx-8,380),8,8,STEEL);disc(d,pad,9,(60,70,90,255))
    ov,o=newov(im);hm=L(.35,1,p)
    el(o,(hip[0]+knee[0])/2,(hip[1]+knee[1])/2+6,30,8,hm,rot=3)
    m2=((knee[0]+ank[0])/2+n[0]*5,(knee[1]+ank[1])/2+n[1]*5);el(o,m2[0],m2[1],24,7,L(.3,.8,p),rot=deg(knee,ank))
    return finish(im,ov,"Seated Leg Curl (side view)",label,[("Hamstrings",hm),("Calves",L(.3,.8,p))])
run("leg-curl",leg_curl,0,1,"Legs straight, pad just above the heels","Heels pulled back. Squeeze the hamstrings","1. Pull the pad down and back with your heels","2. Return slowly, do not let the weight drop")

def leg_ext(p,label):
    im,d=mkimg()
    hip=(cx-34,336);seat_back(d,hip[0])
    knee=pt(hip,66,86);A_=L(8,82,p);ank=pt(knee,64,A_)
    torso(d,hip)
    capsule(d,hip,knee,28,19,SK);capsule(d,knee,ank,19,13,SK)
    capsule(d,ank,(ank[0]+13,ank[1]+3),11,9,SK)
    n=(math.cos(rad(A_)),-math.sin(rad(A_)));pad=(ank[0]+n[0]*11,ank[1]+n[1]*11)
    capsule(d,pad,(knee[0]-4,372),8,8,STEEL);disc(d,pad,9,(60,70,90,255))
    ov,o=newov(im);qi=L(.35,1,p)
    el(o,(hip[0]+knee[0])/2,(hip[1]+knee[1])/2-6,30,8,qi,rot=3)
    m2=((knee[0]+ank[0])/2-n[0]*0,(knee[1]+ank[1])/2);el(o,m2[0]+n[0]*5,m2[1]+n[1]*5,24,6,L(.2,.6,p),rot=deg(knee,ank))
    return finish(im,ov,"Leg Extension (side view)",label,[("Quads",qi)])
run("leg-extension",leg_ext,0,1,"Knees bent, pad on the front of the shins","Legs straight. Squeeze the front thigh","1. Straighten the legs, do not swing","2. Lower slowly, with control")

def bulg(p,label):
    im,d=mkimg()
    A1=(cx+30,404);A2=(cx-118,344);hx=cx-28
    hy=L(292,330,p);H=(hx,hy)
    # bench + support post
    rect(d,cx-156,352,cx-84,364,MC,4);rect(d,cx-150,364,cx-140,408,MC,3);rect(d,cx-100,364,cx-90,408,MC,3)
    rect(d,cx+50,236,cx+60,408,MC,3);rect(d,cx+30,404,cx+84,412,MC,3)
    K1=ik2(H,A1,64,64,key=lambda c:-c[0]);K2=ik2(H,A2,64,64,key=lambda c:-c[1])
    capsule(d,H,K2,26,18,SK2);capsule(d,K2,A2,18,12,SK2);capsule(d,A2,(A2[0]-12,A2[1]+2),11,9,SK2)
    capsule(d,H,K1,28,19,SK);capsule(d,K1,A1,19,13,SK);capsule(d,A1,(A1[0]+22,A1[1]),11,9,SK)
    sh=up(H,78,6);head=up(sh,32,4)
    capsule(d,H,sh,34,36,SK);d.ellipse([(head[0]-16)*SS,(head[1]-16)*SS,(head[0]+16)*SS,(head[1]+16)*SS],fill=SK)
    hand=(cx+55,258);E=ik2(sh,hand,46,46,key=lambda c:-c[1])
    capsule(d,sh,E,15,11,SK2);capsule(d,E,hand,11,9,SK2)
    ov,o=newov(im);qi=L(.3,1,p)
    mid=((H[0]+K1[0])/2,(H[1]+K1[1])/2);el(o,mid[0]+8,mid[1]-4,28,9,qi,rot=deg(H,K1))
    el(o,H[0]-6,H[1]+6,14,12,L(.3,.9,p))
    return finish(im,ov,"Supported Bulgarian Split Squat (side view)",label,[("Quads",qi),("Glutes",L(.3,.9,p))])
run("bulgarian-split-squat",bulg,0,1,"Back foot on the bench, hand on a support","Front knee about 90. Chest tall, lean a little","1. Lower straight down, front knee over the foot","2. Push through the front heel to stand")
