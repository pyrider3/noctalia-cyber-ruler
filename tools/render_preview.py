"""Generate native-renderer previews from synthetic workspace data."""
import io,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from ruler import Ruler

def demo():
    result=[]
    for idx,count in enumerate([2,4,3],1):
        cols=[dict(key=[0,j+1],floating=False,windows=[dict(id=idx*100+j,app='DEMO',row=1)]) for j in range(count)]
        if idx==2:
            cols[2]['windows'].append(dict(id=250,app='DEMO',row=2))
            cols.append(dict(key=[1,260],floating=True,windows=[dict(id=260,app='DEMO',row=0)]))
        result.append(dict(id=idx,idx=idx,is_active=idx==2,count=sum(len(c['windows']) for c in cols),app='DEMO',focused_window=idx*100+1,columns=cols))
    return result

def png(r,now):
    b=io.BytesIO();r.paint(now).write_to_png(b);return Image.open(b).convert('RGBA')

def main():
    folder=ROOT/'docs';folder.mkdir(exist_ok=True)
    sheet=Image.new('RGB',(720,540),'#10111c');draw=ImageDraw.Draw(sheet)
    try:font=ImageFont.truetype('DejaVuSans.ttf',19)
    except OSError:font=ImageFont.load_default()
    for i,(theme,label) in enumerate([('classic','Classic Cyber'),('aviation','Aviation HUD'),('islands','Window Islands'),('filmstrip','Desktop Filmstrip')]):
        r=Ruler();r.configure(dict(theme=theme));r.set_workspaces(demo(),0)
        draw.text((30,i*130+14),label,font=font,fill='#bac8dc');image=png(r,0);sheet.paste(image,(60,i*130+45),image)
    sheet.save(folder/'themes.png')
    frames=[];r=Ruler();r.configure(dict(theme='aviation'));ws=demo()
    for frame in range(100):
        if frame==18:ws[1]['focused_window']=203
        if frame==45:ws[1]['is_active']=False;ws[2]['is_active']=True
        now=frame/40;r.set_workspaces(ws,now);image=png(r,now)
        canvas=Image.new('RGB',(640,120),'#10111c');canvas.paste(image,(20,18),image);frames.append(canvas)
    frames[0].save(folder/'aviation.gif',save_all=True,append_images=frames[1:],duration=25,loop=0)
if __name__=='__main__':main()
