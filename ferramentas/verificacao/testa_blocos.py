#!/usr/bin/env python3
"""Testa os blocos da lib/ com todas as combinacoes de entrada, contra a especificacao do projeto.
Uso: 1) no Quartus, rode converter.tcl (gera saida/<bloco>.v); 2) python3 testa_blocos.py
Precisa do Icarus Verilog (iverilog e vvp) no PATH."""
import subprocess, os, sys
import tempfile
W=os.path.dirname(os.path.abspath(__file__)); V=os.environ.get('VDIR', os.path.join(W,'saida')); TB=tempfile.mkdtemp(prefix='tb_')
def run(name, files, body, n):
    tb=f'module tb; reg [{n-1}:0] x; integer i;\n{body}\ninitial begin for(i=0;i<{2**n};i=i+1) begin x=i; #1; $display("%0d %b", i, y); end end endmodule\n'
    p=f'{TB}/{name}_tb.v'; open(p,'w').write(tb); exe=f'{TB}/{name}.vvp'
    r=subprocess.run(['iverilog','-g2005','-o',exe,p]+[f'{V}/{f}.v' for f in files],capture_output=True,text=True)
    if r.returncode: return None, r.stderr
    out=subprocess.run(['vvp','-n',exe],capture_output=True,text=True).stdout
    rows={}
    for l in out.splitlines():
        q=l.split()
        if len(q)==2 and q[0].isdigit(): rows[int(q[0])]=q[1]
    return rows, None
SEG='abcdefg'
DIG={'0':['abcdef'],'1':['bc'],'2':['abdeg'],'3':['abcdg'],'4':['bcfg'],'5':['acdfg'],'6':['acdefg','cdefg'],'7':['abc','abcf'],'8':['abcdefg'],'9':['abcdfg','abcfg'],' ':['']}
def seg2dig(bits):  # bits: string a..g active low
    lit=''.join(s for s,b in zip(SEG,bits) if b=='0')
    for d,vs in DIG.items():
        if lit in vs: return d
    return '?'+lit
results={}
def report(name, fails, total, extra=''):
    results[name]=(fails,total)
    print(f'{"OK  " if not fails else "FALHA"} {name}: {total-len(fails)}/{total} {extra}')
    for f in fails[:12]: print('      ',f)
def sm(v,bits=5):  # sinal-magnitude -> int
    s=v>>(bits-1); m=v&((1<<(bits-1))-1); return -m if s else m
def c2(v,bits): return v-(1<<bits) if v>>(bits-1) else v

# ---- mux2x1: y = S ? B : A
rows,e=run('mux2x1',['mux2x1'],'wire y; mux2x1 u(.A(x[0]),.B(x[1]),.S(x[2]),.Y(y));',3)
if e: print(e)
else: report('mux2x1',[i for i in rows if int(rows[i])!=((i>>1)&1 if (i>>2)&1 else i&1)],8)
# ---- mux4x1
rows,e=run('mux4x1',['mux4x1'],'wire y; mux4x1 u(.I(x[3:0]),.S(x[5:4]),.yi(y));',6)
report('mux4x1',[i for i in rows if int(rows[i])!=((i>>(i>>4))&1)],64)
# ---- inversor (4 bits) F = C2 de I
rows,e=run('inversor',['inversor'],'wire [3:0] y; inversor u(.I0(x[0]),.I1(x[1]),.I2(x[2]),.I3(x[3]),.F0(y[0]),.F1(y[1]),.F2(y[2]),.F3(y[3]));',4)
report('inversor',[(i,rows[i]) for i in rows if int(rows[i],2)!=(-i)&15],16)
# ---- inversor5
rows,e=run('inversor5',['inversor5'],'wire [4:0] y; inversor5 u(.I(x),.O(y));',5)
report('inversor5',[(i,rows[i]) for i in rows if int(rows[i],2)!=(-i)&31],32)
# ---- comp2: SM (IS, I[3..0]) -> C2 5 bits {OS,O}; -0 -> +0
rows,e=run('comp2',['comp2','inversor','mux2x1'],'wire [4:0] y; comp2 u(.I(x[3:0]),.IS(x[4]),.O(y[3:0]),.OS(y[4]));',5)
report('comp2',[(i,rows[i]) for i in rows if int(rows[i],2)!=(sm(i)&31)],32)
# ---- somador_completo
rows,e=run('somador_completo',['somador_completo'],'wire [1:0] y; somador_completo u(.A(x[0]),.B(x[1]),.Cin(x[2]),.S(y[0]),.Cout(y[1]));',3)
report('somador_completo',[(i,rows[i]) for i in rows if int(rows[i],2)!=bin(i).count('1')],8)
# ---- somador6: A,B C2 5 bits -> O C2 6 bits
rows,e=run('somador6',['somador6','somador_completo'],'wire [5:0] y; somador6 u(.A(x[4:0]),.B(x[9:5]),.O(y));',10)
report('somador6',[(c2(i&31,5),c2(i>>5,5),rows[i]) for i in rows if c2(int(rows[i],2),6)!=c2(i&31,5)+c2(i>>5,5)],1024)
# ---- c2_para_sm: I C2 6 bits (|v|<=30) -> SM 6 bits
rows,e=run('c2_para_sm',['c2_para_sm','inversor5','mux2x1'],'wire [5:0] y; c2_para_sm u(.I(x),.O(y));',6)
f=[]
for i in rows:
    v=c2(i,6)
    if abs(v)>30: continue
    exp=(32|(-v)) if v<0 else v
    if int(rows[i],2)!=exp: f.append((v,rows[i]))
report('c2_para_sm',f,61,'(valores -30..+30)')
# ---- somador_subtrator: SM A,B, op -> R em sinal-magnitude (R[5] = sinal, |R| <= 30; zero sai +0)
rows,e=run('somador_subtrator',['somador_subtrator','comp2','inversor','mux2x1','somador6','somador_completo','c2_para_sm','inversor5'],
 'wire [5:0] y; somador_subtrator u(.W(x[3:0]),.sinal_a(x[4]),.X(x[8:5]),.sinal_b(x[9]),.sinal_op(x[10]),.R(y));',11)
if e: print(e)
f=[]
for i in rows:
    a=sm(i&31); b=sm((i>>5)&31); op=i>>10; v=a-b if op else a+b
    exp=(32|(-v)) if v<0 else v
    if int(rows[i],2)!=exp: f.append((a,'-' if op else '+',b,rows[i]))
report('somador_subtrator (saida SM)',f,2048)
# ---- op_and / op_xor: F[5]=sinal, F[4]=0, F[3..0]
for nm,fn,sfn in (('op_and',lambda a,b:a&b,lambda a,b:a&b),('op_xor',lambda a,b:a^b,lambda a,b:a^b)):
    rows,e=run(nm,[nm],f'wire [5:0] y; {nm} u(.A(x[3:0]),.SA(x[4]),.B(x[8:5]),.SB(x[9]),.F(y));',10)
    f=[]
    for i in rows:
        A=i&15; SA=(i>>4)&1; B=(i>>5)&15; SB=(i>>9)&1
        exp=(sfn(SA,SB)<<5)|fn(A,B)
        if int(rows[i],2)!=exp: f.append((i,rows[i],format(exp,'06b')))
    report(nm,f,1024)
# ---- comparador_igual (+0 = -0)
rows,e=run('comparador_igual',['comparador_igual'],'wire y; comparador_igual u(.A(x[4:0]),.B(x[9:5]),.F(y));',10)
report('comparador_igual',[(sm(i&31),sm(i>>5),rows[i]) for i in rows if int(rows[i])!=(sm(i&31)==sm(i>>5))],1024)
# ---- comp_mag |A|>|B|
rows,e=run('comp_mag',['comp_mag'],'wire y; comp_mag u(.A(x[3:0]),.B(x[7:4]),.O(y));',8)
report('comp_mag',[(i&15,i>>4,rows[i]) for i in rows if int(rows[i])!=((i&15)>(i>>4))],256)
# ---- comp_maior A>B SM
rows,e=run('comp_maior',['comp_maior','comp_mag'],'wire y; comp_maior u(.A(x[3:0]),.SA(x[4]),.B(x[8:5]),.SB(x[9]),.O(y));',10)
report('comp_maior',[(sm(i&31),sm(i>>5),rows[i]) for i in rows if int(rows[i])!=(sm(i&31)>sm(i>>5))],1024)
# ---- decodificadores + mux_comparadores -> STATUS (S[2..0]; EQ,GT,LT)
rows,e=run('status',['decodificador_comparadores','mux_comparadores'],
 'wire f1,f2,y; decodificador_comparadores d(.S3(x[2]),.S2(x[1]),.S1(x[0]),.F1(f1),.F2(f2)); mux_comparadores m(.F2(f2),.F1(f1),.compIgual(x[3]),.compMaior(x[4]),.compMenor(x[5]),.STATUS(y));',6)
f=[]
for i in rows:
    s=i&7; eq,gt,lt=(i>>3)&1,(i>>4)&1,(i>>5)&1
    exp={3:eq,4:gt,5:lt}.get(s,0)
    if int(rows[i])!=exp: f.append((format(s,'03b'),eq,gt,lt,rows[i]))
report('decodificador_comparadores+mux_comparadores',f,64)
# ---- decodificador_saida: S -> seletor (F1=sel[1], F2=sel[0])
rows,e=run('decodificador_saida',['decodificador_saida'],'wire [1:0] y; decodificador_saida u(.S3(x[2]),.S2(x[1]),.S1(x[0]),.F1(y[1]),.F2(y[0]));',3)
need={0:0,1:0,2:1,6:2,7:3}
report('decodificador_saida',[(format(i,'03b'),rows[i]) for i in rows if i in need and int(rows[i],2)!=need[i]],5,'(so 000,001,010,110,111 importam)')
# ---- displays
def disp(name, files, body, n, fn, rng):
    rows,e=run(name,files,body,n)
    if e: print(name,e); return
    f=[]; tab=[]
    for i in rng:
        d=seg2dig(rows[i]); tab.append(d)
        ok=fn(i,d)
        if not ok: f.append((i,rows[i],d))
    report(name,f,len(rng),' mostra: '+''.join(x if len(x)==1 else '?' for x in tab))
D=lambda i,d,exp: d==exp
disp('decod7seg_ab_dezena',['decod7seg_ab_dezena'],'wire [6:0] y; decod7seg_ab_dezena u(.A(x[3]),.B(x[2]),.C(x[1]),.D(x[0]),.seg_a(y[6]),.seg_b(y[5]),.seg_c(y[4]),.seg_d(y[3]),.seg_e(y[2]),.seg_f(y[1]),.seg_g(y[0]));',4,lambda i,d: d==str(i//10) or (i<10 and d==' '),range(16))
disp('decod7seg_ab_unidade',['decod7seg_ab_unidade'],'wire [6:0] y; decod7seg_ab_unidade u(.A(x[3]),.B(x[2]),.C(x[1]),.D(x[0]),.au_seg(y[6]),.bu_seg(y[5]),.cu_seg(y[4]),.du_seg(y[3]),.eu_seg(y[2]),.fu_seg(y[1]),.gu_seg(y[0]));',4,lambda i,d: d==str(i%10),range(16))
disp('decod7seg_f_dezena',['decod7seg_f_dezena'],'wire [6:0] y; decod7seg_f_dezena u(.R4(x[4]),.R3(x[3]),.R2(x[2]),.R1(x[1]),.R0(x[0]),.aDEZ(y[6]),.bDEZ(y[5]),.cDEZ(y[4]),.dDEZ(y[3]),.eDEZ(y[2]),.fDEZ(y[1]),.gDEZ(y[0]));',5,lambda i,d: d==str(i//10) or (i<10 and d==' '),range(31))
disp('decod7seg_f_unidade',['decod7seg_f_unidade'],'wire [6:0] y; decod7seg_f_unidade u(.R4(x[4]),.R3(x[3]),.R2(x[2]),.R1(x[1]),.R0(x[0]),.aUNI(y[6]),.bUNI(y[5]),.cUNI(y[4]),.dUNI(y[3]),.eUNI(y[2]),.fUNI(y[1]),.gUNI(y[0]));',5,lambda i,d: d==str(i%10),range(31))
rows,e=run('decod7seg_f',['decod7seg_f','decod7seg_f_dezena','decod7seg_f_unidade'],'wire [14:0] y; decod7seg_f u(.S(x[4:0]),.sinal_S(x[5]),.aDEZ(y[13]),.bDEZ(y[12]),.cDEZ(y[11]),.dDEZ(y[10]),.eDEZ(y[9]),.fDEZ(y[8]),.gDEZ(y[7]),.aUNI(y[6]),.bUNI(y[5]),.cUNI(y[4]),.dUNI(y[3]),.eUNI(y[2]),.fUNI(y[1]),.gUNI(y[0]),.led_negativo(y[14]));',6)
if e: print(e)
else:
    f=[]
    for i in rows:
        m=i&31; s=i>>5
        if m>30: continue
        r=rows[i]; dz=seg2dig(r[1:8]); un=seg2dig(r[8:15])
        if not ((dz==str(m//10) or (m<10 and dz==' ')) and un==str(m%10) and int(r[0])==s): f.append((s,m,r,dz,un))
    report('decod7seg_f',f,62)
# ---- mux_saida: 4000 vetores aleatorios
tb='module tb; reg [25:0] x; integer i; wire [5:0] y; mux_saida u(.SOMA_OU_SUB(x[5:0]),.Comp2B(x[11:6]),.OP_AND(x[17:12]),.OP_XOR(x[23:18]),.S(x[25:24]),.F(y));\ninitial begin for(i=0;i<4000;i=i+1) begin x=$random; #1; $display("%0d %b %b", i, x, y); end end endmodule\n'
open(TB+'/mux_saida_tb.v','w').write(tb)
r=subprocess.run(['iverilog','-o',TB+'/ms.vvp',TB+'/mux_saida_tb.v',V+'/mux_saida.v',V+'/mux4x1.v'],capture_output=True,text=True)
if r.returncode: print(r.stderr)
else:
    out=subprocess.run(['vvp','-n',TB+'/ms.vvp'],capture_output=True,text=True).stdout
    f=[];n=0
    for l in out.splitlines():
        q=l.split()
        if len(q)!=3: continue
        n+=1; x=int(q[1],2); sel=x>>24; exp=(x>>(6*sel))&63
        if int(q[2],2)!=exp: f.append((q[1],q[2]))
    report('mux_saida',f,n,'(4000 vetores aleatorios)')
rows,e=run('apaga_display',['apaga_display'],'wire [6:0] y; apaga_display u(.I(x[6:0]),.EN(x[7]),.O(y));',8)
report('apaga_display',[(i,rows[i]) for i in rows if int(rows[i],2)!=((i&127) if i>>7 else 127)],256)

# ---- ula: todas as combinacoes de A, B e S
def tosm6(v): return (32|(-v)) if v<0 else v
mods=[f[:-2] for f in os.listdir(V) if f.endswith('.v')]
tb='''module tb; reg [12:0] x; integer i; wire [5:0] F; wire ST, DE;
ula u(.A(x[4:0]),.B(x[9:5]),.S(x[12:10]),.F(F),.STATUS(ST),.DISP_EN(DE));
initial begin for(i=0;i<8192;i=i+1) begin x=i; #1; $display("%0d %b %b %b", i, F, ST, DE); end end endmodule'''
open(TB+'/ula_tb.v','w').write(tb)
r=subprocess.run(['iverilog','-o',TB+'/ula.vvp',TB+'/ula_tb.v']+[f'{V}/{m}.v' for m in mods],capture_output=True,text=True)

out=subprocess.run(['vvp','-n',TB+'/ula.vvp'],capture_output=True,text=True).stdout
fails={}; n=0
for l in out.splitlines():
    q=l.split()
    if len(q)!=4: continue
    n+=1; i=int(q[0]); A=i&31; B=(i>>5)&31; S=i>>10
    a,b=sm(A),sm(B)
    if S==0: F=tosm6(a+b)
    elif S==1: F=tosm6(a-b)
    elif S==2:
        c=(b & 31)  # C2 de B em 5 bits, estendido: {OS,OS,O[3..0]}
        c5=b & 31; F=((c5>>4)<<5)|c5
    elif S in (3,4,5): F=0
    elif S==6: F=(((A>>4)&(B>>4))<<5)|((A&15)&(B&15))
    else: F=(((A>>4)^(B>>4))<<5)|((A&15)^(B&15))
    ST={3:a==b,4:a>b,5:a<b}.get(S,False)
    DE=S in (0,1)
    got=(int(q[1],2),int(q[2]),int(q[3]))
    exp=(F,int(ST),int(DE))
    if got!=exp: fails.setdefault(S,[]).append((a,b,got,exp))
report('ula (8 operacoes)',[x for v in fails.values() for x in v],n)

print('\nRESUMO:', ', '.join(k for k,(f,t) in results.items() if f) or 'tudo OK')
