from PIL import Image, ImageDraw, ImageFont
import numpy as np
A='/home/claude/oghf-fix/tools/Anton.ttf'
P='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'

YEL=(255,252,0); BLK=(17,17,17); WHT=(255,255,255); TEAL=(19,167,163)
def trim(im):
    a=np.array(im.convert('RGB')).astype(int)
    m=(abs(a-a[5,5]).sum(axis=2)>30)
    ys,xs=np.where(m); return im.crop((xs.min(),ys.min(),xs.max(),ys.max()))
def fit(im,w,h):
    r=min(w/im.width,h/im.height); return im.resize((int(im.width*r),int(im.height*r)),Image.LANCZOS)
def banner(out,hero,lines,sub,size=(1200,628),square=False,bar='TOP'):
    W,H=size; img=Image.new('RGB',size,BLK); d=ImageDraw.Draw(img)
    d.rectangle([0,0,W,16],fill=YEL)
    h=trim(Image.open(hero).convert('RGB'))
    if square:
        pw=W-120; ph=int(H*0.38); card=Image.new('RGB',(pw,ph),WHT)
        f=fit(h,pw-40,ph-30); card.paste(f,((pw-f.width)//2,(ph-f.height)//2))
        img.paste(card,(60,H-ph-60)); tx=60; ty=60; maxw=W-120; fs=[92,92,64]
    else:
        pw=int(W*0.44); card=Image.new('RGB',(pw,H-120),WHT)
        f=fit(h,pw-40,H-160); card.paste(f,((pw-f.width)//2,(H-120-f.height)//2))
        img.paste(card,(W-pw-40,60)); tx=50; ty=60; maxw=W-pw-110; fs=[96,96,56]
    y=ty+10
    for i,(t,col) in enumerate(lines):
        fsz=fs[0]
        while True:
            f=ImageFont.truetype(A,fsz)
            if d.textlength(t,font=f)<=maxw: break
            fsz-=4
        d.text((tx,y),t,font=f,fill=col); y+=int(fsz*1.2)
    y+=14
    fs2=ImageFont.truetype(P,30 if not square else 32)
    for s in sub:
        # wrap
        words=s.split(); line=''
        for w_ in words:
            if d.textlength((line+' '+w_).strip(),font=fs2)>maxw: d.text((tx,y),line,font=fs2,fill=WHT); y+=int(fs2.size*1.35); line=w_
            else: line=(line+' '+w_).strip()
        d.text((tx,y),line,font=fs2,fill=WHT); y+=int(fs2.size*1.35)
    # footer tagline
    ft=ImageFont.truetype(P,22 if not square else 26)
    d.text((tx,H-48 if not square else 18+0),"" ,font=ft,fill=YEL)
    if not square: d.text((tx,H-50),"offgridhomesteadfam.com",font=ft,fill=YEL)
    img.save(out,optimize=True)
R='/home/claude/oghf-fix/repo/product_images/'
LIB=R+'library_hero_noprice.png'; STA=R+'starter_hero_noprice.png'; SET=R+'offgrid_set_hero_noprice.png'; UPG=R+'library_upgrade_listing.png'
O='/home/claude/oghf-fix/out/bf/'
jobs={
 'bf_teaser':(LIB,[('BLACK FRIDAY',YEL),('IS A PLAN,',WHT),('NOT A PANIC',WHT)],['Three bundles. Four days. Nov 27 to 30.']),
 'bf_launch':(LIB,[('BLACK FRIDAY',YEL),('BUNDLES ONLY',WHT),('25% OFF',YEL)],['Starter. Library. Offgrid Set. Open now through Monday night.']),
 'bf_lastcall':(STA,[('LAST CALL',YEL),('BUNDLES 25% OFF',WHT),('ENDS TONIGHT',WHT)],['Midnight Mountain. Tomorrow they go back to regular price.']),
 'upg_offer':(UPG,[('COMPLETE',YEL),('YOUR LIBRARY',WHT),('PLANNER OWNERS',YEL)],['20% off the other five books. No second Planner in the box.']),
 'upg_lastcall':(UPG,[('PRICE ENDS',YEL),('SUNDAY',WHT),('PLANNER OWNERS',YEL)],['Midnight Mountain. The five books go back to full price.']),
}
for k,(h,l,s) in jobs.items():
    banner(O+k+'_email.png',h,l,s)
    banner(O+k+'_square.png',h,l,s,size=(1080,1080),square=True)
print('ok')
