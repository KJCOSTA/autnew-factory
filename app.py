import streamlit as st
import time
import pandas as pd
import plotly.express as px

# --- LOG DE VERSÃO ---
VERSION_INFO = "AutNew OS v2.0 | UI/UX Premium | Atualizado: 18/01/2026 - 19h30"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="AutNew Factory",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS AVANÇADO (A MÁGICA VISUAL) ---
st.markdown("""
<style>
    /* 1. FONTES MODERNAS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400&display=swap');

    :root {
        --bg-dark: #0f172a;
        --card-bg: #1e293b;
        --primary: #3b82f6;
        --primary-hover: #2563eb;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --border: #334155;
    }

    /* 2. RESET GERAL */
    .stApp {
        background-color: var(--bg-dark);
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }
    
    /* 3. MENU LATERAL PERSONALIZADO (SEM BOLINHAS) */
    section[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid var(--border);
    }
    
    /* Esconder o estilo padrão do Radio Button */
    .stRadio > label { display: none; }
    div[role="radiogroup"] > label > div:first-child { display: none; }
    
    /* Estilizar as opções do menu como Botões de Navegação */
    div[role="radiogroup"] label {
        background: transparent;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 4px;
        border: 1px solid transparent;
        transition: all 0.2s;
        cursor: pointer;
        color: var(--text-muted);
        font-weight: 500;
    }
    
    div[role="radiogroup"] label:hover {
        background: rgba(59, 130, 246, 0.1);
        color: white;
    }
    
    /* Item Selecionado */
    div[role="radiogroup"] label[data-checked="true"] {
        background: var(--primary);
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        border: none;
    }

    /* 4. CARDS & CONTAINERS */
    .custom-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    /* 5. BOTÕES DE AÇÃO (HIERARQUIA) */
    div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        border: none;
        color: white;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        transition: transform 0.1s;
    }
    div[data-testid="stHorizontalBlock"] button[kind="primary"]:active {
        transform: scale(0.98);
    }

    /* 6. INPUTS MODERNOS */
    input[type="text"], textarea {
        background-color: #020617 !important;
        border: 1px solid var(--border) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    /* 7. TIMELINE DE PROGRESSO */
    .step-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 30px;
        padding: 0 10px;
    }
    .step {
        text-align: center;
        position: relative;
        flex: 1;
        color: var(--text-muted);
        font-size: 0.8rem;
        font-weight: 600;
    }
    .step.active { color: var(--primary); }
    .step.completed { color: #10b981; }
    .step-icon {
        width: 30px; height: 30px;
        background: var(--card-bg);
        border: 2px solid var(--border);
        border-radius: 50%;
        margin: 0 auto 8px;
        display: flex; align-items: center; justify-content: center;
        z-index: 2; position: relative;
    }
    .step.active .step-icon {
        border-color: var(--primary);
        background: rgba(59, 130, 246, 0.1);
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
    }
    .step.completed .step-icon {
        border-color: #10b981;
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
    }
    
    /* Conector da linha */
    .step::after {
        content: '';
        position: absolute;
        top: 15px;
        left: 50%;
        width: 100%;
        height: 2px;
        background: var(--border);
        z-index: 1;
    }
    .step:last-child::after { display: none; }
    .step.completed::after { background: #10b981; }

    /* UTILS */
    .sim-badge {
        display: inline-block;
        padding: 4px 12px;
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.4);
        color: #fbbf24;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: bold;
        letter-spacing: 1px;
        margin-bottom: 20px;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- ESTADO (SESSION STATE) ---
if 'phase' not in st.session_state: st.session_state.phase = 1
if 'data' not in st.session_state: st.session_state.data = {}
if 'options' not in st.session_state: st.session_state.options = []

# --- COMPONENTE: TIMELINE ---
def render_timeline(current):
    steps = ["INPUT", "INTELIGÊNCIA", "CRIAÇÃO", "MONTAGEM", "EXPORT"]
    
    html = '<div class="step-container">'
    for i, label in enumerate(steps):
        phase = i + 1
        status = ""
        icon = str(phase)
        
        if phase < current:
            status = "completed"
            icon = "✓"
        elif phase == current:
            status = "active"
        
        html += f"""
        <div class="step {status}">
            <div class="step-icon">{icon}</div>
            <div>{label}</div>
        </div>
        """
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# --- SIDEBAR (MENU "NATIVO") ---
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0 20px 0;">
            <h2 style="margin:0; color:white; font-size:1.4rem;">💠 AutNew</h2>
            <p style="margin:0; color:#64748b; font-size:0.8rem; letter-spacing:1px;">PRO STUDIO</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Menu estilizado via CSS para parecer lista
    menu = st.radio(
        "Navegação",
        ["🏭  Fábrica de Vídeo", "⚙️  Configurações", "📊  Monitoramento", "📜  Diretrizes", "📺  Canal"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Status Card Compacto
    st.markdown("""
    <div style="background:#0f172a; padding:15px; border-radius:12px; border:1px solid #334155;">
        <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
            <span style="font-size:0.75rem; color:#94a3b8; font-weight:600;">COTA MENSAL</span>
            <span style="font-size:0.75rem; color:#fff;">85%</span>
        </div>
        <div style="background:#1e293b; height:6px; border-radius:3px; overflow:hidden;">
            <div style="background:#3b82f6; width:85%; height:100%;"></div>
        </div>
        <div style="margin-top:10px; font-size:0.7rem; color:#64748b;">
            ● OpenAI: <span style="color:#10b981;">Online</span><br>
            ● YouTube: <span style="color:#fbbf24;">Simulado</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='margin-top:30px; font-size:0.65rem; color:#475569; text-align:center;'>{VERSION_INFO}</div>", unsafe_allow_html=True)

# --- ÁREA PRINCIPAL ---

if menu == "🏭  Fábrica de Vídeo":
    
    # Header da Área de Trabalho
    st.markdown('<div class="sim-badge">AMBIENTE DE SIMULAÇÃO</div>', unsafe_allow_html=True)
    render_timeline(st.session_state.phase)
    
    # --- FASE 1: INPUT ---
    if st.session_state.phase == 1:
        st.markdown("### 🚀 Configuração da Produção")
        st.markdown("Defina os parâmetros iniciais para ativar a esteira de automação.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("**1. Fonte de Dados**")
            url = st.text_input("URL do Concorrente", placeholder="Cole o link do YouTube...")
            st.file_uploader("Histórico do Canal (DNA)", type=['csv'])
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("**2. Estratégia**")
            intent = st.text_area("Intenção do Vídeo", height=132, placeholder="Qual o tema e o sentimento desejado?")
            st.caption("A IA usará isso para calibrar o tom emocional.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Ação
        c1, c2, c3 = st.columns([1, 2, 1])
        with c3:
            if st.button("INICIAR PROCESSAMENTO ⚡", type="primary", use_container_width=True):
                with st.spinner("Inicializando agentes de mineração..."):
                    time.sleep(1.5)
                    st.session_state.phase = 2
                    st.rerun()

    # --- FASE 2: INTELIGÊNCIA ---
    elif st.session_state.phase == 2:
        st.markdown("### 🧠 Processamento Neural")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("**Logs de Execução**")
            with st.status("Trabalhando...", expanded=True) as status:
                st.write("🔍 Minerando texto da URL...")
                time.sleep(1)
                st.write("🧬 Analisando DNA do Canal...")
                time.sleep(1)
                st.write("✨ Gerando 3 estratégias...")
                status.update(label="Completo!", state="complete", expanded=False)
            st.success("Dados extraídos com sucesso.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("**Análise de DNA (Retenção)**")
            # Gráfico Plotly
            df = pd.DataFrame({"Tema": ["Oração", "Salmos", "Mensagem"], "Retenção": [65, 50, 40]})
            fig = px.bar(df, x="Tema", y="Retenção", color="Retenção", color_continuous_scale=["#1e293b", "#3b82f6"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#94a3b8", height=200, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        c1, c2, c3 = st.columns([1, 2, 1])
        with c3:
            if st.button("VER ESTRATÉGIAS ➡️", type="primary", use_container_width=True):
                # Mock Data Generation
                st.session_state.options = [
                    {"t": "A Oração que Quebra Cadeias", "p": "Rosto idoso, luz divina azul neon."},
                    {"t": "Salmo 91: Segredo Oculto", "p": "Bíblia aberta, aura de proteção."},
                    {"t": "Sente Angústia? Prece Rápida", "p": "Silhueta saindo do túnel."}
                ]
                st.session_state.phase = 3
                st.rerun()

    # --- FASE 3: DECISÃO ---
    elif st.session_state.phase == 3:
        st.markdown("### 🎨 Estúdio Criativo")
        
        cols = st.columns(3)
        for i, opt in enumerate(st.session_state.options):
            with cols[i]:
                st.markdown(f'<div class="custom-card">', unsafe_allow_html=True)
                st.markdown(f"<small style='color:#3b82f6'>OPÇÃO 0{i+1}</small>", unsafe_allow_html=True)
                st.text_area("Título", value=opt['t'], key=f"t{i}", height=70)
                st.text_area("Prompt Visual", value=opt['p'], key=f"p{i}", height=100)
                
                c_a, c_b = st.columns(2)
                if c_a.button("🖼️ Gerar", key=f"g{i}"):
                    st.image(f"https://source.unsplash.com/random/400x225?tech&sig={i}")
                if c_b.button("✅ Escolher", key=f"s{i}"):
                    st.toast(f"Opção {i+1} selecionada!")
                st.markdown('</div>', unsafe_allow_html=True)
                
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("**Editor de Roteiro (1.600 palavras)**")
        st.text_area("Texto Verbatim", value="[ABERTURA]\nAmado irmão... (Texto completo editável)", height=200, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c3:
            if st.button("APROVAR E MONTAR 🎬", type="primary", use_container_width=True):
                with st.spinner("Renderizando cenas..."):
                    time.sleep(2)
                    st.session_state.phase = 4
                    st.rerun()

    # --- FASE 4: MONTAGEM ---
    elif st.session_state.phase == 4:
        st.markdown("### 🎞️ Estúdio de Montagem")
        st.info("A IA segmentou seu roteiro. Revise os ativos antes do render final.")
        
        for i in range(1, 4):
            with st.expander(f"Cena 0{i} | 00:0{i*5}s", expanded=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.text_area("Narração", value="Texto da narração...", height=70, key=f"c{i}", label_visibility="collapsed")
                c2.info("Visual: Stock Video")
                c3.button("🔄 Trocar", key=f"sw{i}")
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c3:
            if st.button("RENDERIZAR FINAL 🎥", type="primary", use_container_width=True):
                with st.spinner("Processando vídeo (MP4)..."):
                    time.sleep(3)
                    st.session_state.phase = 5
                    st.rerun()

    # --- FASE 5: ENTREGA ---
    elif st.session_state.phase == 5:
        st.balloons()
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800", caption="Video_Final.mp4")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 📦 Exportar")
            st.button("⬇️ Baixar MP4", use_container_width=True)
            st.button("🔴 Publicar YouTube", type="primary", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🔄 Novo Projeto"):
                st.session_state.phase = 1
                st.rerun()

# --- OUTRAS TELAS ---
elif menu == "📜  Diretrizes":
    st.title("Gestão de Diretrizes")
    st.info("Configuração do 'Cérebro' do canal.")

elif menu == "📊  Monitoramento":
    st.title("Monitor de Recursos")
    st.warning("Conecte suas chaves para ver dados reais.")
