import streamlit as st
import time
import pandas as pd
import plotly.express as px
import datetime

# --- LOG DE VERSÃO (RODAPÉ) ---
VERSION_INFO = "AutNew V1 - Atualização nº0001 - 18/01/2026 - 16h40 | UI/UX Premium + Feedback Visual"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="AutNew Factory V1",
    page_icon="🙏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS VISUAIS PREMIUM (CSS) ---
st.markdown("""
<style>
    /* FONTS & CORES GLOBAIS */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    :root {
        --primary-gold: #D4AF37;
        --gold-hover: #B5952F;
        --bg-color: #F8F9FA;
        --card-bg: #FFFFFF;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
    }

    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--text-primary);
    }

    /* --- COMPONENTE: CARD PADRONIZADO --- */
    .custom-card {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .custom-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border-color: var(--primary-gold);
    }

    /* --- BOTÕES PADRONIZADOS --- */
    /* Primário (Ação Principal) */
    div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        background-color: var(--primary-gold) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px rgba(212, 175, 55, 0.3) !important;
    }
    div[data-testid="stHorizontalBlock"] button[kind="primary"]:hover {
        background-color: var(--gold-hover) !important;
        transform: translateY(-1px);
    }

    /* Secundário (Ações de Apoio) */
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
        background-color: white !important;
        border: 1px solid #E5E7EB !important;
        color: var(--text-secondary) !important;
        border-radius: 8px !important;
    }
    div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
        border-color: var(--primary-gold) !important;
        color: var(--primary-gold) !important;
    }

    /* --- TIMELINE DE PROGRESSO --- */
    .progress-track {
        display: flex;
        justify-content: space-between;
        position: relative;
        margin-bottom: 40px;
        padding: 0 20px;
    }
    .progress-track::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 20px;
        right: 20px;
        height: 2px;
        background: #E5E7EB;
        z-index: 0;
    }
    .progress-step {
        position: relative;
        z-index: 1;
        background: white;
        padding: 0 10px;
        color: #9CA3AF;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .progress-step.active {
        color: var(--primary-gold);
    }
    .progress-step.completed {
        color: #10B981;
    }
    
    /* --- ALERTA DE SIMULAÇÃO --- */
    .sim-badge {
        background-color: #FEF3C7;
        color: #92400E;
        font-size: 0.75rem;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
        border: 1px solid #F59E0B;
        display: inline-block;
        margin-bottom: 10px;
    }

    /* Esconder elementos padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- GESTÃO DE ESTADO (SESSION STATE) ---
if 'phase' not in st.session_state:
    st.session_state.phase = 1
if 'data' not in st.session_state:
    st.session_state.data = {"url": "", "intent": ""}
if 'generated_options' not in st.session_state:
    st.session_state.generated_options = []

# --- FUNÇÃO VISUAL: TIMELINE ---
def render_progress_bar(current):
    steps = ["1. Gatilhos", "2. Inteligência", "3. Criação", "4. Montagem", "5. Entrega"]
    
    html = '<div class="progress-track">'
    for i, step in enumerate(steps):
        phase_num = i + 1
        if phase_num < current:
            status = "completed"
            icon = "✅"
        elif phase_num == current:
            status = "active"
            icon = "📍"
        else:
            status = ""
            icon = "⚪"
            
        html += f'<div class="progress-step {status}"><span>{icon}</span> {step}</div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/D4AF37/praying-hands.png", width=40)
    st.markdown("### **AutNew** Factory")
    st.caption("Video Factory V1")
    
    st.markdown("---")
    menu = st.radio("Navegação", ["🏭 Plan Run", "📜 Diretrizes", "⚙️ Build Plan", "📊 Monitor", "📺 Canal"], label_visibility="collapsed")
    
    st.markdown("---")
    # Status de Simulação
    st.markdown("""
    <div style='background-color:#FEF3C7; padding:10px; border-radius:8px; border:1px solid #FCD34D;'>
        <small style='color:#92400E; font-weight:bold;'>🔌 MODO SIMULAÇÃO</small><br>
        <small style='color:#92400E;'>APIs Desconectadas.</small>
    </div>
    """, unsafe_allow_html=True)
    
    # RODAPÉ DE VERSÃO (SEU PEDIDO)
    st.markdown("---")
    st.caption(VERSION_INFO)

# --- LÓGICA: PLAN RUN ---
if menu == "🏭 Plan Run":
    
    # 1. CABEÇALHO COM CONTEXTO
    st.markdown(f"<div class='sim-badge'>AMBIENTE DE TESTE</div>", unsafe_allow_html=True)
    render_progress_bar(st.session_state.phase)
    
    # --- FASE 1: GATILHOS ---
    if st.session_state.phase == 1:
        st.markdown("<h2 class='serif-font'>Configuração da Produção</h2>", unsafe_allow_html=True)
        st.markdown("Defina os parâmetros iniciais para ativar a fábrica.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 📥 Fontes de Dados")
            url = st.text_input("🔗 URL do Concorrente", value=st.session_state.data.get('url', ''), placeholder="Cole o link do YouTube...")
            file = st.file_uploader("📂 Planilha de Histórico (DNA)", type=['xlsx', 'csv'])
            
            if file:
                st.toast("Arquivo carregado com sucesso!", icon="✅")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Intenção Estratégica")
            intent = st.text_area("Objetivo do Vídeo", value=st.session_state.data.get('intent', ''), height=145, placeholder="Qual o tema espiritual e o objetivo deste vídeo?")
            st.caption("ℹ️ O sistema cruzará este tema com sua planilha de melhores desempenhos.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # AÇÃO PRINCIPAL
        col_actions = st.columns([2, 1])
        with col_actions[1]:
            if st.button("INICIAR PROCESSAMENTO 🚀", type="primary", use_container_width=True):
                if not url and not intent:
                    st.toast("⚠️ Preencha pelo menos um campo para testar.", icon="⚠️")
                else:
                    with st.spinner("Inicializando motores de IA..."):
                        time.sleep(1.5)
                        st.session_state.data['url'] = url
                        st.session_state.data['intent'] = intent
                        st.session_state.phase = 2
                        st.rerun()

    # --- FASE 2: INTELIGÊNCIA ---
    elif st.session_state.phase == 2:
        st.markdown("<h2 class='serif-font'>Inteligência de Dados</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 📡 Processamento")
            
            with st.status("Executando Agentes...", expanded=True) as status:
                st.write("🔍 Minerando texto (Sem vídeo)...")
                time.sleep(1)
                st.write("🧬 Analisando DNA do Canal...")
                time.sleep(1)
                st.write("✨ Gerando estratégias criativas...")
                status.update(label="Análise Completa!", state="complete", expanded=False)
            
            st.info("✅ 14.500 caracteres extraídos.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 📊 Insights de Retenção")
            
            # Gráfico Plotly Limpo
            df = pd.DataFrame({"Tema": ["Oração Manhã", "Salmos", "Mensagem"], "Retenção": [65, 55, 40]})
            fig = px.bar(df, x="Tema", y="Retenção", color="Retenção", color_continuous_scale=["#E5E7EB", "#D4AF37"])
            fig.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        col_actions = st.columns([3, 1])
        with col_actions[1]:
            if st.button("VER ESTRATÉGIAS ➡️", type="primary", use_container_width=True):
                # Gerar dados mockados se vazio
                if not st.session_state.generated_options:
                    st.session_state.generated_options = [
                        {"t": "A Oração que Quebra Cadeias", "p": "Rosto idoso, luz divina, choque sagrado."},
                        {"t": "Salmo 91: Segredo Oculto", "p": "Bíblia aberta, aura azul protetora."},
                        {"t": "Sente Angústia? Prece Rápida", "p": "Silhueta saindo do túnel para a luz."}
                    ]
                st.session_state.phase = 3
                st.rerun()

    # --- FASE 3: CRIAÇÃO (MULTI-OPTION) ---
    elif st.session_state.phase == 3:
        st.markdown("<h2 class='serif-font'>Estúdio Criativo</h2>", unsafe_allow_html=True)
        st.markdown("Escolha e refine a melhor estratégia. Você está no comando.")
        
        # Grid de Opções
        cols = st.columns(3)
        selected_option = None
        
        for i, opt in enumerate(st.session_state.generated_options):
            with cols[i]:
                st.markdown(f'<div class="custom-card">', unsafe_allow_html=True)
                st.markdown(f"**OPÇÃO {i+1}**")
                
                # Campos Editáveis
                new_t = st.text_area("Título", value=opt['t'], key=f"t{i}", height=70)
                new_p = st.text_area("Prompt Visual", value=opt['p'], key=f"p{i}", height=70)
                
                # Ações Individuais
                c1, c2 = st.columns(2)
                if c1.button("🖼️ Gerar", key=f"btn_g{i}", help="Gerar preview da thumb"):
                    with st.spinner("Gerando imagem..."):
                        time.sleep(1.5)
                        st.image(f"https://source.unsplash.com/random/400x225?spiritual&sig={i}", caption="Preview")
                
                if c2.button("✅ Escolher", key=f"btn_s{i}", type="secondary"):
                    st.toast(f"Opção {i+1} selecionada para produção!", icon="🌟")
                
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("### 📝 Editor de Roteiro")
        with st.expander("Abrir Editor de Texto (1.600 palavras)", expanded=True):
            st.text_area("Conteúdo Verbatim", value="[ABERTURA] Amado irmão... (Texto completo)", height=300)

        col_actions = st.columns([3, 1])
        with col_actions[1]:
            if st.button("APROVAR E MONTAR 🎬", type="primary", use_container_width=True):
                with st.spinner("Congelando roteiro e gerando cenas..."):
                    time.sleep(1.5)
                    st.session_state.phase = 4
                    st.rerun()

    # --- FASE 4: MONTAGEM ---
    elif st.session_state.phase == 4:
        st.markdown("<h2 class='serif-font'>Estúdio de Montagem</h2>", unsafe_allow_html=True)
        st.info("A IA segmentou seu roteiro. Revise os ativos antes de renderizar.")
        
        scenes = [
            {"id":1, "txt":"Amado irmão, se acordou com o coração apertado...", "type":"Stock Video"},
            {"id":2, "txt":"Esta oração encontrou você no momento certo.", "type":"IA Image"},
            {"id":3, "txt":"Vamos clamar a providência do Salmo 23.", "type":"Stock Video"}
        ]
        
        for scene in scenes:
            with st.container():
                st.markdown(f"**Cena {scene['id']}**")
                c1, c2, c3 = st.columns([3, 2, 1])
                c1.text_area("Narração", value=scene['txt'], height=70, key=f"s{scene['id']}", label_visibility="collapsed")
                c2.info(f"Visual: {scene['type']}")
                c3.button("🔄 Trocar", key=f"swap{scene['id']}")
                st.divider()
        
        col_actions = st.columns([3, 1])
        with col_actions[1]:
            if st.button("RENDERIZAR FINAL 🎥", type="primary", use_container_width=True):
                with st.spinner("Renderizando MP4 (Isso pode levar alguns segundos)..."):
                    time.sleep(3)
                    st.session_state.phase = 5
                    st.rerun()

    # --- FASE 5: ENTREGA ---
    elif st.session_state.phase == 5:
        st.balloons()
        st.success("🎉 Renderização concluída com sucesso!")
        
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([2, 1])
        with c1:
            st.image("https://images.unsplash.com/photo-1507692049790-de58293a4697?w=800", caption="Video_Final.mp4")
        with c2:
            st.markdown("### 📦 Ações Finais")
            st.button("⬇️ Baixar MP4 (1080p)", use_container_width=True)
            st.button("🔴 Publicar no YouTube", type="primary", use_container_width=True)
            st.caption("O upload usará a API conectada no menu 'Canal'.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🔄 Começar Novo Vídeo"):
            st.session_state.phase = 1
            st.rerun()

# --- OUTRAS PÁGINAS ---
elif menu == "📜 Diretrizes":
    st.title("Manual de Identidade")
    st.info("Painel de gestão de regras ativas.")
    # (Tabela de diretrizes iria aqui - simplificada para este update focado em UX)

elif menu == "📊 Monitor":
    st.title("Monitor de Recursos")
    st.warning("Conecte suas chaves para ver dados reais.")
