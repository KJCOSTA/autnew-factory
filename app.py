<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutNew Factory V1 - Dashboard de Produção</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Chart.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    
    <!-- FontAwesome (Icons) -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">

    <!-- Chosen Palette: Spiritual Premium -->
    <!-- Primary Background: Warm Paper (#F9F7F2) -->
    <!-- Text: Deep Charcoal (#2C2C2C) -->
    <!-- Accent: Divine Gold (#D4AF37) -->
    <!-- UI Elements: Soft White (#FFFFFF) & Light Gray (#E5E7EB) -->

    <style>
        /* Base Typography */
        body {
            font-family: 'Lato', sans-serif;
            background-color: #F9F7F2;
            color: #2C2C2C;
        }
        
        h1, h2, h3, .serif-font {
            font-family: 'Playfair Display', serif;
        }

        .mono-font {
            font-family: 'JetBrains Mono', monospace;
        }

        /* Chart Container Styling - CRITICAL REQUIREMENT */
        .chart-container {
            position: relative;
            width: 100%;
            max-width: 100%; /* Flexible within parent grid */
            height: 300px;
            max-height: 400px;
            margin: 0 auto;
        }
        
        @media (min-width: 768px) {
            .chart-container {
                height: 350px;
            }
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1; 
        }
        ::-webkit-scrollbar-thumb {
            background: #D4AF37; 
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #b5952f; 
        }

        /* Component Classes */
        .btn-gold {
            background-color: #D4AF37;
            color: white;
            transition: all 0.3s ease;
        }
        .btn-gold:hover {
            background-color: #b5952f;
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .nav-item.active {
            border-left: 4px solid #D4AF37;
            background-color: #F3EFE5;
            color: #1F2937;
        }

        .card-select {
            transition: all 0.2s ease;
            border: 2px solid transparent;
        }
        .card-select.selected {
            border-color: #D4AF37;
            background-color: #FFFBEB;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade {
            animation: fadeIn 0.4s ease-out forwards;
        }

        /* Forbidden Term Badge */
        .forbidden-badge {
            background-color: #FEE2E2;
            color: #991B1B;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
        }
    </style>

    <!-- Application Structure Plan:
         Designed as a "Production Dashboard" mirroring the AutNew Factory workflow.
         1. Left Sidebar: "Production Pipeline" navigation tracking the 4 distinct phases (Input -> Intel -> Creative -> Export) + Monitor status.
         2. Main Canvas: Dynamic area that changes based on the active phase.
            - Phase 1 (Input): Forms for Data Ingestion.
            - Phase 2 (Intel): Visualizing the "Black Box" processing (Charts/Logs).
            - Phase 3 (Creative): The "Decision Room" for Strategy, Script, and Visuals.
            - Phase 4 (Export): Final delivery summary.
         3. Right Overlay: Collapsible "Manual/Diretrizes" to keep rules accessible without cluttering the workspace.
         Rationale: This structure separates "setup" from "execution" and "review", preventing cognitive overload while maintaining the logical flow of the factory.
    -->
    <!-- Visualization & Content Choices:
         - Phase 2: Uses Chart.js (Bar Chart) to visualize "Retention by Theme" (DNA Analyst). Goal: Show the user WHY specific creative choices will be made.
         - Phase 2: Uses a "Console Log" simulation to show backend processes (API calls). Goal: Transparency of the "Black Box".
         - Phase 3: Interactive Grid for Títulos/Thumbs/Script. Goal: Comparison and Selection.
         - Icons: FontAwesome used throughout for visual cues (No SVG).
         - Data Storage: JS Objects store mock data from the "Source Report" (forbidden words, script structure).
    -->
    <!-- CONFIRMATION: NO SVG graphics used. NO Mermaid JS used. -->

</head>
<body class="flex h-screen overflow-hidden">

    <!-- SIDEBAR NAVIGATION -->
    <aside class="w-64 bg-white border-r border-gray-200 flex flex-col shadow-sm z-20 hidden md:flex">
        <div class="p-6 border-b border-gray-100 flex items-center gap-3">
            <div class="w-10 h-10 bg-gray-900 rounded-lg flex items-center justify-center text-[#D4AF37]">
                <i class="fas fa-church text-xl"></i>
            </div>
            <div>
                <h1 class="text-lg font-bold text-gray-800 leading-none">AutNew</h1>
                <span class="text-xs text-[#D4AF37] font-bold tracking-widest uppercase">Factory V1</span>
            </div>
        </div>

        <nav class="flex-1 overflow-y-auto py-4">
            <div class="px-4 mb-2">
                <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Plan Run</p>
            </div>
            
            <a href="#" onclick="switchPhase(1)" id="nav-1" class="nav-item active flex items-center gap-3 px-6 py-3 text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                <i class="fas fa-file-import w-5 text-center"></i>
                1. Input & Gatilhos
            </a>
            <a href="#" onclick="switchPhase(2)" id="nav-2" class="nav-item flex items-center gap-3 px-6 py-3 text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                <i class="fas fa-brain w-5 text-center"></i>
                2. Inteligência (IA)
            </a>
            <a href="#" onclick="switchPhase(3)" id="nav-3" class="nav-item flex items-center gap-3 px-6 py-3 text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                <i class="fas fa-pen-nib w-5 text-center"></i>
                3. Sala de Criação
            </a>
            <a href="#" onclick="switchPhase(4)" id="nav-4" class="nav-item flex items-center gap-3 px-6 py-3 text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                <i class="fas fa-box-open w-5 text-center"></i>
                4. Entrega & Export
            </a>

            <div class="px-4 mt-8 mb-2">
                <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Gestão</p>
            </div>
            <a href="#" class="flex items-center gap-3 px-6 py-3 text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                <i class="fas fa-chart-line w-5 text-center"></i>
                Monitor de Cotas
            </a>
            <a href="#" class="flex items-center gap-3 px-6 py-3 text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                <i class="fas fa-youtube w-5 text-center"></i>
                Canal Conectado
            </a>
        </nav>

        <!-- API STATUS MONITOR -->
        <div class="p-4 bg-gray-50 border-t border-gray-200">
            <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold text-gray-500">MONITOR DE RECURSOS</span>
                <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            </div>
            <div class="space-y-2">
                <div class="flex justify-between text-xs text-gray-600">
                    <span>OpenAI API</span>
                    <span class="font-mono text-gray-800">$12.50 left</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-1.5">
                    <div class="bg-green-500 h-1.5 rounded-full" style="width: 80%"></div>
                </div>
                
                <div class="flex justify-between text-xs text-gray-600">
                    <span>Gemini 2.5 Pro</span>
                    <span class="font-mono text-gray-800">Active</span>
                </div>
                <div class="flex justify-between text-xs text-gray-600">
                    <span>YouTube Data</span>
                    <span class="font-mono text-gray-800">98% Quota</span>
                </div>
            </div>
        </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="flex-1 flex flex-col h-full overflow-hidden relative">
        
        <!-- HEADER -->
        <header class="bg-white border-b border-gray-200 px-8 py-4 flex justify-between items-center z-10">
            <div>
                <h2 class="text-xl font-bold text-gray-800 serif-font" id="header-title">Fase 1: Configuração & Gatilhos</h2>
                <p class="text-xs text-gray-500" id="header-desc">Defina a intenção e os dados de entrada para a fábrica.</p>
            </div>
            <div class="flex items-center gap-4">
                <button onclick="toggleGuidelines()" class="flex items-center gap-2 text-sm font-bold text-[#D4AF37] hover:text-[#b5952f] transition-colors border border-[#D4AF37] px-4 py-2 rounded-lg">
                    <i class="fas fa-book"></i> Diretrizes Mestre
                </button>
                <div class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-600">
                    <i class="fas fa-user"></i>
                </div>
            </div>
        </header>

        <!-- SCROLLABLE CONTENT AREA -->
        <div class="flex-1 overflow-y-auto p-8 relative">
            
            <!-- GUIDELINES SLIDE-OVER (Hidden by default) -->
            <div id="guidelines-panel" class="absolute top-0 right-0 h-full w-96 bg-white shadow-2xl transform translate-x-full transition-transform duration-300 z-50 overflow-y-auto border-l border-gray-200 p-6">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="serif-font text-xl font-bold text-[#D4AF37]">Manual de Identidade</h3>
                    <button onclick="toggleGuidelines()" class="text-gray-400 hover:text-red-500"><i class="fas fa-times text-xl"></i></button>
                </div>
                
                <div class="space-y-6 text-sm text-gray-600">
                    <div class="bg-red-50 p-4 rounded-lg border border-red-100">
                        <h4 class="font-bold text-red-700 mb-2 flex items-center gap-2"><i class="fas fa-ban"></i> LISTA NEGRA (Proibidos)</h4>
                        <div class="flex flex-wrap gap-2">
                            <span class="forbidden-badge">Blindar</span>
                            <span class="forbidden-badge">Escudo</span>
                            <span class="forbidden-badge">Chave</span>
                            <span class="forbidden-badge">Muralha</span>
                            <span class="forbidden-badge">"Se você sente..."</span>
                            <span class="forbidden-badge">"Respire fundo"</span>
                        </div>
                    </div>

                    <div>
                        <h4 class="font-bold text-gray-800 mb-2">🎨 Anatomia Thumb (60+)</h4>
                        <ul class="list-disc pl-4 space-y-1">
                            <li>Fontes <strong>Extra Bold</strong> e Grandes.</li>
                            <li>Alto contraste e clareza.</li>
                            <li>Rosto: Choque Sagrado ou Paz Profunda.</li>
                            <li>Nunca usar sorrisos genéricos.</li>
                        </ul>
                    </div>

                    <div>
                        <h4 class="font-bold text-gray-800 mb-2">📜 Arquitetura Roteiro</h4>
                        <ul class="list-disc pl-4 space-y-1">
                            <li><strong>0-30s:</strong> Abertura Magnética (Promessa).</li>
                            <li><strong>Meio:</strong> CTA Compartilhamento.</li>
                            <li><strong>Final:</strong> CTA Ebook + Grupo VIP.</li>
                            <li><strong>Total:</strong> ~1.600 palavras.</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- PHASE 1: INPUTS -->
            <section id="phase-1" class="max-w-4xl mx-auto animate-fade">
                <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-8 mb-6">
                    <div class="grid grid-cols-1 gap-6">
                        <!-- Competitor Link -->
                        <div>
                            <label class="block text-sm font-bold text-gray-700 mb-2">
                                <i class="fab fa-youtube text-red-600 mr-2"></i>Link do Concorrente (Referência)
                            </label>
                            <input type="text" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#D4AF37]" placeholder="https://youtube.com/watch?v=...">
                        </div>

                        <!-- History Upload -->
                        <div>
                            <label class="block text-sm font-bold text-gray-700 mb-2">
                                <i class="fas fa-table text-green-600 mr-2"></i>Planilha de Histórico (DNA do Canal)
                            </label>
                            <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:bg-gray-50 cursor-pointer transition-colors">
                                <i class="fas fa-cloud-upload-alt text-3xl text-gray-300 mb-2"></i>
                                <p class="text-sm text-gray-500">Arraste seu arquivo .csv ou .xlsx aqui</p>
                                <p class="text-xs text-[#D4AF37] font-bold mt-2">Mundo_da_Prece_Analytics_Nov.xlsx (Carregado)</p>
                            </div>
                        </div>

                        <!-- Intention -->
                        <div>
                            <label class="block text-sm font-bold text-gray-700 mb-2">
                                <i class="fas fa-bullseye text-blue-500 mr-2"></i>Intenção e Tema do Vídeo
                            </label>
                            <textarea rows="3" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#D4AF37]" placeholder="Ex: Oração da manhã focada em gratidão e quebra de maldições financeiras. Tom solene mas esperançoso."></textarea>
                        </div>

                        <!-- Manual Transcript Fallback -->
                        <div class="border border-gray-200 rounded-lg p-4 bg-gray-50">
                            <button onclick="toggleTranscription()" class="flex justify-between items-center w-full text-left">
                                <span class="text-sm font-bold text-gray-600 flex items-center gap-2">
                                    <i class="fas fa-keyboard"></i> Transcrição Manual (Opcional - Bifurcação)
                                </span>
                                <i id="trans-icon" class="fas fa-chevron-down text-gray-400 transition-transform"></i>
                            </button>
                            <div id="manual-transcript-area" class="hidden mt-4">
                                <textarea rows="4" class="w-full bg-white border border-gray-200 rounded-lg px-4 py-2 text-sm" placeholder="Cole o texto aqui se o YouTube bloquear a extração automática..."></textarea>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="flex justify-end">
                    <button onclick="startSimulation()" class="btn-gold px-8 py-4 rounded-xl font-bold shadow-lg flex items-center gap-3 text-lg">
                        <i class="fas fa-cogs"></i> INICIAR PLAN RUN
                    </button>
                </div>
            </section>

            <!-- PHASE 2: INTELLIGENCE MONITOR -->
            <section id="phase-2" class="max-w-5xl mx-auto hidden animate-fade">
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                    
                    <!-- Console Log Simulation -->
                    <div class="bg-[#1e1e1e] rounded-xl p-6 shadow-md text-green-400 font-mono text-xs overflow-hidden h-64 lg:col-span-1 border border-gray-700 relative">
                        <div class="absolute top-2 right-2 text-gray-500 text-[10px]">TERMINAL: ACTIVE</div>
                        <div id="console-output" class="space-y-2">
                            <p>> Inicializando AutNew Factory V1...</p>
                        </div>
                    </div>

                    <!-- DNA Analyst Chart -->
                    <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 lg:col-span-2">
                        <h3 class="text-sm font-bold text-gray-600 uppercase mb-4 flex items-center gap-2">
                            <i class="fas fa-dna text-[#D4AF37]"></i> Análise de DNA do Canal (Retenção)
                        </h3>
                        <!-- Chart Container -->
                        <div class="chart-container">
                            <canvas id="retentionChart"></canvas>
                        </div>
                    </div>
                </div>

                <!-- Extraction Summary -->
                <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 opacity-50 transition-opacity duration-1000" id="extraction-card">
                    <div class="flex items-center gap-4 mb-4 border-b border-gray-100 pb-4">
                        <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center text-blue-600">
                            <i class="fas fa-search"></i>
                        </div>
                        <div>
                            <h3 class="font-bold text-gray-800">Mineração de Dados (Search Web)</h3>
                            <p class="text-xs text-gray-500">Extração Textual Pura (Sem processamento de mídia)</p>
                        </div>
                    </div>
                    <div class="grid grid-cols-3 gap-4 text-center">
                        <div class="p-3 bg-gray-50 rounded-lg">
                            <p class="text-xs text-gray-400 uppercase">Tokens Texto</p>
                            <p class="font-bold text-gray-800 text-xl" id="token-count">0</p>
                        </div>
                        <div class="p-3 bg-gray-50 rounded-lg">
                            <p class="text-xs text-gray-400 uppercase">Fato Teológico</p>
                            <p class="font-bold text-green-600 text-sm mt-1">Salmo 23 (Original)</p>
                        </div>
                        <div class="p-3 bg-gray-50 rounded-lg">
                            <p class="text-xs text-gray-400 uppercase">Status</p>
                            <p class="font-bold text-[#D4AF37] text-sm mt-1" id="process-status">Aguardando...</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- PHASE 3: CREATIVE ROOM -->
            <section id="phase-3" class="max-w-7xl mx-auto hidden animate-fade">
                <div class="grid grid-cols-12 gap-6 h-[calc(100vh-140px)]">
                    
                    <!-- Left Col: Strategy (Titles & Thumbs) -->
                    <div class="col-span-4 flex flex-col gap-4 overflow-y-auto pr-2">
                        
                        <!-- Titles -->
                        <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                            <h3 class="text-xs font-bold text-gray-400 uppercase mb-3 flex justify-between items-center">
                                1. Selecione o Título Viral
                                <button class="text-[#D4AF37] hover:text-[#b5952f]"><i class="fas fa-sync"></i></button>
                            </h3>
                            <div class="space-y-3" id="titles-container">
                                <!-- Titles injected via JS -->
                            </div>
                        </div>

                        <!-- Thumbnail Concepts -->
                        <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex-1">
                            <h3 class="text-xs font-bold text-gray-400 uppercase mb-3">2. Estratégia Visual (Thumb)</h3>
                            <div class="space-y-3" id="thumbs-container">
                                <!-- Thumb concepts injected via JS -->
                            </div>
                            
                            <!-- Prompt Preview -->
                            <div class="mt-4 p-3 bg-gray-900 rounded-lg border border-gray-700">
                                <p class="text-[10px] text-gray-400 uppercase mb-1">Prompt Imagen 3 (EN)</p>
                                <p class="text-xs text-gray-300 italic mono-font" id="thumb-prompt-preview">Select a concept above...</p>
                            </div>
                        </div>
                    </div>

                    <!-- Middle/Right Col: Script Editor -->
                    <div class="col-span-8 flex flex-col h-full">
                        <div class="bg-white rounded-xl shadow-sm border border-gray-100 flex-1 flex flex-col overflow-hidden">
                            <!-- Toolbar -->
                            <div class="p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
                                <div class="flex items-center gap-2">
                                    <span class="text-sm font-bold text-gray-700">Editor de Roteiro (Verbatim)</span>
                                    <span class="text-xs bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded-full">~1.600 palavras</span>
                                </div>
                                <div class="flex gap-2">
                                    <button class="text-gray-400 hover:text-gray-600 px-2"><i class="fas fa-undo"></i></button>
                                    <button class="text-gray-400 hover:text-gray-600 px-2"><i class="fas fa-copy"></i></button>
                                </div>
                            </div>
                            
                            <!-- Text Area -->
                            <div class="flex-1 p-0 relative">
                                <textarea class="w-full h-full p-8 resize-none focus:outline-none serif-font text-lg leading-loose text-gray-700" id="script-editor"></textarea>
                                <!-- Floating CTA Action -->
                                <div class="absolute bottom-6 right-6">
                                    <button onclick="switchPhase(4)" class="btn-gold px-6 py-3 rounded-xl font-bold shadow-lg flex items-center gap-2">
                                        <i class="fas fa-check-circle"></i> APROVAR E GERAR
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- PHASE 4: EXPORT -->
            <section id="phase-4" class="max-w-2xl mx-auto hidden animate-fade text-center pt-12">
                <div class="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6 shadow-sm">
                    <i class="fas fa-check text-4xl text-green-600"></i>
                </div>
                <h2 class="text-3xl font-bold text-gray-800 serif-font mb-2">Kit de Produção Pronto!</h2>
                <p class="text-gray-500 mb-8">Todos os ativos foram validados pelo manual e gerados com sucesso.</p>

                <div class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden text-left mb-8">
                    <div class="p-4 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
                        <span class="font-bold text-gray-700">Pacote de Entrega (Google Drive)</span>
                        <span class="text-xs text-gray-400">ID: #AN-2026-001</span>
                    </div>
                    <div class="p-6 space-y-4">
                        <div class="flex items-center gap-4">
                            <div class="w-10 h-10 bg-blue-100 rounded flex items-center justify-center text-blue-600"><i class="fas fa-file-word"></i></div>
                            <div class="flex-1">
                                <h4 class="font-bold text-gray-800 text-sm">Roteiro_Final_Vids.docx</h4>
                                <p class="text-xs text-gray-500">Formatado para Google Vids (Speaker labels)</p>
                            </div>
                            <button class="text-gray-400 hover:text-[#D4AF37]"><i class="fas fa-download"></i></button>
                        </div>
                        <div class="flex items-center gap-4">
                            <div class="w-10 h-10 bg-purple-100 rounded flex items-center justify-center text-purple-600"><i class="fas fa-image"></i></div>
                            <div class="flex-1">
                                <h4 class="font-bold text-gray-800 text-sm">Thumbnail_HD_Imagen3.png</h4>
                                <p class="text-xs text-gray-500">1280x720 • Alta Resolução</p>
                            </div>
                            <button class="text-gray-400 hover:text-[#D4AF37]"><i class="fas fa-download"></i></button>
                        </div>
                        <div class="flex items-center gap-4">
                            <div class="w-10 h-10 bg-yellow-100 rounded flex items-center justify-center text-yellow-600"><i class="fas fa-tags"></i></div>
                            <div class="flex-1">
                                <h4 class="font-bold text-gray-800 text-sm">Metadados_SEO.txt</h4>
                                <p class="text-xs text-gray-500">Título, Descrição, Tags Otimizadas</p>
                            </div>
                            <button class="text-gray-400 hover:text-[#D4AF37]"><i class="fas fa-download"></i></button>
                        </div>
                    </div>
                </div>

                <div class="flex justify-center gap-4">
                    <button onclick="location.reload()" class="px-6 py-3 rounded-lg border border-gray-300 text-gray-600 hover:bg-gray-50 font-medium">
                        Novo Vídeo
                    </button>
                    <button class="btn-gold px-8 py-3 rounded-lg font-bold shadow-md flex items-center gap-2">
                        <i class="fab fa-google-drive"></i> Abrir no Drive
                    </button>
                </div>
            </section>

        </div>
    </main>

    <!-- JAVASCRIPT LOGIC -->
    <script>
        // --- DATA STORE (Simulating Source Report Data) ---
        const factoryData = {
            titles: [
                { id: 1, text: "A Oração da Manhã que Quebra Cadeias Invisíveis", tag: "CURIOSIDADE", chars: 55 },
                { id: 2, text: "Salmo 91: O Segredo Oculto para Proteger sua Casa", tag: "BENEFÍCIO", chars: 52 },
                { id: 3, text: "Angústia no Peito? Faça Esta Prece de 3 Minutos", tag: "URGÊNCIA", chars: 48 }
            ],
            thumbs: [
                { id: 1, name: "Choque Sagrado", desc: "Close-up rosto idoso, lágrimas de alívio, luz dourada.", prompt: "Cinematic close-up, elderly face looking up, divine light, warm tones, high contrast, 8k, photorealistic." },
                { id: 2, name: "Mãos de Poder", desc: "Mãos calejadas orando, raio rompendo tempestade.", prompt: "Worker hands praying, dramatic storm clouds background, single sun ray breaking through, hopeful atmosphere." },
                { id: 3, name: "A Porta Aberta", desc: "Silhueta saindo do túnel para luz em cruz.", prompt: "Silhouette figure walking from dark tunnel into blinding cross-shaped light, ethereal, spiritual journey." }
            ],
            scriptTemplate: `[ABERTURA MAGNÉTICA 0:00]
(Tom: Calmo, firme)
Amado irmão, amada irmã. Se o seu coração acordou hoje apertado, sentindo que os caminhos estão fechados, esta oração encontrou você no momento certo.

[PARTICIPAÇÃO IMEDIATA]
Já clique no botão de inscrever-se e deixe seu "Amém" nos comentários. Ao fazer isso, você materializa sua fé...

[DESENVOLVIMENTO IMERSIVO]
Hoje vamos clamar a providência divina baseada no mistério do Salmo 23. Você sabia que quando Davi diz "Preparas uma mesa perante mim", ele estava cercado por inimigos no deserto?

(A oração continua com profundidade teológica extraída da pesquisa...)

[PONTO DE REENGAJAMENTO]
Sinta essa paz invadindo seu lar. Agora, pense em 3 pessoas que precisam dessa mesma paz. Compartilhe este vídeo com elas agora no WhatsApp. Seja um Canal de Luz.

[CTA FINAL - OFERTA]
Como prometido, para proteger sua família, preparei o E-book "Orações da Família Brasileira". O link está fixado no primeiro comentário. Entre também no Grupo VIP.`
        };

        // --- CORE FUNCTIONS ---

        function toggleTranscription() {
            const area = document.getElementById('manual-transcript-area');
            const icon = document.getElementById('trans-icon');
            area.classList.toggle('hidden');
            icon.classList.toggle('rotate-180');
        }

        function toggleGuidelines() {
            const panel = document.getElementById('guidelines-panel');
            if (panel.classList.contains('translate-x-full')) {
                panel.classList.remove('translate-x-full');
            } else {
                panel.classList.add('translate-x-full');
            }
        }

        function switchPhase(phaseNum) {
            // Hide all phases
            [1, 2, 3, 4].forEach(p => document.getElementById(`phase-${p}`).classList.add('hidden'));
            
            // Show active phase
            const activeSection = document.getElementById(`phase-${phaseNum}`);
            activeSection.classList.remove('hidden');
            activeSection.classList.add('animate-fade');

            // Update Header
            const titles = [
                "Fase 1: Configuração & Gatilhos",
                "Fase 2: Processamento Inteligente",
                "Fase 3: Sala de Criação Estratégica",
                "Fase 4: Entrega Final"
            ];
            const descs = [
                "Defina a intenção e os dados de entrada para a fábrica.",
                "Gemini 2.5 Pro + Code Execution em andamento...",
                "Aprovação Humana Obrigatória (Review with User).",
                "Kit de produção gerado e salvo no Drive."
            ];
            document.getElementById('header-title').innerText = titles[phaseNum-1];
            document.getElementById('header-desc').innerText = descs[phaseNum-1];

            // Update Sidebar
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active', 'border-l-4', 'border-[#D4AF37]', 'bg-[#F3EFE5]'));
            const activeNav = document.getElementById(`nav-${phaseNum}`);
            activeNav.classList.add('active');
        }

        function startSimulation() {
            switchPhase(2);
            
            // Simulate Console Logs
            const logs = [
                "> Conectando Gemini 2.5 Pro...",
                "> Minerando URL (Search Web - No Images)...",
                "> Extraindo Transcrição Textual...",
                "> Executando DNA Analyst (Python)...",
                "> Lendo Asset: @Diretrizes_Mestre...",
                "> Gerando Roteiro (Gemini 3 Pro)..."
            ];
            
            let i = 0;
            const logContainer = document.getElementById('console-output');
            const interval = setInterval(() => {
                if (i < logs.length) {
                    const p = document.createElement('p');
                    p.innerText = logs[i];
                    logContainer.appendChild(p);
                    i++;
                } else {
                    clearInterval(interval);
                    document.getElementById('process-status').innerText = "Concluído";
                    document.getElementById('process-status').classList.remove('text-[#D4AF37]');
                    document.getElementById('process-status').classList.add('text-green-500');
                    document.getElementById('token-count').innerText = "14,502";
                    document.getElementById('extraction-card').classList.remove('opacity-50');
                    
                    // Delay before moving to Creative Room
                    setTimeout(() => {
                        populateCreativeRoom();
                        switchPhase(3);
                    }, 1500);
                }
            }, 800);

            // Render Chart
            renderRetentionChart();
        }

        function renderRetentionChart() {
            const ctx = document.getElementById('retentionChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Oração Manhã', 'Cura', 'Salmos', 'Mensagem Noite', 'Motivacional'],
                    datasets: [{
                        label: 'Retenção Média (%)',
                        data: [65, 42, 58, 48, 30],
                        backgroundColor: [
                            '#D4AF37', '#E5E7EB', '#FCD34D', '#E5E7EB', '#E5E7EB'
                        ],
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false, // Vital for container responsiveness
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: { beginAtZero: true, grid: { color: '#f3f4f6' } },
                        x: { grid: { display: false } }
                    }
                }
            });
        }

        function populateCreativeRoom() {
            // Populate Titles
            const titleContainer = document.getElementById('titles-container');
            titleContainer.innerHTML = '';
            factoryData.titles.forEach((t, index) => {
                titleContainer.innerHTML += `
                    <div onclick="selectTitle(this)" class="card-select p-3 border rounded-lg cursor-pointer hover:bg-yellow-50 ${index === 0 ? 'selected' : ''}">
                        <div class="flex justify-between items-start">
                            <p class="font-bold text-gray-800 text-sm leading-tight">${t.text}</p>
                            ${index === 0 ? '<i class="fas fa-check-circle text-[#D4AF37]"></i>' : ''}
                        </div>
                        <div class="flex justify-between mt-2">
                            <span class="text-[10px] font-bold text-gray-400 bg-gray-100 px-1 rounded">${t.tag}</span>
                            <span class="text-[10px] text-gray-400">${t.chars} chars</span>
                        </div>
                    </div>
                `;
            });

            // Populate Thumbs
            const thumbContainer = document.getElementById('thumbs-container');
            thumbContainer.innerHTML = '';
            factoryData.thumbs.forEach((t, index) => {
                thumbContainer.innerHTML += `
                    <div onclick="selectThumb(this, '${t.prompt}')" class="card-select p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-yellow-50 ${index === 0 ? 'selected' : ''}">
                        <span class="font-bold text-gray-700 block text-xs mb-1">${t.name}</span>
                        <p class="text-[10px] text-gray-500 mb-1">${t.desc}</p>
                    </div>
                `;
            });

            // Set Script
            document.getElementById('script-editor').value = factoryData.scriptTemplate;
            // Set Initial Prompt
            document.getElementById('thumb-prompt-preview').innerText = factoryData.thumbs[0].prompt;
        }

        // Selection Logic
        window.selectTitle = function(el) {
            document.querySelectorAll('#titles-container .card-select').forEach(c => {
                c.classList.remove('selected');
                const icon = c.querySelector('.fa-check-circle');
                if(icon) icon.remove();
            });
            el.classList.add('selected');
            el.querySelector('.flex').innerHTML += '<i class="fas fa-check-circle text-[#D4AF37]"></i>';
        }

        window.selectThumb = function(el, prompt) {
            document.querySelectorAll('#thumbs-container .card-select').forEach(c => c.classList.remove('selected'));
            el.classList.add('selected');
            document.getElementById('thumb-prompt-preview').innerText = prompt;
        }

    </script>
</body>
</html>
