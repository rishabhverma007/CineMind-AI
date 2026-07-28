import streamlit as st


def inject_styles() -> None:
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@500;600;700;800&display=swap');
    :root { --red:#E50914; --violet:#7C3AED; --cyan:#06B6D4; --bg:#09090B; --text:#F8FAFC; --muted:#94A3B8; }
    .stApp { background: radial-gradient(circle at 10% 5%, #21113b 0, transparent 26%), radial-gradient(circle at 90% 0%, #092d3e 0, transparent 28%), #09090B; color:var(--text); font-family:Inter,sans-serif; }
    #MainMenu, footer, header {visibility:hidden;} .block-container {max-width:1400px; padding:1.7rem 3.2rem 3rem;}
    [data-testid='stSidebar'] {background:linear-gradient(180deg,rgba(20,20,27,.93),rgba(9,9,11,.97)); border-right:1px solid rgba(255,255,255,.08)}
    [data-testid='stSidebar'] .stRadio label {padding:7px 10px; border-radius:10px;} [data-testid='stSidebar'] .stRadio label:hover {background:rgba(255,255,255,.08)}
    h1,h2,h3 {font-family:Poppins,sans-serif!important; letter-spacing:-.03em;} h1 {font-size:3rem!important;}
    .eyebrow {color:#67e8f9; font-size:.76rem; letter-spacing:.14em; font-weight:800; text-transform:uppercase;}
    .hero {padding:3.5rem; min-height:310px; border:1px solid rgba(255,255,255,.13); border-radius:28px; background:linear-gradient(100deg,rgba(9,9,11,.88) 24%,rgba(9,9,11,.2)), var(--hero); background-size:cover; background-position:center; box-shadow:0 25px 60px rgba(0,0,0,.35);}
    .glass {background:rgba(255,255,255,.065); border:1px solid rgba(255,255,255,.12); border-radius:20px; padding:1.2rem; backdrop-filter:blur(16px);}
    .metric {font-size:1.65rem;font-weight:800;color:#fff}.muted{color:var(--muted)}
    .movie-card {height:100%; overflow:hidden; border-radius:17px; border:1px solid rgba(255,255,255,.12); background:rgba(255,255,255,.055); transition:transform .2s,box-shadow .2s;}.movie-card:hover{transform:translateY(-5px);box-shadow:0 18px 35px rgba(0,0,0,.35)}
    .movie-card img{width:100%;height:270px;object-fit:cover;display:block}.movie-copy{padding:.8rem .9rem 1rem}.movie-title{font-weight:750;font-size:.98rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.badge{font-size:.72rem;color:#fcd34d}.tag{display:inline-block;background:rgba(124,58,237,.2);color:#ddd6fe;border-radius:999px;padding:3px 8px;font-size:.68rem;margin:5px 3px 0 0}
    .stButton>button {border:0;border-radius:11px;background:linear-gradient(100deg,var(--red),#b91c1c);color:white;font-weight:700;transition:.2s}.stButton>button:hover{transform:translateY(-1px);box-shadow:0 8px 18px rgba(229,9,20,.25)}
    .stTextInput input,.stSelectbox div[data-baseweb='select']>div {background:rgba(255,255,255,.07)!important;border-color:rgba(255,255,255,.15)!important;border-radius:12px!important;color:white!important}
    .section {margin-top:2.25rem;margin-bottom:.85rem}.detail-poster{border-radius:18px;width:100%;box-shadow:0 18px 38px rgba(0,0,0,.4)}
    @media(max-width:700px){.block-container{padding:1rem}.hero{padding:1.5rem;min-height:260px}h1{font-size:2.1rem!important}.movie-card img{height:210px}}
    </style>""", unsafe_allow_html=True)
