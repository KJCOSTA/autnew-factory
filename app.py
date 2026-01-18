import streamlit as st
import time
import pandas as pd
import plotly.express as px
import datetime

# --- LOG DE VERSÃO (RODAPÉ) ---
VERSION_INFO = "AutNew V1.1 [Dark Premium] - Fix: 18/01/2026 22h30 | UX/UI Blue Tech"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="AutNew Factory | Studio AI",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PREMIUM: DARK BLUE THEME & UX ---
st.markdown("""
<style>
    /* IMPORTANDO FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400&display=swap');

    /* VARIÁVEIS DE TEMA (DARK BLUE TECH) */
    :root {
        --bg-dark: #0f172a;
        --card-bg: #1e293b;
        --primary-blue: #3b82f6;
        --accent-cyan: #06b6d4;
        --text-main: #f8fafc;
        --text-dim: #94a3b8;
        --success: #10b981;
        --gradient-btn: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        --gradient-card: linear-gradient(180deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%);
    }

    /* ESTILO GERAL DO CORPO */
    .stApp {
        background-color: var(--bg-dark);
        background-image: radial-gradient(circle at 50% 0%, #1e293b 0%, #0f172a 70%);
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        color: white !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }

    /* --- CONTAINERS & CARDS (GLASSMORPHISM) --- */
    .custom-card {
        background: var(--card-bg);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-bottom: 24px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .custom-card:hover {
        border-color: var(--primary-blue);
        transform: translateY(-2px);
    }

    /* --- BOTÕES (HIERARQUIA CLARA) --- */
    .stButton > button {
        width: 100%;
        background: var(--gradient-btn) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 0.7rem 1.5rem !important;
        border-radius: 8px !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.6) !important;
        transform: scale(1.02) !important;
    }

    /* --- INPUTS & TEXT AREAS --- */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {
        background-color: #0f172a !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 1px var(--primary-blue) !important;
    }

    /* --- SIDEBAR STYLING --- */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #334155 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: var(--text-main) !important;
    }

    /* --- TIMELINE DE PROGRESSO (NEON) --- */
    .progress-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 40px;
        background: #1e293b;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    .step-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
    }
    .step-item.active {
        color: var(--primary-blue);
        text-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
    }
    .step-item.completed {
        color: var(--success);
    }
    .step-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: #334155;
    }
    .step-item.active .step-dot {
        background-color: var(--primary-blue);
        box-shadow: 0 0 8px var(--primary-blue);
    }
    .step-item.completed .step-dot {
        background-color: var(--success);
    }

    /* --- ALERTA DE SIMULAÇÃO (MODERNO) --- */
    .sim-mode-badge {
        display: inline-block;
        background: rgba(245, 158, 11, 0.1);
        color: #fbbf24;
        border: 1px solid #fbbf24;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Manter visibilidade do menu lateral */
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
    }
    
    /* Esconder apenas elementos desnecessários */
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# --- GESTÃO DE ESTADO (SESSION STATE) ---
if 'phase' not in st.session_state:
    st.session_state.phase = 1
if 'data' not in st.session_state:
    st.session_state.data = {"url": "", "intent": ""}
if 'generated_options' not in st.session_state:
    st.session_state.generated_options = []

# --- COMPONENTES UI ---

def render_timeline(current):
    """Renderiza a timeline de progresso visual"""
    steps = ["Gatilhos", "Inteligência", "Criação", "Montagem", "Entrega"]
    
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    cols = st.columns(len(steps))
    
    for i, step in enumerate(steps):
        phase_num = i + 1
        status = ""
        
        if phase_num < current:
            status = "completed"
        elif phase_num == current:
            status = "active"
            
        with cols[i]:
            st.markdown(f"""
            <div class="step-item {status}" style="justify-content: center;">
                <div class="step-dot"></div>
                <span>{step}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def section_header(title, subtitle):
    """Renderiza cabeçalho de seção"""
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <h2 style="margin-bottom: 5px;">{title}</h2>
        <p style="color: #94a3b8; font-size: 0.9rem;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 1.5rem; margin:0;">💠 AutNew</h1>
        <p style="color:#64748b; font-size: 0.8rem; letter-spacing: 2px;">FACTORY OS</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "NAVEGAÇÃO", 
        ["🏭 Plan Run", "📜 Diretrizes", "⚙️ Build Plan", "📊 Monitor", "📺 Canal"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📡 Status do Sistema")
    
    # Status Card
    st.markdown("""
    <div style="background:#1e293b; padding:12px; border-radius:8px; border:1px solid #334155;">
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
            <span style="font-size:0.8rem; color:#94a3b8;">API Gateway</span>
            <span style="font-size:0.8rem; color:#10b981;">● Online</span>
        </div>
        <div style="background:#0f172a; height:4px; width:100%; border-radius:2px;">
            <div style="background:#3b82f6; height:4px; width:80%; border-radius:2px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption(VERSION_INFO)

# --- LÓGICA PRINCIPAL ---

if menu == "🏭 Plan Run":
    
    # Cabeçalho Global da Área de Trabalho
    st.markdown('<span class="sim-mode-badge">⚡ MODO SIMULAÇÃO (TESTE)</span>', unsafe_allow_html=True)
    render_timeline(st.session_state.phase)
    
    # --- FASE 1: GATILHOS (INPUT) ---
    if st.session_state.phase == 1:
        section_header("Configuração da Produção", "Defina os inputs para ativar os agentes neurais.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 📥 Fonte de Dados")
            url = st.text_input("🔗 URL do Concorrente", placeholder="Cole o link do YouTube aqui...")
            file = st.file_uploader("📂 Planilha DNA (Histórico)", type=['csv','xlsx'])
            
            if file:
                st.success("✅ Arquivo indexado com sucesso.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 🎯 Intenção do Vídeo")
            intent = st.text_area(
                "Objetivo Estratégico", 
                height=145, 
                placeholder="Descreva o tema, o sentimento desejado e o público-alvo..."
            )
            st.caption("💡 A IA usará isso para calibrar o tom emocional.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Ação Principal
        st.markdown("<br>", unsafe_allow_html=True)
        col_space, col_btn = st.columns([2, 1])
        with col_btn:
            if st.button("INICIAR PROCESSAMENTO ⚡", type="primary"):
                if not url and not intent:
                    st.toast("⚠️ Preencha ao menos um dos campos para continuar.", icon="⚠️")
                else:
                    with st.spinner("🔄 Acionando agentes de mineração..."):
                        time.sleep(1.5)
                        st.session_state.data['url'] = url
                        st.session_state.data['intent'] = intent
                        st.session_state.phase = 2
                        st.rerun()

    # --- FASE 2: INTELIGÊNCIA (BLACK BOX) ---
    elif st.session_state.phase == 2:
        section_header("Processamento Neural", "Os agentes estão analisando dados e gerando insights.")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 📠 Logs do Sistema")
            
            with st.status("Executando Pipeline...", expanded=True) as status:
                st.write("🔍 Minerador: Extraindo texto da URL...")
                time.sleep(1)
                st.write("🧬 Analista: Cruzando dados de retenção...")
                time.sleep(1)
                st.write("✨ Criativo: Gerando 3 variações...")
                time.sleep(0.5)
                status.update(label="✅ Processamento Concluído!", state="complete", expanded=False)
            
            st.success("📊 14.500 Tokens processados.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 📊 DNA do Canal (Retenção)")
            
            # Gráfico Dark Premium
            df = pd.DataFrame({
                "Tema": ["Oração", "Salmos", "Mensagem"], 
                "Retenção": [65, 55, 40]
            })
            fig = px.bar(
                df, x="Tema", y="Retenção", 
                color="Retenção", 
                color_continuous_scale=["#1e293b", "#3b82f6"]
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8',
                height=250,
                margin=dict(t=0, b=0, l=0, r=0),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        col_space, col_btn = st.columns([3, 1])
        with col_btn:
            if st.button("VISUALIZAR ESTRATÉGIAS ➡️", type="primary"):
                # Gerar Mocks
                if not st.session_state.generated_options:
                    st.session_state.generated_options = [
                        {"t": "A Oração que Quebra Cadeias", "p": "Close-up rosto idoso, luz divina azul neon."},
                        {"t": "Salmo 91: Segredo Oculto", "p": "Bíblia aberta na mesa, aura de proteção."},
                        {"t": "Sente Angústia? Prece Rápida", "p": "Silhueta saindo do túnel escuro para luz."}
                    ]
                st.session_state.phase = 3
                st.rerun()

    # --- FASE 3: DECISÃO CRIATIVA ---
    elif st.session_state.phase == 3:
        section_header("Estúdio de Criação", "Compare as estratégias e aprove o roteiro final.")
        
        # Grid de Opções
        cols = st.columns(3)
        for i, opt in enumerate(st.session_state.generated_options):
            with cols[i]:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.markdown(f"**OPÇÃO 0{i+1}**")
                st.markdown("---")
                
                new_t = st.text_area("Título", value=opt['t'], key=f"t{i}", height=70)
                new_p = st.text_area("Prompt Visual", value=opt['p'], key=f"p{i}", height=100)
                
                c1, c2 = st.columns(2)
                if c1.button("🖼️ Preview", key=f"prev{i}"):
                    st.image(f"https://source.unsplash.com/random/400x225?spiritual&sig={i}", caption="Mockup IA")
                
                if c2.button("✅ Escolher", key=f"sel{i}"):
                    st.toast(f"⭐ Opção {i+1} marcada como favorita!", icon="🌟")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Editor de Roteiro
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Roteiro Verbatim (1.600 Palavras)")
        roteiro = st.text_area(
            "Editor Full-Screen", 
            value="[ABERTURA MAGNÉTICA]\nAmado irmão, se você acordou hoje com o coração pesado...\n\n(Texto completo editável aqui)", 
            height=300, 
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_space, col_btn = st.columns([3, 1])
        with col_btn:
            if st.button("APROVAR E MONTAR 🎬", type="primary"):
                with st.spinner("🎨 Congelando ativos e preparando cenas..."):
                    time.sleep(2)
                    st.session_state.phase = 4
                    st.rerun()

    # --- FASE 4: MONTAGEM ---
    elif st.session_state.phase == 4:
        section_header("Linha de Montagem", "Revise a segmentação de cenas antes do render final.")
        
        # Lista de Cenas
        scenes = [
            {"id":1, "txt":"Amado irmão, se acordou com o coração apertado...", "type":"Stock Video"},
            {"id":2, "txt":"Esta oração encontrou você no momento certo.", "type":"IA Image"},
            {"id":3, "txt":"Vamos clamar a providência do Salmo 23.", "type":"Stock Video"}
        ]
        
        for scene in scenes:
            with st.expander(f"🎬 Cena 0{scene['id']} | 00:0{scene['id']*5}s", expanded=(scene['id']==1)):
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.text_area(
                    "Narração", 
                    value=scene['txt'], 
                    height=70, 
                    key=f"s{scene['id']}", 
                    label_visibility="collapsed"
                )
                c2.info(f"🎨 Visual:\n{scene['type']}")
                c3.button("🔄 Trocar", key=f"swap{scene['id']}")

        st.markdown("<br>", unsafe_allow_html=True)
        col_space, col_btn = st.columns([3, 1])
        with col_btn:
            if st.button("RENDERIZAR FINAL 🎥", type="primary"):
                with st.spinner("🎬 Renderizando MP4 (Aguarde alguns instantes)..."):
                    time.sleep(3)
                    st.session_state.phase = 5
                    st.rerun()

    # --- FASE 5: ENTREGA ---
    elif st.session_state.phase == 5:
        st.balloons()
        st.markdown("""
        <div style="text-align:center; margin-bottom:30px;">
            <h1 style="color:#10b981 !important;">🎉 Vídeo Finalizado!</h1>
            <p style="color:#94a3b8;">O arquivo foi gerado e está pronto para distribuição.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.image(
                "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800", 
                caption="Video_Final_Render_1080p.mp4"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 📦 Exportar")
            st.button("⬇️ Baixar MP4", use_container_width=True)
            st.button("🔴 Publicar no YouTube", type="primary", use_container_width=True)
            st.warning("⚠️ Atenção: A publicação via API é irreversível.")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Iniciar Novo Ciclo", use_container_width=True):
                st.session_state.phase = 1
                st.session_state.data = {"url": "", "intent": ""}
                st.session_state.generated_options = []
                st.rerun()

# --- OUTRAS TELAS ---
elif menu == "📜 Diretrizes":
    st.title("📜 Gestão de Diretrizes")
    st.info("💡 Aqui você gerencia o 'Cérebro' do canal (Lista Negra, Regras de Design, etc).")
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 🧠 Manual de Identidade Carregado")
    st.text_area(
        "Conteúdo atual", 
        value="Persona: Parceiro criativo do Mundo da Prece\nNicho: Espiritualidade ecumênica\nPúblico: 60+\n...", 
        height=200
    )
    st.button("💾 Salvar Alterações")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "⚙️ Build Plan":
    st.title("⚙️ Configuração de Fluxos")
    st.warning("🚧 Em desenvolvimento: Aqui você poderá customizar o pipeline de produção.")

elif menu == "📊 Monitor":
    st.title("📊 Monitor de Recursos")
    st.warning("🔑 Conecte suas chaves de API para ver o consumo em tempo real.")
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 🔐 Configuração de APIs")
    st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    st.text_input("Google Gemini API Key", type="password", placeholder="AIza...")
    st.button("💾 Salvar Credenciais")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📺 Canal":
    st.title("📺 Gestão do Canal YouTube")
    st.info("🔗 Conecte sua conta do YouTube para publicação automática.")
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 🎬 Canal: Mundo da Prece")
    st.metric("Inscritos", "45.2K", "+1.2K")
    st.metric("Vídeos Publicados", "127", "+3 esta semana")
    st.markdown('</div>', unsafe_allow_html=True)
