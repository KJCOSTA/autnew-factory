import streamlit as st
import time
import pandas as pd
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="AutNew Factory V1",
    page_icon="🙏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS VISUAIS (CSS PREMIUM) ---
st.markdown("""
<style>
    /* Cores Premium: Mundo da Prece */
    .stApp {
        background-color: #F9F7F2;
    }
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #2C2C2C;
        font-weight: 700;
        font-size: 2.5rem;
    }
    .gold-btn {
        background-color: #D4AF37 !important;
        color: white !important;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: bold;
    }
    /* Cards personalizados */
    .custom-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #E5E7EB;
        margin-bottom: 20px;
    }
    
    /* Esconder menu padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- GESTÃO DE ESTADO (MEMÓRIA DA SESSÃO) ---
if 'phase' not in st.session_state:
    st.session_state.phase = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

# --- BARRA LATERAL (NAVEGAÇÃO) ---
with st.sidebar:
    st.markdown("## 🙏 **AutNew** Factory")
    st.caption("Versão: Video Factory V1")
    st.markdown("---")
    
    # Menu de Navegação
    menu = st.radio(
        "Navegação", 
        ["🏭 Plan Run (Fábrica)", "⚙️ Build Plan", "📊 Monitor", "📜 Diretrizes", "📺 Canal"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    # Monitor de Recursos (Mini)
    st.markdown("#### 📡 Monitor de Saúde")
    st.progress(85, text="Cotas OpenAI")
    st.caption("API Status: 🟢 Online")
    
    with st.expander("🛠️ Ferramentas Ativas"):
        st.write("✅ YouTube Data API")
        st.write("✅ Gemini 3 Pro")
        st.write("✅ MoviePy Engine")

# --- LÓGICA DAS PÁGINAS ---

if menu == "🏭 Plan Run (Fábrica)":
    
    # CABEÇALHO DINÂMICO
    phases = {
        1: "Fase 1: Configuração & Gatilhos",
        2: "Fase 2: Inteligência (Processamento)",
        3: "Fase 3: Sala de Criação & Decisão",
        4: "Fase 4: Estúdio de Montagem",
        5: "Fase 5: Entrega Final"
    }
    
    st.markdown(f"<h1 class='main-header'>{phases[st.session_state.phase]}</h1>", unsafe_allow_html=True)
    
    # --- FASE 1: INPUTS ---
    if st.session_state.phase == 1:
        st.info("👋 Bem-vindo ao Turno de Produção. Insira os dados para iniciar a automação.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 📥 Dados de Entrada")
            url = st.text_input("🔗 URL do Concorrente (YouTube)", placeholder="https://youtube.com/...")
            arquivo = st.file_uploader("📂 Planilha de Histórico (.xlsx)", type=['xlsx', 'csv'])
            
            # Bifurcação Manual
            with st.expander("✍️ Transcrição Manual (Opcional)"):
                manual_text = st.text_area("Cole o texto aqui se necessário", height=150)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 🎯 Intenção Estratégica")
            intent = st.text_area("Qual o objetivo espiritual deste vídeo?", height=150, 
                                placeholder="Ex: Oração da manhã para quebra de maldições financeiras. Tom solene.")
            
            st.markdown("#### 📜 Diretrizes Ativas")
            st.warning("⚠️ Lista Negra Ativa: 'Blindar', 'Escudo', 'Chave' (Bloqueados)")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("🚀 INICIAR PLAN RUN", type="primary", use_container_width=True):
            # Em produção real, validariamos se url e intent existem.
            # Para teste rápido, permitimos avançar.
            st.session_state.data['url'] = url
            st.session_state.data['intent'] = intent
            st.session_state.phase = 2
            st.rerun()

    # --- FASE 2: PROCESSAMENTO (SIMULAÇÃO BACKEND) ---
    elif st.session_state.phase == 2:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 📡 Logs do Sistema")
            with st.status("Processando Motores de IA...", expanded=True) as status:
                st.write("🔍 Minerando metadados do YouTube (Anti-Erro Imagem)...")
                time.sleep(1)
                st.write("✅ Transcrição extraída (14.500 caracteres)")
                st.write("📊 Executando 'Code Execution' na planilha...")
                time.sleep(1.5)
                st.write("🧬 Padrão de Retenção Identificado: 'Orações > 12min'")
                st.write("📖 Realizando Pesquisa Teológica (Deep Research)...")
                time.sleep(1)
                st.write("✨ Gerando Roteiro Criativo (Gemini 3 Pro)...")
                status.update(label="Processamento Completo!", state="complete", expanded=False)
        
        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 🧬 Análise de DNA (Code Execution)")
            # Gráfico Simulado
            chart_data = pd.DataFrame({
                "Temas": ["Oração Manhã", "Cura", "Salmos", "Mensagem Noite"],
                "Retenção (%)": [65, 42, 58, 48]
            })
            st.bar_chart(chart_data, x="Temas", y="Retenção (%)", color="#D4AF37")
            st.caption("O sistema identificou que 'Oração da Manhã' tem 35% mais retenção.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("➡️ Avançar para Sala de Criação"):
            st.session_state.phase = 3
            st.rerun()

    # --- FASE 3: DECISÃO CRIATIVA ---
    elif st.session_state.phase == 3:
        st.success("✅ Roteiro e Estratégias gerados! Revise e aprove.")
        
        col_esq, col_dir = st.columns([1, 2])
        
        with col_esq:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 1. Escolha o Título Viral")
            titulo = st.radio(
                "Opções geradas com base em CTR:",
                [
                    "A Oração da Manhã que Quebra Cadeias Invisíveis (Revelação)",
                    "Salmo 91: O Segredo Oculto para Proteger sua Casa Hoje",
                    "Sente Angústia? Faça Esta Prece de 3 Minutos Agora"
                ]
            )
            
            st.markdown("---")
            st.markdown("### 2. Conceito da Thumbnail")
            thumb_opt = st.radio(
                "Conceitos Visuais (Anatomia 60+):",
                ["A: Choque Sagrado (Rosto Close-up)", "B: Mãos de Poder (Clima Tempestade)", "C: A Porta Aberta (Silhueta)"]
            )
            st.info(f"Prompt Imagen 3 (Inglês): Cinematic close-up of elderly hands clasped in prayer, golden light, high contrast.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_dir:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 3. Editor de Roteiro (Verbatim)")
            st.caption("Este texto será usado para gerar a narração na próxima etapa.")
            roteiro_txt = st.text_area(
                "Edite o roteiro antes da narração:",
                value="""[ABERTURA MAGNÉTICA 0:00]
Amado irmão, amada irmã. Se o seu coração acordou hoje apertado, sentindo que os caminhos estão fechados, esta oração encontrou você no momento certo.

[PARTICIPAÇÃO IMEDIATA]
Já clique no botão de inscrever-se e deixe seu "Amém" nos comentários...

[DESENVOLVIMENTO IMERSIVO]
Hoje vamos clamar a providência divina baseada no mistério do Salmo 23...

[CTA FINAL - OFERTA]
Como prometido, o link para o E-book "Orações da Família Brasileira" está fixado no primeiro comentário.""",
                height=500
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("---")
        col_actions = st.columns(4)
        with col_actions[3]:
            if st.button("✨ APROVAR E IR PARA MONTAGEM", type="primary", use_container_width=True):
                st.session_state.phase = 4
                st.rerun()

    # --- FASE 4: ESTÚDIO DE MONTAGEM (NOVO) ---
    elif st.session_state.phase == 4:
        st.markdown("### 🎬 Estúdio de Montagem Automática")
        st.info("A IA segmentou seu roteiro em cenas. Revise cada bloco antes da renderização final.")
        
        # Simulação de Cenas
        cenas = [
            {"id": 1, "texto": "Amado irmão... Se o seu coração acordou hoje apertado...", "visual": "Video Stock: Man Praying Silhouette (Pexels)", "audio": "Audio_01.mp3"},
            {"id": 2, "texto": "Hoje vamos clamar a providência divina baseada no mistério do Salmo 23.", "visual": "Imagem IA: Luz Dourada sobre Bíblia (DALL-E)", "audio": "Audio_02.mp3"},
            {"id": 3, "texto": "Sinta essa paz invadindo seu lar agora.", "visual": "Video Stock: Family Hugging (Pexels)", "audio": "Audio_03.mp3"}
        ]
        
        for cena in cenas:
            with st.container():
                st.markdown(f"#### Cena {cena['id']}")
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    st.text_area("Narração", value=cena['texto'], height=70, key=f"txt_{cena['id']}")
                with c2:
                    # Usando uma imagem placeholder real
                    st.image("https://images.unsplash.com/photo-1507692049790-de58293a4697?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80", caption=cena['visual'])
                with c3:
                    st.button(f"🔄 Trocar Visual", key=f"btn_v_{cena['id']}")
                    st.button(f"🔊 Ouvir Áudio", key=f"btn_a_{cena['id']}")
                st.divider()
        
        col_final = st.columns(3)
        with col_final[1]:
            if st.button("🎥 RENDERIZAR VÍDEO FINAL (MP4)", type="primary", use_container_width=True):
                st.session_state.phase = 5
                st.rerun()

    # --- FASE 5: ENTREGA FINAL ---
    elif st.session_state.phase == 5:
        st.balloons()
        st.markdown("<center><h2>📦 Vídeo Pronto para Publicação!</h2></center>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 📺 Preview Final")
            # Placeholder de vídeo
            st.image("https://images.unsplash.com/photo-1507692049790-de58293a4697?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80", caption="Video_Final_Render.mp4")
            st.download_button("⬇️ Baixar MP4 (1080p)", data="Mock Data", file_name="Video_Final.mp4", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### 🚀 Publicação Automática")
            st.markdown("**Canal Conectado:** Mundo da Prece")
            st.text_input("Título Final", value="A Oração da Manhã que Quebra Cadeias Invisíveis (Revelação)")
            st.text_area("Descrição", "🙏 A Oração da Manhã que Quebra Cadeias...\n\n#Oração #Fé", height=150)
            
            if st.button("🔴 PUBLICAR NO YOUTUBE", type="primary"):
                st.success("Enviando via API... (Simulado)")
                time.sleep(2)
                st.success("✅ Publicado com Sucesso! Link: youtu.be/xyz123")
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("---")
        if st.button("🔄 Criar Novo Vídeo"):
            st.session_state.phase = 1
            st.rerun()

# --- OUTRAS PÁGINAS ---
elif menu == "📊 Monitor":
    st.title("Monitor de Recursos")
    st.info("Conecte suas chaves de API aqui.")
    st.text_input("OpenAI API Key", type="password")
    st.text_input("Google Gemini API Key", type="password")
    st.button("Salvar Chaves")

elif menu == "📜 Diretrizes":
    st.title("Diretrizes Mestre")
    st.markdown("Aqui fica o seu manual 'Constituição'.")
    st.text_area("Editor de Manual", "1. Lista Negra: Blindar, Escudo...", height=300)
