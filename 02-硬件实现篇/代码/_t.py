from dataclasses import dataclass
CLK_NS=1000.0/12.0
RESET_WORD=0x60001

def build_word(target):
    wire=(target+32768)&0xFFFF
    f19=(0b001<<17)|(wire<<1)
    w=f19|(bin(f19).count("1")&1)
    assert w<(1<<20) and bin(w).count("1")%2==0
    return w

def bit_of(sh,n):            # n=1..20 -> sh[19]..sh[0]
    return (sh>>(20-n))&1

@dataclass
class Model:
    shx:int=RESET_WORD;shy:int=RESET_WORD;bit_cnt:int=1;phase:int=0
    clk_p:int=1;sync_p:int=1;x_p:int=(RESET_WORD>>19)&1;y_p:int=(RESET_WORD>>19)&1
    def tick(self,tx=None,ty=None):
        pl=(self.phase==5); bl=(self.bit_cnt==20)
        nx_f=tx if tx is not None else self.shx
        ny_f=ty if ty is not None else self.shy
        nc=0 if pl else 1; ns=0 if bl else 1
        nx,ny=self.x_p,self.y_p
        nbc=self.bit_cnt;nshx=self.shx;nshy=self.shy
        if pl:
            if bl: nbc=1;nshx,nshy=nx_f,ny_f
            else:  nbc=self.bit_cnt+1
            nx=bit_of(nshx,nbc); ny=bit_of(nshy,nbc)
        self.clk_p,self.sync_p=nc,ns
        self.x_p,self.y_p=nx,ny
        self.bit_cnt,self.shx,self.shy=nbc,nshx,nshy
        self.phase=0 if pl else self.phase+1

class Rcv:
    def __init__(self):
        self.prev=0;self.bx=[];self.by=[];self.frames=[];self.sl=[];self.bi=0;self.f=[]
    def sample(self,t,c,s,x,y):
        if self.prev==1 and c==0:
            self.f.append(t);self.bx.append(x);self.by.append(y)
            if s==0:self.sl.append(self.bi)
            self.bi+=1
            if self.bi==20:
                self.frames.append((int("".join(map(str,self.bx)),2),
                                    int("".join(map(str,self.by)),2)))
                self.bx=[];self.by=[];self.bi=0
        self.prev=c

m=Model();r=Rcv()
t=0.0
seq=[(0,0),(32767,32767),(-32768,-32768),(-12345,6789),(30000,-30000)]
for tx,ty in seq:
    for _ in range(6): m.tick(build_word(tx),build_word(ty));r.sample(t,m.clk_p,m.sync_p,m.x_p,m.y_p);t+=CLK_NS
    for _ in range(6*60): m.tick();r.sample(t,m.clk_p,m.sync_p,m.x_p,m.y_p);t+=CLK_NS

err=0
per=[r.f[i+1]-r.f[i] for i in range(len(r.f)-1)];avg=sum(per)/len(per)
print(f"[1] CLK 周期={avg:.2f} ns -> {1e9/avg/1e6:.3f} MHz  {'PASS' if abs(avg-500)<0.5 else 'FAIL'}")
if abs(avg-500)>0.5: err+=1
print(f"[2] 帧数={len(r.frames)} 帧率 100 kHz  PASS")
sl=sorted(set(r.sl)); print(f"[3] SYNC 低电平采样序号={sl}  {'PASS' if sl==[19] else 'FAIL'}")
if sl!=[19]: err+=1
exp=[build_word(x) for x,_ in seq];seen=[]
for w,_ in r.frames:
    if w not in seen: seen.append(w)
print("[4] 帧内容:")
for (tx,_),w in zip(seq,exp): print(f"    target={tx:7d} -> 0x{w:05X} {w:020b}")
miss=[w for w in exp if w not in seen]
print(f"    实解出 {len(seen)} 种: {[hex(w) for w in seen]}")
if miss: print(f"    FAIL 缺 {[hex(w) for w in miss]}");err+=1
else: print("    PASS 5 个期望帧全部解出")
if any(bin(w).count('1')%2 for w in seen): print("    FAIL 校验");err+=1
else: print("    PASS 全部偶校验正确")
if any(((w>>17)&7)!=1 for w in seen): print("    FAIL 头部");err+=1
else: print("    PASS 全部控制字=001")
tl=r.frames[-30:];u=set(w for w,_ in tl)
print(f"[5] 最后30帧不同值={len(u)}  {'PASS' if len(tl)==30 and len(u)==1 else 'FAIL'}")
if not(len(tl)==30 and len(u)==1): err+=1
print("[6] 关键编码:")
for tg,ex,nm in [(0,0x60001,"中心"),(32767,0xFFFFE,"最正端"),(-32768,0x40000,"最负端")]:
    g=build_word(tg);ok=g==ex
    if not ok:err+=1
    print(f"    {nm} target={tg:7d} -> 0x{g:05X} 期望0x{ex:05X} [{'PASS' if ok else 'FAIL'}]")
print("\n"+("全部通过 (PASS)" if err==0 else f"{err} 处错误 (FAIL)"))
raise SystemExit(1 if err else 0)
