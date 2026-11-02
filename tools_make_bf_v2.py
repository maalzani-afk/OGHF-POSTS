from PIL import Image, ImageDraw, ImageFont
import numpy as np
A='/home/claude/oghf-fix/tools/Anton.ttf'; PB='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
YEL=(255,252,0); BLK=(17,17,17); WHT=(255,255,255); GRY=(150,150,150)
R='/home/claude/oghf-fix/repo/product_images/'
def trim(im):
    a=np.array(im.convert('RGB')).astype(int); m=(abs(a-a[5,5]).sum(axis=2)>30); ys,xs=np.where(m)
    return im.crop((xs.min(),ys.min(),xs.max(),ys.max()))
def fit(im,w,h):
    r=min(w/im.width,h/im.height); return im.resize((int(im.width*r),int(im.height*r)),Image.LANCZOS)
def F(p,s): return ImageFont.truetype(p,s)
def canvas(hero,W=1200,H=628,cardw=400):
    img=Image.new('RGB',(W,H),BLK); d=ImageDraw.Draw(img); d.rectangle([0,0,W,16],fill=YEL)
    h=trim(Image.open(hero).convert('RGB')); card=Image.new('RGB',(cardw,H-120),WHT)
    f=fit(h,cardw-24,H-150); card.paste(f,((cardw-f.width)//2,(H-120-f.height)//2)); img.paste(card,(W-cardw-40,70))
    return img,d
def strike(d,x,y,text,font,col):
    d.text((x,y),text,font=font,fill=col); w=d.textlength(text,font=font); b=font.getbbox(text)
    ym=y+(b[1]+b[3])//2; d.line([x-6,ym+6,x+w+6,ym-6],fill=(255,70,70),width=7); return w
def pill(d,x,y,text,font):
    w=d.textlength(text,font=font); d.rounded_rectangle([x,y,x+w+36,y+font.size+22],radius=12,fill=YEL); d.text((x+18,y+8),text,font=font,fill=BLK)
def tag(d,x,y,text): d.text((x,y),text,font=F(PB,26),fill=YEL)
def upg_offer(out):
    img,d=canvas(R+'library_upgrade_listing.png'); X=50
    tag(d,X,44,'PLANNER OWNERS ONLY')
    d.text((X,84),'FINISH THE',font=F(A,104),fill=WHT); d.text((X,196),'SYSTEM.',font=F(A,104),fill=YEL)
    w=strike(d,X,352,'$104',F(A,60),GRY); d.text((X+w+36,318),'$83',font=F(A,124),fill=YEL)
    d.text((X,478),'5 books. You save $21. The Manual comes free.',font=F(PB,27),fill=WHT)
    pill(d,X,534,'PRICE ENDS SUN NOV 22',F(PB,26)); img.save(out)
def upg_last(out):
    img,d=canvas(R+'library_upgrade_listing.png'); X=50
    tag(d,X,44,'PLANNER OWNERS: LAST CALL')
    d.text((X,84),'ENDS',font=F(A,120),fill=WHT); d.text((X,214),'SUNDAY.',font=F(A,120),fill=YEL)
    w=strike(d,X,372,'$104',F(A,52),GRY); d.text((X+w+34,350),'$83',font=F(A,100),fill=YEL)
    d.text((X,490),'Midnight Mountain. Then the Upgrade is gone.',font=F(PB,27),fill=WHT)
    pill(d,X,544,'5 BOOKS. SAVE $21. MANUAL FREE.',F(PB,24)); img.save(out)
def bf_teaser(out):
    img,d=canvas(R+'library_hero_noprice.png'); X=50
    tag(d,X,44,'STARTS FRIDAY NOV 27')
    d.text((X,84),'25% OFF',font=F(A,150),fill=YEL); d.text((X,244),'EVERY BUNDLE.',font=F(A,92),fill=WHT)
    d.text((X,372),'Starter. Library. Offgrid Set.',font=F(PB,30),fill=WHT)
    d.text((X,420),'Four days. Nothing else is on sale.',font=F(PB,26),fill=(210,210,210))
    pill(d,X,500,'CODE: STAYREADY25',F(PB,30)); img.save(out)
def bf_launch(out):
    img,d=canvas(R+'library_hero_noprice.png',cardw=340); X=50
    tag(d,X,40,'BLACK FRIDAY IS OPEN. CODE: STAYREADY25')
    d.text((X,78),'25% OFF BUNDLES',font=F(A,86),fill=YEL)
    rows=[('STARTER','$67','$50.25'),('LIBRARY','$127','$95.25'),('OFFGRID SET','$57','$42.75')]
    y=190
    for n,old,new in rows:
        d.text((X,y+14),n,font=F(PB,30),fill=WHT); strike(d,X+300,y+10,old,F(A,46),GRY); d.text((X+420,y-2),new,font=F(A,76),fill=YEL); y+=108
    d.text((X,y+14),'Ends Mon Nov 30, midnight Mountain.',font=F(PB,26),fill=(210,210,210)); img.save(out)
def bf_last(out):
    img,d=canvas(R+'starter_hero_noprice.png'); X=50
    tag(d,X,44,'LAST CALL')
    d.text((X,84),'TONIGHT',font=F(A,130),fill=WHT); d.text((X,226),'25% OFF',font=F(A,130),fill=YEL)
    d.text((X,380),'Every bundle. Ends midnight Mountain.',font=F(PB,29),fill=WHT)
    d.text((X,428),'Tomorrow it is back to regular price.',font=F(PB,26),fill=(210,210,210))
    pill(d,X,500,'CODE: STAYREADY25',F(PB,30)); img.save(out)
O='/home/claude/oghf-fix/out/bf/'
for n,f in [('upg_offer',upg_offer),('upg_lastcall',upg_last),('bf_teaser',bf_teaser),('bf_launch',bf_launch),('bf_lastcall',bf_last)]: f(O+n+'_v2_email.png')
