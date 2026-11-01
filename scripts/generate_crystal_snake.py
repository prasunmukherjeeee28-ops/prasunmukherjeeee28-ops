from PIL import Image, ImageDraw, ImageFilter
import math, os

W, H = 640, 244
OUT = "dist"
os.makedirs(OUT, exist_ok=True)
route = [(100,92),(180,92),(260,92),(340,92),(420,92),(500,92),(540,110),(540,150),(500,170),(420,170),(340,170),(260,170),(180,170),(100,170),(70,150),(70,110)]
spots = [(475,65),(565,180),(310,135),(125,60),(400,195),(225,125)]

def path(t):
    n=len(route); z=t*n; i=int(z)%n; u=z-int(z)
    p0,p1,p2,p3=route[(i-1)%n],route[i],route[(i+1)%n],route[(i+2)%n]
    def cr(a,b,c,d):
        return .5*((2*b)+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u*u*u)
    return cr(p0[0],p1[0],p2[0],p3[0]),cr(p0[1],p1[1],p2[1],p3[1])

def frame(k, total=48):
    im=Image.new("RGBA",(W,H),(3,8,19,255))
    glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
    gd.ellipse((65,10,380,230),fill=(28,105,220,48))
    gd.ellipse((340,25,635,240),fill=(22,70,180,35))
    im=Image.alpha_composite(im,glow.filter(ImageFilter.GaussianBlur(34)))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((20,18,620,226),radius=18,fill=(7,19,39,238),outline=(125,190,255,75),width=1)
    cols,rows=22,7; x0,y0=32,30; cw,ch=576/cols,184/rows
    for r in range(rows):
        for c in range(cols):
            x,y=x0+c*cw,y0+r*ch
            d.rounded_rectangle((x+2,y+2,x+cw-2,y+ch-2),radius=5,fill=(17,40,68,130),outline=(150,205,255,28),width=1)
    t=k/total; head=path(t)
    body=[path((t-j*.0105)%1) for j in range(12,-1,-1)]
    haze=Image.new("RGBA",(W,H),(0,0,0,0)); hd=ImageDraw.Draw(haze)
    hd.line(body,fill=(35,135,255,185),width=24,joint="curve")
    im=Image.alpha_composite(im,haze.filter(ImageFilter.GaussianBlur(10)))
    d=ImageDraw.Draw(im)
    for j,(x,y) in enumerate(body[:-1]):
        r=8.7-j*.25
        d.ellipse((x-r,y-r,x+r,y+r),fill=(int(85+j*3),int(190+j*3),255,255),outline=(220,248,255,210),width=1)
        d.ellipse((x-r*.55,y-r*.72,x+r*.15,y-r*.25),fill=(255,255,255,90))
    hx,hy=head
    d.ellipse((hx-12,hy-12,hx+12,hy+12),fill=(75,185,255,255),outline=(242,253,255,255),width=2)
    d.ellipse((hx-5,hy-5,hx-2,hy-2),fill=(255,255,255,240))
    d.ellipse((hx+2,hy-3,hx+5,hy+3),fill=(5,27,55,255))
    fx,fy=spots[(k//8)%len(spots)]
    pulse=11+2*math.sin(k*.55)
    f=Image.new("RGBA",(W,H),(0,0,0,0)); fd=ImageDraw.Draw(f)
    fd.ellipse((fx-24,fy-24,fx+24,fy+24),fill=(25,255,125,170))
    im=Image.alpha_composite(im,f.filter(ImageFilter.GaussianBlur(12)))
    d=ImageDraw.Draw(im)
    d.ellipse((fx-pulse,fy-pulse,fx+pulse,fy+pulse),fill=(30,255,130,70))
    d.ellipse((fx-7,fy-7,fx+7,fy+7),fill=(75,255,150,255),outline=(230,255,240,255),width=1)
    d.ellipse((fx-3,fy-4,fx,fy-1),fill=(255,255,255,255))
    d.text((34,7),"CRYSTAL SNAKE  /  LIQUID GLASS",fill=(165,210,250,220))
    return im.convert("P",palette=Image.Palette.ADAPTIVE,colors=96)

frames=[frame(i) for i in range(48)]
frames[0].save(os.path.join(OUT,"crystal-snake.gif"),save_all=True,append_images=frames[1:],duration=90,loop=0,optimize=True,disposal=2)
