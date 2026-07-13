import streamlit as str
import google.generativeai as genai
import random

# Forçar layout limpo e responsivo
str.set_page_config(page_title="Galo Mestre Pro", layout="wide", initial_sidebar_state="collapsed")

# --- DESIGN PREMIUM (CSS INJECTION) ---
str.markdown("""
    <style>
    [data-testid="stHeader"] {background-color: rgba(0,0,0,0);}
    .main .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    
    /* Cabeçalho Galo Mestre */
    .header-container {
        background: linear-gradient(90deg, #134e3a 0%, #1a3a2a 100%);
        padding: 20px;
        border-radius: 0px 0px 15px 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    .header-title {
        color: #f3e5ab;
        font-family: 'Georgia', serif;
        font-size: 28px;
        font-weight: bold;
        letter-spacing: 2px;
        margin: 0;
    }
    .header-subtitle {
        color: #ffffff;
        font-size: 11px;
        letter-spacing: 3px;
        margin-top: 5px;
    }
    
    /* Cartões de Métricas */
    .metric-card {
        background-color: #f7f9f8;
        border: 1px solid #e1e8e5;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .metric-val {
        font-size: 36px;
        font-weight: bold;
        color: #111111;
        margin: 10px 0px;
    }
    
    /* Caixa de Dicas do Dia */
    .tip-box {
        background-color: #f4ebd0;
        border-radius: 16px;
        padding: 18px;
        border-left: 5px solid #d4af37;
        margin: 20px 0px;
        color: #4a3b1a;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. CABEÇALHO INTEGRADO ---
str.markdown("""
    <div class="header-container">
        <div class="header-title">🐓 GALO MESTRE</div>
        <div class="header-subtitle">GESTÃO DE ALTA PERFORMANCE</div>
    </div>
""", unsafe_allow_html=True)

# --- 2. BARRA DE NAVEGAÇÃO DE MENU (TABS COM ÍCONES) ---
menu_tabs = str.tabs(["🛖 Galpão", "🛡️ Biosegurança", "🌡️ Clima", "🏥 Saúde", "🥚 Produção", "💰 Financeiro", "🔔 Alertas", "🤖 IA Mestre"])

# --- CONTEÚDO PRINCIPAL ---
with menu_tabs[0]:
    
    # Cartão Principal
    str.markdown("""
        <div class="metric-card">
            <span style='font-size: 30px;'>📏</span>
            <div style='color: #666666; font-weight: bold; font-size: 14px; margin-top: 5px;'>ÁREA TOTAL</div>
            <div class="metric-val">10.0 <span style='font-size: 20px;'>m²</span></div>
            <div style='color: #555555; font-size: 13px;'>Densidade de 10 aves/m²</div>
        </div>
    """, unsafe_allow_html=True)

    # Caixa Amarela de Dica Dinâmica
    str.markdown("""
        <div class="tip-box">
            <strong>💡 Dica do Galo Mestre:</strong> Certifique-se de que os equipamentos estejam distribuídos de forma 
            que nenhuma ave precise caminhar mais de 3 metros para encontrar água ou ração.
        </div>
    """, unsafe_allow_html=True)

    str.markdown("---")
    str.subheader("🎮 Atuadores Automáticos & Sensores")
    
    col_act1, col_act2 = str.columns(2)
    with col_act1:
        lock_btn = str.button("🔓 Desbloquear Tranca Automática" if str.session_state.get('coop_lock', True) else "🔒 Ativar Fechadura de Segurança")
        if lock_btn:
            str.session_state['coop_lock'] = not str.session_state.get('coop_lock', True)
        str.info(f"Estado da Fechadura: {'Trancada (Modo Seguro)' if str.session_state.get('coop_lock', True) else 'Aberta (Acesso Livre)'}")
        
    with col_act2:
        feeder_toggle = str.toggle("Ligar Motores dos Alimentadores", value=False)
        str.info(f"Alimentadores: {'EM EXECUÇÃO' if feeder_toggle else 'DESLIGADOS'}")

with menu_tabs[7]: # Aba IA Mestre
    str.subheader("🤖 Diagnóstico de IA do Galo Mestre")
    
    api_key_env = str.secrets.get("GOOGLE_API_KEY", None)
    
    if not api_key_env:
        str.error("Falta Configurar! A GOOGLE_API_KEY não foi inserida no gestor de Secrets do Streamlit.")
    else:
        str.success("Chave API detetada e pronta para execução.")
        if str.button("Executar Auditoria Geral com Gemini"):
            try:
                genai.configure(api_key=api_key_env)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                with str.spinner("Galo Mestre gerando relatório de alta performance..."):
                    response = model.generate_content("Dê 3 recomendações comerciais rápidas e avançadas para um galpão de avicultura com 10m2 e densidade de 10 aves por metro quadrado.")
                    str.markdown(response.text)
            except Exception as e:
                str.error(f"Erro ao chamar a IA. Detalhes: {e}")
