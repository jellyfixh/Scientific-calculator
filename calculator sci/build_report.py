"""Build a Thai project report from the local scientific calculator website."""
import argparse
import os
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, Flowable, KeepTogether)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_OUT = os.path.join(ROOT, 'output', 'pdf', 'scientific-calculator-report.pdf')
FONT_DIR = r'C:\Windows\Fonts'
FONT_REGULAR = os.path.join(FONT_DIR, 'tahoma.ttf')
FONT_BOLD = os.path.join(FONT_DIR, 'tahomabd.ttf')
if not all(os.path.isfile(p) for p in (FONT_REGULAR, FONT_BOLD)):
    raise FileNotFoundError('Tahoma fonts not found in C:\\Windows\\Fonts')
pdfmetrics.registerFont(TTFont('Tahoma', FONT_REGULAR, shapable=True))
pdfmetrics.registerFont(TTFont('Tahoma-Bold', FONT_BOLD, shapable=True))
pdfmetrics.registerFontFamily('Tahoma', normal='Tahoma', bold='Tahoma-Bold', italic='Tahoma', boldItalic='Tahoma-Bold')

INK = HexColor('#403748')
MUTED = HexColor('#8F8493')
PINK = HexColor('#F3A9C8')
PINK_DEEP = HexColor('#D979A3')
PINK_LIGHT = HexColor('#FFF3F8')
LILAC = HexColor('#D9C7F3')
LILAC_LIGHT = HexColor('#F7F2FC')
MINT = HexColor('#C9E9DC')
MINT_LIGHT = HexColor('#F1FAF6')
GOLD = HexColor('#FAE8AF')
LINE = HexColor('#F1E8EF')
PAPER = HexColor('#FFFCFE')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitle', fontName='Tahoma-Bold', fontSize=28, leading=38, textColor=INK, alignment=TA_CENTER, spaceAfter=12))
styles.add(ParagraphStyle(name='CoverSub', fontName='Tahoma', fontSize=12, leading=20, textColor=MUTED, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='CoverEyebrow', fontName='Tahoma-Bold', fontSize=11, leading=16, textColor=PINK_DEEP, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='H1', fontName='Tahoma-Bold', fontSize=18, leading=26, textColor=INK, spaceAfter=8, keepWithNext=True))
styles.add(ParagraphStyle(name='H2', fontName='Tahoma-Bold', fontSize=12.5, leading=18, textColor=HexColor('#8C6EA7'), spaceBefore=7, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name='Body', fontName='Tahoma', fontSize=9.5, leading=16, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name='Small', fontName='Tahoma', fontSize=8, leading=12, textColor=MUTED, spaceAfter=3))
styles.add(ParagraphStyle(name='Table', fontName='Tahoma', fontSize=8.5, leading=13, textColor=INK))
styles.add(ParagraphStyle(name='TableHead', fontName='Tahoma-Bold', fontSize=8.5, leading=13, textColor=INK))
styles.add(ParagraphStyle(name='Callout', fontName='Tahoma', fontSize=9, leading=15, textColor=INK))

def P(text, style='Body'):
    return Paragraph(text, styles[style])

def section(num, title, subtitle=None):
    items = [P(f'<font color="#D979A3">{num}</font>  {title}', 'H1')]
    if subtitle:
        items.append(P(subtitle, 'Small'))
    items.append(HRFlowable(width='100%', thickness=.8, color=LINE, spaceBefore=2, spaceAfter=10))
    return items

def callout(text, fill=PINK_LIGHT, stroke=None):
    t=Table([[P(text,'Callout')]], colWidths=[166*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),fill),('BOX',(0,0),(-1,-1),.7,stroke or fill),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    return t

def grid_table(rows, widths, header=True):
    data=[]
    for i,row in enumerate(rows):
        sty='TableHead' if header and i==0 else 'Table'
        data.append([P(str(v),sty) for v in row])
    t=Table(data,colWidths=widths,repeatRows=1 if header else 0,hAlign='LEFT')
    cmds=[('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.45,LINE),
          ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
          ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]
    if header: cmds += [('BACKGROUND',(0,0),(-1,0),LILAC),('BACKGROUND',(0,1),(-1,-1),PAPER)]
    t.setStyle(TableStyle(cmds));return t

class WebsitePreview(Flowable):
    """A drawn report illustration of the actual calculator page structure."""
    def __init__(self,width=166*mm,height=111*mm): super().__init__();self.width=width;self.height=height
    def draw(self):
        c=self.canv;w=self.width;h=self.height
        c.setFillColor(HexColor('#FFF8FC'));c.roundRect(0,0,w,h,14,fill=1,stroke=0)
        # Display card
        dx=8;dy=h-49;dw=w*.56-12;dh=39
        c.setFillColor(HexColor('#FBF6FC'));c.setStrokeColor(LINE);c.roundRect(dx,dy,dw,dh,9,fill=1,stroke=1)
        c.setFillColor(HexColor('#F1EAFA'));c.roundRect(dx+8,dy+dh-13,34,8,4,fill=1,stroke=0)
        c.setFillColor(HexColor('#8F72B1'));c.setFont('Tahoma-Bold',5.5);c.drawCentredString(dx+25,dy+dh-10,'SCI · DEG')
        c.setFillColor(MUTED);c.setFont('Tahoma',7);c.drawRightString(dx+dw-9,dy+dh-12,'สลับ DEG / RAD')
        c.setFillColor(MUTED);c.setFont('Tahoma',7);c.drawRightString(dx+dw-10,dy+14,'พร้อมคำนวณ')
        c.setFillColor(INK);c.setFont('Tahoma-Bold',17);c.drawRightString(dx+dw-10,dy+3,'0')
        # Calculator keys
        labels=[['2nd','π','e','AC','DEL'],['sin','cos','tan','÷','%'],['ln','log','√','×','xʸ'],['7','8','9','−','('],['4','5','6','+ ',')'],['1','2','3','n!','Ans'],['0','.', '00','=']]
        gap=3;kw=(dw-4*gap)/5;kh=7.7;start_y=dy-7
        for r,row in enumerate(labels):
            yy=start_y-(r+1)*(kh+gap)
            col=0
            for label in row:
                xx=dx+col*(kw+gap)
                kw2=kw*2+gap if r==6 and col==0 else kw
                if label in ('sin','cos','tan','ln','log','√','π','e','n!','Ans'): fill=LILAC_LIGHT
                elif label in ('÷','%','×','−','+ '): fill=PINK_LIGHT
                elif label=='=': fill=PINK
                elif label=='AC': fill=HexColor('#FFF8E8')
                else: fill=HexColor('#FAF7FA')
                c.setFillColor(fill);c.setStrokeColor(LINE);c.roundRect(xx,yy,kw2,kh,3,fill=1,stroke=1)
                c.setFillColor(INK);c.setFont('Tahoma-Bold',6.3);c.drawCentredString(xx+kw2/2,yy+2.5,label.strip())
                col += 2 if r==6 and col==0 else 1
        # Right feature panel, with tabs and cards
        px=w*.59;pw=w-px-8;py=14;ph=h-58
        c.setFillColor(white);c.setStrokeColor(HexColor('#F1E8EF'));c.roundRect(px,py,pw,ph,9,fill=1,stroke=1)
        tabw=(pw-14)/3
        for i,(name,fill) in enumerate([('สถิติ',PINK_LIGHT),('กราฟ',LILAC_LIGHT),('ประวัติ',MINT_LIGHT)]):
            tx=px+5+i*(tabw+2);c.setFillColor(fill if i==0 else HexColor('#F8F2F7'));c.roundRect(tx,py+ph-15,tabw,10,3,fill=1,stroke=0)
            c.setFillColor(INK if i==0 else MUTED);c.setFont('Tahoma',6);c.drawCentredString(tx+tabw/2,py+ph-12,name)
        c.setFillColor(INK);c.setFont('Tahoma-Bold',8);c.drawString(px+7,py+ph-29,'คำนวณสถิติ')
        c.setFillColor(MUTED);c.setFont('Tahoma',5.5);c.drawString(px+7,py+ph-40,'ใส่ตัวเลขคั่นด้วยจุลภาคหรือเว้นวรรค')
        c.setFillColor(HexColor('#FFFAFD'));c.setStrokeColor(LINE);c.roundRect(px+7,py+ph-62,pw-14,17,4,fill=1,stroke=1)
        c.setFillColor(MUTED);c.setFont('Tahoma',5.5);c.drawString(px+11,py+ph-55,'12, 15, 18, 20, 25')
        c.setFillColor(PINK);c.roundRect(px+7,py+ph-77,50,10,3,fill=1,stroke=0)
        c.setFillColor(INK);c.setFont('Tahoma',5.5);c.drawCentredString(px+32,py+ph-74,'คำนวณให้หน่อย')
        cols=2;cw=(pw-20)/2
        for i,(lab,val) in enumerate([('ค่าเฉลี่ย','18'),('มัธยฐาน','18'),('ฐานนิยม','—'),('ส่วนเบี่ยงเบนฯ','4.4')]):
            rr=i//cols;cc=i%cols;xx=px+7+cc*(cw+5);yy=py+ph-99-rr*28
            c.setFillColor(HexColor('#FFFCFE'));c.setStrokeColor(LINE);c.roundRect(xx,yy,cw,23,4,fill=1,stroke=1)
            c.setFillColor(MUTED);c.setFont('Tahoma',5);c.drawString(xx+4,yy+14,lab)
            c.setFillColor(INK);c.setFont('Tahoma-Bold',7);c.drawString(xx+4,yy+4,val)
        c.setFillColor(MUTED);c.setFont('Tahoma',5.5);c.drawString(8,3,'ภาพประกอบจำลองจากโครงหน้าจอและสีในเว็บ')

class OOPMap(Flowable):
    def __init__(self,width=166*mm,height=88*mm): super().__init__();self.width=width;self.height=height
    def draw(self):
        c=self.canv;w=self.width;h=self.height
        def node(x,y,nw,nh,title,body,fill):
            c.setFillColor(fill);c.setStrokeColor(LINE);c.roundRect(x,y,nw,nh,7,fill=1,stroke=1)
            c.setFillColor(INK);c.setFont('Tahoma-Bold',8);c.drawCentredString(x+nw/2,y+nh-14,title)
            p=Paragraph(body,ParagraphStyle('node',fontName='Tahoma',fontSize=7,leading=10,textColor=INK,alignment=TA_CENTER))
            _,ph=p.wrap(nw-12,nh-24);p.drawOn(c,x+6,y+nh-21-ph)
        node(5,h-47,64,38,'ผู้ใช้','กดปุ่ม / กรอกค่า',GOLD)
        node(88,h-47,94,38,'CalculatorView','จัดการหน้าจอและเหตุการณ์',MINT)
        node(202,h-47,94,38,'ExpressionEngine','แปลงและคำนวณนิพจน์',PINK_LIGHT)
        node(320,h-47,100,38,'ผลลัพธ์','ตัวเลข / กราฟ / สถิติ',LILAC_LIGHT)
        for x1,x2 in [(69,88),(182,202),(296,320)]:
            yy=h-28;c.setStrokeColor(PINK_DEEP);c.line(x1,yy,x2,yy);c.line(x2-4,yy+2,x2,yy);c.line(x2-4,yy-2,x2,yy)
        node(53,9,105,37,'StatisticsPanel','อ่านข้อมูลและคำนวณสถิติ',LILAC_LIGHT)
        node(205,9,105,37,'GraphPlotter','ใช้ engine และวาด Canvas',LILAC_LIGHT)
        c.setStrokeColor(HexColor('#A996BD'));c.setDash(3,2);c.line(125,47,105, h-50);c.line(257,47,250,h-50);c.setDash()
        c.setFillColor(MUTED);c.setFont('Tahoma',6);c.drawString(4,0,'ความสัมพันธ์สรุปจากคลาสที่ประกาศจริงใน index.html')

def footer(canvas,doc):
    canvas.saveState();w,h=A4
    if doc.page>1:
        canvas.setStrokeColor(LINE);canvas.line(22*mm,16*mm,w-22*mm,16*mm)
        canvas.setFillColor(MUTED);canvas.setFont('Tahoma',7.5)
        canvas.drawString(22*mm,10.5*mm,'เครื่องคิดเลขวิทยาศาสตร์ | รายงานจากเว็บในโครงการ')
        canvas.drawRightString(w-22*mm,10.5*mm,str(doc.page))
    canvas.restoreState()

def make_story():
    s=[]
    # Cover
    s += [Spacer(1,17*mm),P('รายงานโครงงานเว็บไซต์','CoverEyebrow'),Spacer(1,6*mm),
          P('เครื่องคิดเลข<br/>วิทยาศาสตร์','CoverTitle'),
          P('Scientific Calculator Website<br/>สรุปแนวคิด ฟังก์ชัน และโครงสร้างโปรแกรม','CoverSub'),Spacer(1,12*mm)]
    banner=Table([[P('<b>ผู้จัดทำ</b><br/>Kannicha Arruk','Callout'),P('<b>โปรแกรม</b><br/>HTML · CSS · JavaScript','Callout')]],colWidths=[83*mm,83*mm])
    banner.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),PINK_LIGHT),('BACKGROUND',(1,0),(1,0),MINT_LIGHT),('BOX',(0,0),(-1,-1),.6,LINE),('INNERGRID',(0,0),(-1,-1),.6,LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),11),('BOTTOMPADDING',(0,0),(-1,-1),11)]))
    s += [banner,Spacer(1,10*mm),WebsitePreview(),PageBreak()]
    # Overview and web screen
    s += section('01','เกี่ยวกับเว็บไซต์','สรุปข้อมูลและรูปแบบการใช้งานจากหน้าเว็บเครื่องคิดเลขวิทยาศาสตร์ในโครงการ')
    s += [P('เครื่องคิดเลขวิทยาศาสตร์นี้รวมการคำนวณทั่วไป ฟังก์ชันตรีโกณมิติและลอการิทึม การสรุปสถิติ และการวาดกราฟไว้ในหน้าเดียว ออกแบบให้ใช้งานง่ายบนหน้าจอขนาดต่าง ๆ โดยใช้แผงแสดงผล ปุ่มกด และแท็บแยกหมวดฟังก์ชัน.'),
          P('องค์ประกอบหลักบนหน้าเว็บ','H2'),
          grid_table([['ส่วนของหน้า','หน้าที่'],['แผงแสดงผล','แสดงนิพจน์ คำตอบ และโหมด DEG/RAD'],['แป้นเครื่องคิดเลข','ป้อนตัวเลข ตัวดำเนินการ ค่าคงที่ และฟังก์ชัน'],['แท็บสถิติ','รับชุดข้อมูลแล้วแสดงค่าสถิติสรุป'],['แท็บกราฟ','รับฟังก์ชันและช่วง x เพื่อวาดกราฟ'],['แท็บประวัติ','แสดงรายการคำนวณย้อนหลังและเรียกกลับมาใช้']], [43*mm,123*mm]),Spacer(1,4*mm),
          callout('<b>รูปแบบภาพ</b><br/>ใช้พื้นหลังพาสเทล แผงสีขาวมุมมน และสีชมพู ม่วงอ่อน เขียวอ่อน แยกแป้นตัวเลข ฟังก์ชัน และตัวดำเนินการ ตามหน้าเว็บไซต์',fill=MINT_LIGHT),PageBreak()]
    # Scope
    s += section('02','ขอบเขตและฟังก์ชัน','ความสามารถตามปุ่มและแผงที่มีอยู่ในเว็บ')
    s += [grid_table([['หมวด','ฟังก์ชันในเว็บ'],['คำนวณพื้นฐาน','บวก ลบ คูณ หาร เศษเหลือ ยกกำลัง วงเล็บ และแฟกทอเรียล'],['ฟังก์ชันวิทยาศาสตร์','sin, cos, tan, asin, acos, atan, √, ln, log, abs, floor, ceil'],['ค่าคงที่และโหมด','π, e, Ans และสลับองศา/เรเดียน'],['สถิติ','ค่าเฉลี่ย มัธยฐาน ฐานนิยม ส่วนเบี่ยงเบนมาตรฐาน ค่าต่ำสุด และค่าสูงสุด'],['กราฟ','วาด y=f(x) กำหนดช่วง x และระยะขั้น พร้อมปรับช่วง y อัตโนมัติ'],['ประวัติ','เก็บรายการคำนวณล่าสุดในเบราว์เซอร์และเลือกนิพจน์กลับมาใช้'],['การควบคุม','คลิกปุ่มหรือใช้แป้นพิมพ์ Enter, Backspace และ Escape']], [43*mm,123*mm]),Spacer(1,6*mm),
          P('ขอบเขตข้อมูล','H2'),
          P('ช่องสถิติรับตัวเลขคั่นด้วยจุลภาค เว้นวรรค หรือขึ้นบรรทัดใหม่ ส่วนกราฟรับนิพจน์ที่มี x และช่วงเริ่ม/สิ้นสุด โดยสุ่มประเมินจุดภายในช่วงเพื่อสร้างเส้นกราฟ. '),
          callout('<b>ข้อจำกัดที่ระบุจากโค้ด</b><br/>นิพจน์จำกัดความยาวไม่เกิน 100 ตัวอักษร แฟกทอเรียลรองรับจำนวนเต็ม 0–170 และการวาดกราฟจำกัดจำนวนจุดที่ประเมินเพื่อคุมภาระการคำนวณ',fill=HexColor('#FFF8E8'),stroke=GOLD),PageBreak()]
    # OOP and technical implementation
    s += section('03','โครงสร้างโปรแกรม','คลาสและความรับผิดชอบสรุปจากโค้ด JavaScript จริงใน index.html')
    s += [P('โปรแกรมจัดโครงสร้างด้วยคลาส 4 คลาส โดยแยกตัวประเมินนิพจน์ ออกจากการควบคุมหน้าจอ และแยกการคำนวณสถิติกับการวาดกราฟเป็นคนละส่วน.'),OOPMap(),Spacer(1,3*mm),
          grid_table([['คลาส','ความรับผิดชอบ'],['ExpressionEngine','แปลงนิพจน์และคำนวณตามตัวดำเนินการ ค่าคงที่ และฟังก์ชัน'],['CalculatorView','จัดการการป้อนค่า ปุ่มกด โหมดมุม คำตอบ ประวัติ และการสลับแท็บ'],['StatisticsPanel','อ่านชุดตัวเลข ตรวจข้อมูล และคำนวณค่าสถิติ'],['GraphPlotter','ประเมินฟังก์ชันตามค่า x แล้ววาดเส้นกราฟบน Canvas']], [48*mm,118*mm]),Spacer(1,3*mm),
          callout('<b>แนวคิดเชิงวัตถุ</b><br/>แต่ละคลาสรับผิดชอบงานเฉพาะด้าน และ CalculatorView เชื่อมการทำงานผ่านออบเจ็กต์ ExpressionEngine, StatisticsPanel และ GraphPlotter',fill=LILAC_LIGHT),PageBreak()]
    # Algorithms
    s += section('04','วิธีทำงานของฟังก์ชันหลัก','อธิบายลำดับจากโค้ดและส่วนติดต่อผู้ใช้')
    s += [P('การคำนวณนิพจน์','H2'),
          grid_table([['ลำดับ','การทำงาน'],['1','รับนิพจน์จากปุ่มหรือคีย์บอร์ด แล้วแทนเครื่องหมายคูณ หาร ลบ และรากให้อยู่ในรูปภายใน'],['2','อ่านนิพจน์เป็นส่วนย่อยด้วย parser แบบ recursive descent และจัดการวงเล็บ ค่าคงที่ และฟังก์ชัน'],['3','ประเมินบวก/ลบ คูณ/หาร/เศษเหลือ ยกกำลัง เครื่องหมาย unary และแฟกทอเรียล'],['4','ตรวจผลลัพธ์ว่าคำนวณได้ แล้วแสดงคำตอบและอัปเดต Ans กับประวัติ']], [20*mm,146*mm]),
          P('ค่าสถิติ','H2'),P('เรียงชุดข้อมูลเพื่อหามัธยฐาน นับความถี่เพื่อหาฐานนิยม และคำนวณค่าเฉลี่ยจากผลรวม/จำนวนข้อมูล ส่วนเบี่ยงเบนมาตรฐานในโค้ดใช้ความแปรปรวนแบบประชากร โดยหารด้วยจำนวนข้อมูล n.'),
          P('กราฟและประวัติ','H2'),P('GraphPlotter ประเมินค่าฟังก์ชันหลายจุดตามช่วง x แล้วปรับสเกล y จากค่าที่ได้ ก่อนวาดแกน ตาราง และเส้นโค้งบน HTML Canvas ส่วนประวัติใช้ localStorage คีย์ mali-history และเก็บรายการล่าสุดสูงสุด 30 รายการ.'),
          callout('<b>รูปแบบใช้งาน</b><br/>หน้าเว็บตอบสนองต่อการปรับขนาดหน้าต่าง และเมื่อเปิดแท็บกราฟจะวาดกราฟใหม่ให้สัมพันธ์กับพื้นที่แสดงผล',fill=MINT_LIGHT),PageBreak()]
    # Summary and references
    s += section('05','สรุปและแหล่งข้อมูล')
    s += [P('เว็บไซต์รวมเครื่องมือคำนวณวิทยาศาสตร์หลายหมวดไว้ในหน้าจอเดียว ตั้งแต่การคำนวณนิพจน์ สถิติ ไปจนถึงกราฟ โดยใช้คลาส JavaScript แยกส่วนประมวลผลกับส่วนแสดงผลให้ดูแลได้เป็นระบบ.'),
          P('คุณลักษณะของเว็บ','H2'),P('• ใช้งานผ่านแป้นกดหรือคีย์บอร์ด<br/>• แยกสถิติ กราฟ และประวัติเป็นแท็บ<br/>• เลือก DEG/RAD สำหรับฟังก์ชันตรีโกณมิติ<br/>• ใช้ localStorage เก็บประวัติในเบราว์เซอร์<br/>• ใช้ Mali เป็นแบบอักษรของหน้าเว็บ และใช้สีพาสเทลช่วยจัดกลุ่มส่วนต่าง ๆ'),
          P('แหล่งข้อมูล','H2'),
          P('[1] เว็บเครื่องคิดเลขวิทยาศาสตร์ของโครงการนี้: <b>../index.html</b> (ตรวจโครงสร้างและฟังก์ชันจากซอร์สในโครงการ ณ 2 พฤศจิกายน 2569).','Small'),
          P('[2] เอกสาร PDF ที่ผู้ใช้แนบ ใช้เป็นแนวหัวข้อรายงานเท่านั้น; เนื้อหาและรายละเอียดในฉบับนี้อิงจากเว็บเครื่องคิดเลขวิทยาศาสตร์และซอร์สโค้ดของโครงการ.','Small'),
          Spacer(1,6*mm),callout('<b>จัดทำโดย Kannicha Arruk</b>',fill=PINK_LIGHT)]
    return s

def main():
    parser=argparse.ArgumentParser(description='สร้างรายงาน PDF จากเว็บเครื่องคิดเลขวิทยาศาสตร์')
    parser.add_argument('--output',default=DEFAULT_OUT,help='ตำแหน่งไฟล์ PDF ปลายทาง')
    args=parser.parse_args();out=os.path.abspath(args.output)
    os.makedirs(os.path.dirname(out),exist_ok=True)
    doc=SimpleDocTemplate(out,pagesize=A4,rightMargin=22*mm,leftMargin=22*mm,topMargin=19*mm,bottomMargin=23*mm,
        title='รายงานเว็บไซต์เครื่องคิดเลขวิทยาศาสตร์',author='Kannicha Arruk',subject='รายงานโครงงานเครื่องคิดเลขวิทยาศาสตร์')
    doc.build(make_story(),onFirstPage=footer,onLaterPages=footer)
    print(out)

if __name__=='__main__':
    main()
