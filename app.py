import streamlit as st
import time
import pandas as pd
import plotly.express as px
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="AutNew Factory V1",
    page_icon="🙏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS VISUAIS (CSS PREMIUM & ALERTAS) ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    :root {
        --primary-gold: #D4AF37;
        --secondary-gold: #AA8C2C;
        --bg-color: #F9F7F2;
        --text-dark: #2C2C2C;
    }

    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, .serif-font {
        font-family: 'Playfair Display', serif !important;
        color: var(--text-dark);
    }

    /* BARRA DE ALERTA DE SIMULAÇÃO */
    .simulation-banner {
        background-color: #FEF3C7;
        border: 1px solid #F59E0B;
        color: #92400E;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 0.9rem;
    }

    /* TIMELINE STYLES */
    .timeline-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding: 1rem 2rem;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        position: relative;
    }
    .timeline-line {
        position: absolute;
        top: 50%; left: 60px; right: 60px; height: 3px; background: #E5E7EB; z-index: 0; transform: translateY(-50%);
    }
    .timeline-progress {
        position: absolute;
        top: 50%; left: 60px; height: 3px; background: var(--primary-gold); z-index: 0; transform: translateY(-50%); transition: width 0.5s ease;
    }
    .step-wrapper {
        position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center;
    }
    .step-circle {
        width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; background: white; border: 2px solid #E5E7EB; color: #9CA3AF; margin-bottom: 0.5rem; transition: all 0.3s ease;
    }
    .step-active .step-circle {
        border-color: var(--primary-gold); background: var(--primary-gold); color: white; box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
    }
    .step-completed .step-circle {
        border-color: #10B981; background: #10B981; color: white;
    }
    .step-label {
        font-size: 0.75rem; font-weight: 600; color: #9CA3AF; text-transform: uppercase;
    }
    .step-active .step-label { color: var(--primary-gold); }
    .step-completed .step-label { color: #10B981; }

    /* Custom Cards */
    .custom-card {
        background-color: white; padding: 24px; border-radius: 16px; border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    /* Buttons */
    div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        background-color: var(--primary-gold) !important;
        border-color: var(--primary-gold) !important;
        color: white !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- GESTÃO DE ESTADO (SESSION STATE) ---
if 'phase' not in st.session_state:
    st.session_state.phase = 1

# Inicialização das Diretrizes (Pre-load com os dados do manual)
if 'guidelines_df' not in st.session_state:
    data = [
        {"Categoria": "Lista Negra", "Tag": "Proibido", "Diretriz": "Não usar: Blindar, Blindagem, Escudo, Chave, Muralha", "Ativo": True},
        {"Categoria": "Lista Negra", "Tag": "Proibido", "Diretriz": "Não usar: 'Se você sente', 'Você não chegou aqui por acaso', 'Respire fundo'", "Ativo": True},
        {"Categoria": "Lista Negra", "Tag": "Promessas", "Diretriz": "Não prometer curas médicas ou ganhos materiais diretos", "Ativo": True},
        {"Categoria": "Thumb Visual", "Tag": "Anatomia 60+", "Diretriz": "Fontes Extra Grandes e Extra Bolds. Alto contraste.", "Ativo": True},
        {"Categoria": "Thumb Visual", "Tag": "Emoção", "Diretriz": "Rostos: Choque sagrado, paz profunda. NUNCA sorrisos genéricos.", "Ativo": True},
        {"Categoria": "Roteiro", "Tag": "Estrutura", "Diretriz": "0-30s: Abertura Magnética com promessa clara.", "Ativo": True},
        {"Categoria": "Roteiro", "Tag": "CTA", "Diretriz": "Meio do vídeo: CTA para compartilhamento.", "Ativo": True},
        {"Categoria": "Roteiro", "Tag": "Venda", "Diretriz": "Final: CTA para E-book e Grupo VIP.", "Ativo": True},
        {"Categoria": "SEO", "Tag": "Hashtags", "Diretriz": "Máximo 15 tags. 3 genéricas, 4 cauda longa, 2 branding.", "Ativo": True},
    ]
    st.session_state.guidelines_df = pd.DataFrame(data)

# --- FUNÇÕES ---
def render_timeline(current_phase):
    steps = [
        {"id": 1, "label": "Gatilhos", "icon": "1"},
        {"id": 2, "label": "Inteligência", "icon": "2"},
        {"id": 3, "label": "Criação", "icon": "3"},
        {"id": 4, "label": "Montagem", "icon": "4"},
        {"id": 5, "label": "Entrega", "icon": "5"}
    ]
    progress_pct = ((current_phase - 1) / (len(steps) - 1)) * 100
    
    html = f"""
    <div class="timeline-container">
        <div class="timeline-line"></div>
        <div class="timeline-progress" style="width: {progress_pct}%"></div>
    """
    for step in steps:
        status = "step-completed" if step['id'] < current_phase else ("step-active" if step['id'] == current_phase else "")
        icon = "✓" if step['id'] < current_phase else step['icon']
        html += f"""
        <div class="step-wrapper {status}">
            <div class="step-circle">{icon}</div>
            <div class="step-label">{step['label']}</div>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def simulation_banner():
    st.markdown("""
    <div class="simulation-banner">
        ⚠️ MODO DE SIMULAÇÃO (TESTE): APIs Desconectadas • Nenhum custo real gerado • Dados fictícios
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🙏 **AutNew** Factory")
    st.caption("Video Factory V1")
    st.markdown("---")
    
    menu = st.radio("Navegação", ["🏭 Plan Run", "📜 Diretrizes (Gestão)", "⚙️ Build Plan", "📊 Monitor", "📺 Canal"], label_visibility="collapsed")
    
    st.markdown("---")
    st.error("🔌 **APIs: OFFLINE** (Simulação)")
    st.markdown("**Status dos Motores:**")
    st.code("OpenAI: ... Simulando\nGemini: ... Simulando\nYouTube: .. Simulando", language="text")

# --- PÁGINA: PLAN RUN ---
if menu == "🏭 Plan Run":
    simulation_banner()
    render_timeline(st.session_state.phase)
    
    # FASE 1: GATILHOS
    if st.session_state.phase == 1:
        st.markdown("<h2 class='serif-font'>Fase 1: Configuração</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 📥 Inputs")
            st.text_input("🔗 URL Concorrente", placeholder="https://...")
            st.file_uploader("📂 Planilha DNA", type=['csv','xlsx'])
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Intenção")
            st.text_area("Objetivo", height=145, placeholder="Ex: Oração da manhã...")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("INICIAR PROCESSAMENTO 🚀", type="primary", use_container_width=True):
            with st.spinner("Inicializando motores..."):
                time.sleep(1)
                st.session_state.phase = 2
                st.rerun()

    # FASE 2: INTELIGÊNCIA
    elif st.session_state.phase == 2:
        st.markdown("<h2 class='serif-font'>Fase 2: Inteligência de Dados</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.info("📡 **Processando (Simulado)...**")
            with st.status("Mineração em andamento", expanded=True):
                st.write("🔍 Extraindo texto (sem vídeo)...")
                time.sleep(1)
                st.write("🧬 Analisando DNA do Canal...")
                time.sleep(1)
                st.write("✨ Gerando estratégias criativas...")
        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 📊 Insights de Retenção")
            df_chart = pd.DataFrame({"Tema": ["Oração", "Salmos", "Mensagem"], "Retenção": [65, 55, 40]})
            fig = px.bar(df_chart, x="Tema", y="Retenção", color="Retenção", color_continuous_scale=["#eee", "#D4AF37"])
            fig.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("VER PROPOSTAS ➡️", type="primary", use_container_width=True):
            st.session_state.phase = 3
            st.rerun()

    # FASE 3: CRIAÇÃO (DECISÃO)
    elif st.session_state.phase == 3:
        st.markdown("<h2 class='serif-font'>Fase 3: Estúdio Criativo</h2>", unsafe_allow_html=True)
        st.markdown("Revise as opções geradas pela IA baseadas nas suas Diretrizes.")
        
        cols = st.columns(3)
        opcoes = [
            {"t": "A Oração que Quebra Cadeias", "p": "Close-up rosto idoso, luz divina."},
            {"t": "Salmo 91: Segredo Oculto", "p": "Bíblia aberta, aura azul."},
            {"t": "Sente Angústia? Prece de 3 min", "p": "Silhueta saindo do túnel."}
        ]
        
        # Seleção visual
        selected_idx = st.radio("Escolha a melhor estratégia:", [0, 1, 2], 
                                format_func=lambda x: f"Opção {x+1}", 
                                label_visibility="collapsed", horizontal=True)

        # Mostrar Detalhes da Opção Selecionada
        opt = opcoes[selected_idx]
        st.markdown(f"""
        <div class="custom-card" style="border-left: 5px solid #D4AF37;">
            <h3>Opção {selected_idx+1} Selecionada</h3>
            <p><b>Título:</b> {opt['t']}</p>
            <p><b>Prompt Thumb:</b> {opt['p']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📝 Editor de Roteiro")
        st.text_area("Edite o roteiro aqui:", value="[ABERTURA] Amado irmão... (Texto de 1.600 palavras)", height=200)
        
        st.markdown("---")
        
        # BOTÃO DE AÇÃO COM FEEDBACK
        col_act1, col_act2 = st.columns([3, 1])
        with col_act2:
            if st.button("✅ APROVAR E MONTAR", type="primary", use_container_width=True):
                with st.spinner("Salvando aprovação e gerando cenas..."):
                    time.sleep(1.5) # Tempo para usuário ver que algo aconteceu
                    st.session_state.phase = 4
                    st.rerun()

    # FASE 4: MONTAGEM
    elif st.session_state.phase == 4:
        st.markdown("<h2 class='serif-font'>Fase 4: Estúdio de Montagem</h2>", unsafe_allow_html=True)
        st.info("ℹ️ A IA segmentou seu roteiro em cenas. Revise os visuais antes de renderizar.")
        
        for i in range(1, 4):
            with st.expander(f"Cena {i} (00:0{i*5})", expanded=True):
                c1, c2 = st.columns([3, 1])
                c1.text_area(f"Texto Cena {i}", value="Texto da narração...", height=70, key=f"c{i}")
                c2.button(f"🔄 Trocar Visual", key=f"btn{i}")
        
        if st.button("🎥 RENDERIZAR FINAL", type="primary", use_container_width=True):
            with st.spinner("Renderizando vídeo (Simulado)..."):
                time.sleep(2)
                st.session_state.phase = 5
                st.rerun()

    # FASE 5: ENTREGA
    elif st.session_state.phase == 5:
        st.balloons()
        st.success("🎉 Vídeo Renderizado com Sucesso!")
        col1, col2 = st.columns([2, 1])
        col1.image("https://images.unsplash.com/photo-1507692049790-de58293a4697?w=800", caption="Video_Final.mp4")
        col2.button("⬇️ Baixar MP4", use_container_width=True)
        col2.button("🔴 Publicar no YouTube", type="primary", use_container_width=True)
        
        if st.button("🔄 Novo Projeto"):
            st.session_state.phase = 1
            st.rerun()

# --- PÁGINA: GESTOR DE DIRETRIZES (CRUD) ---
elif menu == "📜 Diretrizes (Gestão)":
    st.markdown("<h2 class='serif-font'>Gestão de Diretrizes & Ativos</h2>", unsafe_allow_html=True)
    st.markdown("Adicione, edite ou remova as regras que a IA deve seguir. Isso é o 'Cérebro' do canal.")
    
    # Editor de Dados Interativo
    edited_df = st.data_editor(
        st.session_state.guidelines_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Categoria": st.column_config.SelectboxColumn(
                "Categoria",
                options=["Lista Negra", "Thumb Visual", "Roteiro", "SEO", "Geral"],
                required=True
            ),
            "Tag": st.column_config.TextColumn("Tag (Ex: Proibido)", required=True),
            "Diretriz": st.column_config.TextColumn("Regra / Instrução", width="large", required=True),
            "Ativo": st.column_config.CheckboxColumn("Ativo?", default=True)
        }
    )
    
    # Botão de Salvar (Persistência na Sessão)
    if st.button("💾 Salvar Alterações nas Diretrizes", type="primary"):
        st.session_state.guidelines_df = edited_df
        st.success("Diretrizes atualizadas! A IA usará essas regras na próxima execução.")
        st.balloons()

# --- OUTRAS PÁGINAS ---
elif menu == "📊 Monitor":
    st.title("Monitor de Recursos")
    simulation_banner()
    st.info("Aqui você verá o consumo real das APIs quando conectadas.")

elif menu == "⚙️ Build Plan":
    st.title("Construtor de Fluxos")
    st.info("Área futura para arrastar e soltar novos blocos de lógica.")
