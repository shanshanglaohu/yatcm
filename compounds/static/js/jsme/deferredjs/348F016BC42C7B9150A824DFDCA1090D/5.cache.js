$wnd.jsme.runAsyncCallback5('function LQ(){this.pb=jn("file");this.pb[hd]="gwt-FileUpload"}r(355,336,Nh,LQ);_.Ad=function(a){Yu(this,a)};function MQ(a){var b=$doc.createElement(Hd);mK(qg,b.tagName);this.pb=b;this.b=new VK(this.pb);this.pb[hd]="gwt-HTML";UK(this.b,a,!0);cL(this)}r(359,360,Nh,MQ);function NQ(){Gx();var a=$doc.createElement("textarea");!vt&&(vt=new ut);!tt&&(tt=new st);dw();this.pb=a;this.pb[hd]="gwt-TextArea"}r(399,400,Nh,NQ);\nfunction OQ(a,b){var c,d;c=$doc.createElement(Qg);d=$doc.createElement(Ag);d[Bc]=a.a.a;d.style[Wg]=a.b.a;var e=(xt(),yt(d));c.appendChild(e);wt(a.d,c);jv(a,b,d)}function SQ(){lw.call(this);this.a=(pw(),ww);this.b=(xw(),Aw);this.e[Xc]=$a;this.e[Wc]=$a}r(408,352,Vh,SQ);_.Vd=function(a){var b;b=ln(a.pb);(a=nv(this,a))&&this.d.removeChild(ln(b));return a};r(414,1,{});_.le=function(a){a.focus()};r(415,416,{});_.le=function(a){Yw(a)};\nfunction TQ(a){try{a.w=!1;var b,c,d,e,f;d=a.hb;c=a.ab;d||(a.pb.style[Xg]=se,a.ab=!1,a.ge());b=a.pb;b.style[Ce]=0+(So(),If);b.style[Ig]=ab;e=~~(tn()-en(a.pb,wf))>>1;f=~~(sn()-en(a.pb,vf))>>1;DM(a,bj(on($doc.body)+e,0),bj(($doc.body.scrollTop||0)+f,0));d||((a.ab=c)?(a.pb.style[ld]=Vf,a.pb.style[Xg]=Yg,Ai(a.gb,200)):a.pb.style[Xg]=Yg)}finally{a.w=!0}}function UQ(a){a.i=(new QL(a.j)).tc.Ye();Uu(a.i,new VQ(a),(Xp(),Xp(),Yp));a.d=F(Tx,q,40,[a.i])}\nfunction WQ(){YM();var a,b,c,d,e;uN.call(this,(MN(),NN),null,!0);this.Wg();this.db=!0;a=new MQ(this.k);this.f=new NQ;this.f.pb.style[$g]=cb;Gu(this.f,cb);this.Ug();PM(this,"400px");e=new SQ;e.pb.style[re]=cb;e.e[Xc]=10;c=(pw(),qw);e.a=c;OQ(e,a);OQ(e,this.f);this.e=new Ew;this.e.e[Xc]=20;for(b=this.d,c=0,d=b.length;c<d;++c)a=b[c],Bw(this.e,a);OQ(e,this.e);cN(this,e);ZL(this,!1);this.Vg()}r(667,668,sI,WQ);_.Ug=function(){UQ(this)};\n_.Vg=function(){var a=this.f;a.pb.readOnly=!0;var b=Ku(a.pb)+"-readonly";Fu(a.Id(),b,!0)};_.Wg=function(){YL(this.I.b,"Copy")};_.d=null;_.e=null;_.f=null;_.i=null;_.j="Close";_.k="Press Ctrl-C (Command-C on Mac) or right click (Option-click on Mac) on the selected text to copy it, then paste into another program.";function VQ(a){this.a=a}r(670,1,{},VQ);_.gd=function(){eN(this.a,!1)};_.a=null;function XQ(a){this.a=a}r(671,1,{},XQ);\n_.Kc=function(){Pu(this.a.f.pb,!0);ew.le(this.a.f.pb);var a=this.a.f,b;b=fn(a.pb,Vg).length;if(0<b&&a.kb){if(0>b)throw new MF("Length must be a positive integer. Length: "+b);if(b>fn(a.pb,Vg).length)throw new MF("From Index: 0  To Index: "+b+"  Text Length: "+fn(a.pb,Vg).length);try{a.pb.setSelectionRange(0,0+b)}catch(c){}}};_.a=null;function YQ(a){UQ(a);a.a=(new QL(a.b)).tc.Ye();Uu(a.a,new ZQ(a),(Xp(),Xp(),Yp));a.d=F(Tx,q,40,[a.a,a.i])}\nfunction $Q(a){a.j="Cancel";a.k="Paste the text to import into the text area below.";a.b="Accept";YL(a.I.b,"Paste")}function aR(a){YM();WQ.call(this);this.c=a}r(673,667,sI,aR);_.Ug=function(){YQ(this)};_.Vg=function(){Gu(this.f,"150px")};_.Wg=function(){$Q(this)};_.ge=function(){tN(this);Vm((Sm(),Tm),new bR(this))};_.a=null;_.b=null;_.c=null;function cR(a){YM();aR.call(this,a)}r(672,673,sI,cR);_.Ug=function(){var a;YQ(this);a=new LQ;Uu(a,new dR(this),(GJ(),GJ(),HJ));this.d=F(Tx,q,40,[this.a,a,this.i])};\n_.Vg=function(){Gu(this.f,"150px");rB(new eR(this),this.f)};_.Wg=function(){$Q(this);this.k+=" Or drag and drop a file on it."};function dR(a){this.a=a}r(674,1,{},dR);_.fd=function(a){var b,c;b=new FileReader;a=(c=qn(a.a),c.files[0]);fR(b,new gR(this));b.readAsText(a)};_.a=null;function gR(a){this.a=a}r(675,1,{},gR);_.hf=function(a){LA();Fx(this.a.a.f,a)};_.a=null;function eR(a){this.a=a;this.b=new hR(this);this.c=this.d=1}r(676,506,{},eR);_.a=null;function hR(a){this.a=a}r(677,1,{},hR);\n_.hf=function(a){this.a.a.f.pb[Vg]=null!=a?a:l};_.a=null;function ZQ(a){this.a=a}r(681,1,{},ZQ);_.gd=function(){if(this.a.c){var a=this.a.c,b;b=new IA(a.a,0,fn(this.a.f.pb,Vg));yB(a.a.a,b.a)}eN(this.a,!1)};_.a=null;function bR(a){this.a=a}r(682,1,{},bR);_.Kc=function(){Pu(this.a.f.pb,!0);ew.le(this.a.f.pb)};_.a=null;r(683,1,Th);_.Zc=function(){var a,b;a=new iR(this.a);void 0!=$wnd.FileReader?b=new cR(a):b=new aR(a);RM(b);TQ(b)};function iR(a){this.a=a}r(684,1,{},iR);_.a=null;r(685,1,Th);\n_.Zc=function(){var a;a=new WQ;var b=this.a,c;Fx(a.f,b);b=(c=RF(b,"\\r\\n|\\r|\\n|\\n\\r"),c.length);Gu(a.f,20*(10>b?b:10)+If);Vm((Sm(),Tm),new XQ(a));RM(a);TQ(a)};function fR(a,b){a.onload=function(a){b.hf(a.target.result)}}V(667);V(673);V(672);V(684);V(670);V(671);V(681);V(682);V(674);V(675);V(676);V(677);V(359);V(408);V(399);V(355);x(qI)(5);\n//@ sourceURL=5.js\n')
