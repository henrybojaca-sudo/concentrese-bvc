import streamlit as st
import streamlit.components.v1 as components
import base64, os

st.set_page_config(page_title="Concentrese BVC", page_icon="BVC", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:#d6eef7;}
[data-testid="stHeader"]{display:none;}
[data-testid="stToolbar"]{display:none;}
.block-container{padding:0!important;max-width:100%!important;}
</style>
""", unsafe_allow_html=True)

COMPANIES = [
    {"n":"Ecopetrol",   "t":"ECOPETROL",   "c":"#003087", "f":"ecopetrol.png"},
    {"n":"Bancolombia", "t":"BCOLOMBIA",   "c":"#FFCC00", "f":"bancolombia.png"},
    {"n":"Nutresa",     "t":"NUTRESA",     "c":"#E30613", "f":"nutresa.png"},
    {"n":"Promigas",    "t":"PROMIGAS",    "c":"#0070B8", "f":"promigas.png"},
    {"n":"Terpel",      "t":"TERPEL",      "c":"#DA291C", "f":"terpel.png"},
    {"n":"Grupo Aval",  "t":"PFAVAL",      "c":"#003087", "f":"grupoaval.png"},
    {"n":"Davivienda",  "t":"PFDAVVNDA",   "c":"#C8102E", "f":"davivienda.png"},
    {"n":"Argos",       "t":"CEMARGOS",    "c":"#A8C50A", "f":"argos.png"},
    {"n":"Celsia",      "t":"CELSIA",      "c":"#00A550", "f":"celsia.png"},
    {"n":"Grupo Argos", "t":"GRUPOARGOS",  "c":"#003057", "f":"grupoargos.png"},
    {"n":"Corficolomb", "t":"CORFICOLCF",  "c":"#6B2D8B", "f":"corficolombiana.png"},
    {"n":"ETB",         "t":"ETB",         "c":"#E3001B", "f":"etb.png"},
]

LOGOS_DIR = os.path.join(os.path.dirname(__file__), "logos")

@st.cache_data(show_spinner="Cargando logos...")
def load_logos():
    result = []
    for c in COMPANIES:
        path = os.path.join(LOGOS_DIR, c["f"])
        try:
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            img = "data:image/png;base64," + b64
        except:
            img = ""
        result.append({**c, "img": img})
    return result

companies = load_logos()

js_companies = "["
for c in companies:
    js_companies += '{n:"' + c["n"] + '",t:"' + c["t"] + '",c:"' + c["c"] + '",l:"' + c["img"] + '"},'
js_companies += "]"

GAME_HTML = ("""
<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI',Arial,sans-serif;background:#d6eef7;min-height:100vh;padding:16px;}
.header{text-align:center;margin-bottom:14px;}
.header h1{font-size:1.8rem;font-weight:900;color:#005f8e;letter-spacing:2px;margin-bottom:2px;}
.header p{color:#4a8fb0;font-size:0.85rem;}
.stats{display:flex;justify-content:center;gap:10px;margin-bottom:14px;flex-wrap:wrap;}
.stat{background:white;border:2px solid #00aeef;border-radius:10px;padding:8px 18px;text-align:center;min-width:90px;box-shadow:0 2px 8px rgba(0,174,239,0.15);}
.stat-val{font-size:1.4rem;font-weight:800;color:#005f8e;}
.stat-lbl{font-size:0.6rem;color:#4a8fb0;text-transform:uppercase;letter-spacing:1px;}
.grid{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;max-width:840px;margin:0 auto 16px;}
.card{aspect-ratio:3/4;perspective:900px;cursor:pointer;}
.card-inner{width:100%;height:100%;position:relative;transform-style:preserve-3d;transition:transform 0.5s cubic-bezier(0.4,0,0.2,1);}
.card.flipped .card-inner,.card.matched .card-inner{transform:rotateY(180deg);}
.card-front,.card-back{position:absolute;inset:0;border-radius:10px;backface-visibility:hidden;-webkit-backface-visibility:hidden;}
.card-back{background:#00aeef;box-shadow:0 3px 10px rgba(0,100,150,0.25);overflow:hidden;border:2px solid #0090cc;display:flex;align-items:center;justify-content:center;}
.card-back::before{content:'';position:absolute;inset:0;background-image:linear-gradient(45deg,rgba(255,255,255,0.18) 25%,transparent 25%),linear-gradient(-45deg,rgba(255,255,255,0.18) 25%,transparent 25%),linear-gradient(45deg,transparent 75%,rgba(255,255,255,0.18) 75%),linear-gradient(-45deg,transparent 75%,rgba(255,255,255,0.18) 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0;}
.card-back .diamond{position:relative;z-index:1;width:44%;aspect-ratio:1;background:rgba(255,255,255,0.25);transform:rotate(45deg);border:3px solid rgba(255,255,255,0.7);border-radius:4px;}
.card:hover .card-back{border-color:#FFD700;box-shadow:0 6px 18px rgba(0,100,150,0.4);}
.card-front{transform:rotateY(180deg);border:3px solid #00aeef;box-shadow:0 3px 10px rgba(0,174,239,0.2);overflow:hidden;display:flex;align-items:center;justify-content:center;}
.card.matched .card-front{border-color:#27ae60;box-shadow:0 3px 14px rgba(39,174,96,0.35);}
.card-front img{width:100%;height:100%;object-fit:cover;}
.card-front .fallback{width:100%;height:100%;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:800;font-size:0.85rem;color:white;padding:8px;line-height:1.3;}
.win-screen{display:none;text-align:center;background:white;border:3px solid #00aeef;border-radius:14px;padding:20px;max-width:440px;margin:0 auto 14px;box-shadow:0 4px 20px rgba(0,174,239,0.2);}
.win-screen.show{display:block;}
.win-screen h2{color:#005f8e;font-size:1.5rem;margin-bottom:6px;}
.win-screen p{color:#333;}
.btn{display:block;margin:0 auto;padding:11px 34px;background:linear-gradient(135deg,#00aeef,#0085c3);color:white;border:none;border-radius:10px;font-size:0.95rem;font-weight:800;cursor:pointer;letter-spacing:1px;box-shadow:0 4px 12px rgba(0,133,195,0.4);}
.btn:hover{transform:translateY(-2px);}
@keyframes fall{to{transform:translateY(110vh) rotate(720deg);opacity:0;}}
.cp{position:fixed;top:-10px;width:10px;height:10px;border-radius:2px;animation:fall linear forwards;pointer-events:none;z-index:9999;}
@media(max-width:600px){.grid{grid-template-columns:repeat(4,1fr);gap:5px;}}
</style></head><body>
<div class="header">
  <h1>CONCENTRESE BVC</h1>
  <p>Encuentra las 12 parejas &mdash; Bolsa de Valores de Colombia</p>
</div>
<div class="stats">
  <div class="stat"><div class="stat-val" id="s-time">0s</div><div class="stat-lbl">Tiempo</div></div>
  <div class="stat"><div class="stat-val" id="s-moves">0</div><div class="stat-lbl">Movimientos</div></div>
  <div class="stat"><div class="stat-val" id="s-pairs">0/12</div><div class="stat-lbl">Parejas</div></div>
  <div class="stat"><div class="stat-val" id="s-left">12</div><div class="stat-lbl">Por encontrar</div></div>
</div>
<div class="win-screen" id="win"><h2>&#127881; Felicitaciones!</h2><p id="win-msg"></p></div>
<div class="grid" id="grid"></div>
<button class="btn" onclick="newGame()">&#128260; Nueva partida</button>
<script>
const C=""" + js_companies + """;
let cards=[],flipped=[],matched=new Set(),moves=0,startTime=null,tmr=null,locked=false;
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function newGame(){
  clearInterval(tmr);flipped=[];matched=new Set();moves=0;locked=false;startTime=Date.now();
  document.getElementById("win").classList.remove("show");
  document.getElementById("s-moves").textContent="0";
  document.getElementById("s-pairs").textContent="0/12";
  document.getElementById("s-left").textContent="12";
  document.getElementById("s-time").textContent="0s";
  cards=shuffle(C.flatMap((c,i)=>[{...c,id:i*2,ci:i},{...c,id:i*2+1,ci:i}]));
  renderGrid();
  tmr=setInterval(()=>{if(matched.size<C.length)document.getElementById("s-time").textContent=Math.floor((Date.now()-startTime)/1000)+"s";},1000);
}
function renderGrid(){
  const g=document.getElementById("grid");g.innerHTML="";
  cards.forEach(card=>{
    const el=document.createElement("div");el.className="card";
    const front = card.l
      ? '<img src="'+card.l+'" alt="'+card.n+'">'
      : '<div class="fallback" style="background:'+card.c+'">'+card.n+'</div>';
    el.innerHTML='<div class="card-inner"><div class="card-back"><div class="diamond"></div></div><div class="card-front" style="background:'+card.c+'">'+front+'</div></div>';
    el.addEventListener("click",()=>flip(card,el));
    g.appendChild(el);
  });
}
function flip(card,el){
  if(locked||flipped.length===2)return;
  if(flipped.find(f=>f.id===card.id))return;
  if(matched.has(card.ci))return;
  el.classList.add("flipped");flipped.push({card,el});
  if(flipped.length===2){
    moves++;document.getElementById("s-moves").textContent=moves;locked=true;
    if(flipped[0].card.ci===flipped[1].card.ci){
      matched.add(flipped[0].card.ci);
      flipped.forEach(f=>f.el.classList.add("matched"));
      const p=matched.size;
      document.getElementById("s-pairs").textContent=p+"/12";
      document.getElementById("s-left").textContent=12-p;
      flipped=[];locked=false;
      if(p===C.length)endGame();
    }else{
      setTimeout(()=>{flipped.forEach(f=>f.el.classList.remove("flipped"));flipped=[];locked=false;},1000);
    }
  }
}
function endGame(){
  clearInterval(tmr);
  const s=Math.floor((Date.now()-startTime)/1000);
  document.getElementById("s-time").textContent=s+"s";
  document.getElementById("win-msg").textContent="Completaste en "+moves+" movimientos y "+s+" segundos.";
  document.getElementById("win").classList.add("show");
  const cols=["#00aeef","#005f8e","#27ae60","#f39c12","#e74c3c","#fff"];
  for(let i=0;i<80;i++){const c=document.createElement("div");c.className="cp";c.style.cssText="left:"+Math.random()*100+"vw;background:"+cols[i%cols.length]+";animation-duration:"+(2+Math.random()*2)+"s;animation-delay:"+Math.random()*0.5+"s;";document.body.appendChild(c);setTimeout(()=>c.remove(),4000);}
}
newGame();
</script></body></html>
""")

components.html(GAME_HTML, height=1100, scrolling=True)
