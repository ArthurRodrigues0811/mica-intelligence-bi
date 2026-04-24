import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Mica Chocolates - BI Premium",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PALETA DE CORES - TEMA DARK POWER BI
# ============================================================================
COLORS = {
    'bg_primary':    '#1a1a2e',
    'bg_card':       '#16213e',
    'bg_sidebar':    '#0f3460',
    'accent1':       '#e94560',
    'accent2':       '#c77dff',
    'accent3':       '#48cae4',
    'accent4':       '#f4a261',
    'accent5':       '#06d6a0',
    'text_primary':  '#ffffff',
    'text_secondary':'#a0aec0',
    'border':        '#2d3748',
    'positive':      '#06d6a0',
    'negative':      '#e94560',
    'warning':       '#f4a261',
    'chart_bg':      '#1a1a2e',
    'grid':          '#2d3748',
}

PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor=COLORS['bg_card'],
        plot_bgcolor=COLORS['bg_primary'],
        font=dict(family="Segoe UI, Arial", color=COLORS['text_primary'], size=12),
        title=dict(font=dict(size=14, color=COLORS['text_primary'])),
        xaxis=dict(
            gridcolor=COLORS['grid'],
            linecolor=COLORS['border'],
            tickcolor=COLORS['text_secondary'],
            tickfont=dict(color=COLORS['text_secondary'], size=11),
        ),
        yaxis=dict(
            gridcolor=COLORS['grid'],
            linecolor=COLORS['border'],
            tickcolor=COLORS['text_secondary'],
            tickfont=dict(color=COLORS['text_secondary'], size=11),
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text_secondary']),
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        hoverlabel=dict(
            bgcolor=COLORS['bg_card'],
            bordercolor=COLORS['border'],
            font=dict(color=COLORS['text_primary']),
        ),
    )
)

BAR_COLORS = [COLORS['accent2'], COLORS['accent3'], COLORS['accent1'],
              COLORS['accent4'], COLORS['accent5'], '#f72585']

# ============================================================================
# CSS CUSTOMIZADO - POWER BI DARK THEME
# ============================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&display=swap');

    /* Reset geral */
    html, body, [class*="css"] {{
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Background principal */
    .stApp {{
        background-color: {COLORS['bg_primary']};
        color: {COLORS['text_primary']};
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['bg_sidebar']} 0%, {COLORS['bg_primary']} 100%);
        border-right: 1px solid {COLORS['border']};
    }}
    [data-testid="stSidebar"] * {{
        color: {COLORS['text_primary']} !important;
    }}

    /* Títulos */
    h1, h2, h3, h4 {{
        color: {COLORS['text_primary']} !important;
        font-weight: 600 !important;
    }}

    /* Métricas */
    [data-testid="metric-container"] {{
        background: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 16px 20px !important;
        border-left: 3px solid {COLORS['accent2']};
        transition: border-left-color 0.3s;
    }}
    [data-testid="metric-container"]:hover {{
        border-left-color: {COLORS['accent1']};
    }}
    [data-testid="metric-container"] label {{
        color: {COLORS['text_secondary']} !important;
        font-size: 12px !important;
        font-weight: 400 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    [data-testid="metric-container"] [data-testid="stMetricValue"] {{
        color: {COLORS['text_primary']} !important;
        font-size: 26px !important;
        font-weight: 700 !important;
    }}
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {{
        font-size: 12px !important;
    }}
    [data-testid="metric-container"] [data-testid="stMetricDelta"] svg {{
        display: none;
    }}

    /* Cards de seção */
    .section-card {{
        background: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
    }}

    /* Dataframes */
    [data-testid="stDataFrame"] {{
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        overflow: hidden;
    }}

    /* Selectbox e multiselect */
    [data-testid="stSelectbox"] > div,
    [data-testid="stMultiSelect"] > div {{
        background: {COLORS['bg_card']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 6px !important;
        color: {COLORS['text_primary']} !important;
    }}

    /* Alertas */
    .stAlert {{
        border-radius: 8px;
        border: none;
    }}

    /* Radio buttons na sidebar */
    [data-testid="stRadio"] > div {{
        gap: 4px;
    }}
    [data-testid="stRadio"] label {{
        background: rgba(255,255,255,0.05);
        border-radius: 6px;
        padding: 8px 12px !important;
        transition: background 0.2s;
        width: 100%;
        cursor: pointer;
    }}
    [data-testid="stRadio"] label:hover {{
        background: rgba(255,255,255,0.1);
    }}

    /* Separadores */
    hr {{
        border-color: {COLORS['border']} !important;
        margin: 20px 0 !important;
    }}

    /* KPI badge */
    .kpi-badge {{
        display: inline-block;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}
    .kpi-pos {{ background: rgba(6,214,160,0.15); color: {COLORS['positive']}; }}
    .kpi-neg {{ background: rgba(233,69,96,0.15);  color: {COLORS['negative']}; }}
    .kpi-warn {{ background: rgba(244,162,97,0.15); color: {COLORS['warning']}; }}

    /* Título da página */
    .page-title {{
        font-size: 24px;
        font-weight: 700;
        color: {COLORS['text_primary']};
        margin-bottom: 4px;
    }}
    .page-subtitle {{
        font-size: 13px;
        color: {COLORS['text_secondary']};
        margin-bottom: 24px;
    }}

    /* Insight cards */
    .insight-card {{
        background: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 10px;
        font-size: 13px;
        line-height: 1.5;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: {COLORS['bg_primary']}; }}
    ::-webkit-scrollbar-thumb {{ background: {COLORS['border']}; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {COLORS['text_secondary']}; }}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# GERADOR DE DADOS SIMULADOS
# ============================================================================
@st.cache_data
def gerar_dados_vendas():
    np.random.seed(42)
    datas = pd.date_range(start='2024-01-01', end='2026-04-24', freq='D')
    produtos = ['Dark 70%', 'Leite Clássico', 'Branco Premium', 'Recheado Morango', 'Nibs Crocante', 'Trufa Gourmet']
    clientes_tipos = ['Varejo', 'Distribuidor', 'E-commerce', 'Corporate']

    dados = []
    for _ in range(1500):
        data = pd.Timestamp(np.random.choice(datas))
        produto = np.random.choice(produtos)
        cliente = np.random.choice(clientes_tipos)
        preco_unitario = np.random.uniform(12, 85)
        quantidade = np.random.randint(10, 500)
        mes = data.month
        if mes in [3, 4, 12]:
            quantidade = int(quantidade * np.random.uniform(1.3, 1.8))
        mes_str = data.strftime('%Y-%m')
        dados.append({
            'data': data, 'produto': produto, 'cliente_tipo': cliente,
            'preco_unitario': preco_unitario, 'quantidade': quantidade,
            'receita': preco_unitario * quantidade, 'mes': mes_str,
            'semana': data.isocalendar()[1], 'ano': data.year,
        })
    return pd.DataFrame(dados)

@st.cache_data
def gerar_dados_estoque():
    np.random.seed(42)
    produtos = ['Dark 70%', 'Leite Clássico', 'Branco Premium', 'Recheado Morango', 'Nibs Crocante', 'Trufa Gourmet']
    dados = []
    for produto in produtos:
        quantidade = np.random.randint(500, 5000)
        valor_unitario = np.random.uniform(12, 85)
        valor_total = quantidade * valor_unitario
        ruptura = 'SIM' if np.random.random() < 0.15 else 'NÃO'
        dados.append({
            'produto': produto, 'quantidade': quantidade,
            'valor_unitario': valor_unitario, 'valor_total': valor_total,
            'giro_dias': np.random.randint(15, 60), 'ruptura': ruptura,
            'perda_percentual': np.random.uniform(0, 5),
            'perda_valor': valor_total * np.random.uniform(0, 0.05)
        })
    return pd.DataFrame(dados)

@st.cache_data
def gerar_dados_producao():
    np.random.seed(42)
    datas = pd.date_range(start='2024-01-01', end='2026-04-24', freq='D')
    produtos = ['Dark 70%', 'Leite Clássico', 'Branco Premium', 'Recheado Morango', 'Nibs Crocante', 'Trufa Gourmet']
    dados = []
    for _ in range(800):
        data = pd.Timestamp(np.random.choice(datas))
        produto = np.random.choice(produtos)
        volume = np.random.randint(100, 2000)
        horas_trabalho = np.random.uniform(2, 16)
        custo_hora = 45
        mes_str = data.strftime('%Y-%m')
        dados.append({
            'data': data, 'produto': produto, 'volume_produzido': volume,
            'horas_trabalhadas': horas_trabalho, 'custo_hora': custo_hora,
            'custo_total': horas_trabalho * custo_hora,
            'custo_por_unidade': (horas_trabalho * custo_hora) / volume, 'mes': mes_str,
        })
    return pd.DataFrame(dados)

@st.cache_data
def gerar_dados_financeiro():
    np.random.seed(42)
    meses = pd.date_range(start='2024-01-01', end='2026-04-24', freq='MS')
    dados = []
    receita_base = 50000
    for mes in meses:
        receita = receita_base * np.random.uniform(0.85, 1.4)
        custo_producao = receita * np.random.uniform(0.35, 0.45)
        despesas_operacionais = receita * np.random.uniform(0.15, 0.25)
        lucro_bruto = receita - custo_producao
        lucro_liquido = lucro_bruto - despesas_operacionais
        mes_str = pd.Timestamp(mes).strftime('%Y-%m')
        dados.append({
            'mes': mes_str, 'receita': receita,
            'custo_producao': custo_producao, 'despesas_operacionais': despesas_operacionais,
            'lucro_bruto': lucro_bruto, 'lucro_liquido': lucro_liquido,
            'margem_bruta': (lucro_bruto / receita) * 100,
            'margem_liquida': (lucro_liquido / receita) * 100,
        })
    return pd.DataFrame(dados)

@st.cache_data
def gerar_dados_clientes():
    np.random.seed(42)
    clientes = [f'Cliente_{i:02d}' for i in range(1, 51)]
    dados = []
    for cliente in clientes:
        receita_anual = np.random.uniform(5000, 500000)
        ticket_medio = np.random.uniform(500, 5000)
        num_pedidos = int(receita_anual / ticket_medio)
        dados.append({
            'cliente': cliente, 'receita_anual': receita_anual,
            'ticket_medio': ticket_medio, 'num_pedidos': num_pedidos,
            'canal': np.random.choice(['Varejo', 'Distribuidor', 'E-commerce', 'Corporate']),
            'otif': np.random.uniform(0.80, 1.0) * 100,
        })
    return pd.DataFrame(dados)

# Carregar dados
df_vendas    = gerar_dados_vendas()
df_estoque   = gerar_dados_estoque()
df_producao  = gerar_dados_producao()
df_financeiro = gerar_dados_financeiro()
df_clientes  = gerar_dados_clientes()


# ============================================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================================
def fmt_brl(valor):
    return f"R$ {valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_pct(valor):
    return f"{valor:.1f}%"

def apply_template(fig, height=340):
    fig.update_layout(
        paper_bgcolor=COLORS['bg_card'],
        plot_bgcolor=COLORS['bg_primary'],
        font=dict(family="Segoe UI, Arial", color=COLORS['text_primary'], size=11),
        height=height,
        margin=dict(l=10, r=10, t=36, b=10),
        xaxis=dict(gridcolor=COLORS['grid'], linecolor=COLORS['border'],
                   tickfont=dict(color=COLORS['text_secondary'], size=10), showgrid=True),
        yaxis=dict(gridcolor=COLORS['grid'], linecolor=COLORS['border'],
                   tickfont=dict(color=COLORS['text_secondary'], size=10), showgrid=True),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=COLORS['text_secondary'], size=10),
                    orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hoverlabel=dict(bgcolor='#0f3460', bordercolor=COLORS['border'],
                        font=dict(color=COLORS['text_primary'], size=11)),
    )
    return fig

def section_title(title, subtitle=""):
    st.markdown(f"""
    <div style="margin-bottom:12px; border-bottom:1px solid {COLORS['border']}; padding-bottom:8px;">
        <span style="font-size:14px; font-weight:600; color:{COLORS['text_primary']};">{title}</span>
        {"<br><span style='font-size:11px; color:"+COLORS['text_secondary']+"'>"+subtitle+"</span>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)

def kpi_delta(valor, positivo_bom=True):
    cor = COLORS['positive'] if valor >= 0 else COLORS['negative']
    if not positivo_bom:
        cor = COLORS['negative'] if valor >= 0 else COLORS['positive']
    seta = "▲" if valor >= 0 else "▼"
    return f'<span style="color:{cor}; font-size:12px; font-weight:600;">{seta} {abs(valor):.1f}%</span>'


# ============================================================================
# INSIGHTS AUTOMÁTICOS
# ============================================================================
def gerar_insights_vendas():
    insights = []
    vpp = df_vendas.groupby('produto')['receita'].sum()
    melhor = vpp.idxmax()
    insights.append(f"🎯 <b>Melhor produto:</b> {melhor} — {fmt_brl(vpp[melhor])}")
    vendas_mes = df_vendas.groupby('mes')['receita'].sum()
    if len(vendas_mes) > 1:
        cresc = ((vendas_mes.iloc[-1] - vendas_mes.iloc[-2]) / vendas_mes.iloc[-2]) * 100
        emoji = "📈" if cresc > 0 else "📉"
        insights.append(f"{emoji} <b>Crescimento MoM:</b> {cresc:+.1f}%")
    melhor_canal = df_vendas.groupby('cliente_tipo')['receita'].sum().idxmax()
    insights.append(f"🛍️ <b>Melhor canal:</b> {melhor_canal}")
    return insights

def gerar_insights_estoque():
    insights = []
    rupturas = df_estoque[df_estoque['ruptura'] == 'SIM']
    if len(rupturas) > 0:
        insights.append(f"⚠️ <b>{len(rupturas)} produto(s) em ruptura!</b>")
        for _, row in rupturas.iterrows():
            insights.append(f"&nbsp;&nbsp;↳ {row['produto']}: impacto ~{fmt_brl(row['valor_total']/10)}/mês")
    val = df_estoque['valor_total'].sum()
    insights.append(f"💰 <b>Capital em estoque:</b> {fmt_brl(val)}")
    perda = df_estoque['perda_valor'].sum()
    insights.append(f"📉 <b>Perda estimada:</b> {fmt_brl(perda)}")
    return insights

def gerar_insights_financeiro():
    insights = []
    ul = df_financeiro.iloc[-1]
    insights.append(f"📊 <b>Margem bruta:</b> {ul['margem_bruta']:.1f}%")
    emoji = "✅" if ul['margem_liquida'] > 15 else "⚠️"
    insights.append(f"{emoji} <b>Margem líquida:</b> {ul['margem_liquida']:.1f}%")
    insights.append(f"💵 <b>Receita atual:</b> {fmt_brl(ul['receita'])}")
    return insights


# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding: 20px 0 16px 0;">
        <div style="font-size:32px;">🍫</div>
        <div style="font-size:17px; font-weight:700; color:{COLORS['text_primary']}; margin-top:6px;">Mica Chocolates</div>
        <div style="font-size:11px; color:{COLORS['text_secondary']}; letter-spacing:1.5px; text-transform:uppercase; margin-top:2px;">BI Premium</div>
    </div>
    <hr style="border-color:{COLORS['border']}; margin:0 0 16px 0;">
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navegação",
        ["📊  Dashboard Executivo", "🛍️  Vendas", "📦  Estoque", "💼  Finanças", "🏭  Produção"],
        label_visibility="collapsed"
    )

    st.markdown(f"""
    <hr style="border-color:{COLORS['border']}; margin:16px 0;">
    <div style="font-size:11px; color:{COLORS['text_secondary']}; text-align:center;">
        Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}
    </div>
    <div style="font-size:10px; color:{COLORS['border']}; text-align:center; margin-top:8px;">
        © 2026 Arthur Rodrigues
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# PÁGINA: DASHBOARD EXECUTIVO
# ============================================================================
if page == "📊  Dashboard Executivo":
    st.markdown(f'<div class="page-title">🏆 Dashboard Executivo</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">Visão holística do negócio — rentabilidade, eficiência e riscos em tempo real</div>', unsafe_allow_html=True)

    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    receita_total = df_vendas['receita'].sum()
    margem_liq_med = df_financeiro['margem_liquida'].mean()
    valor_estoque = df_estoque['valor_total'].sum()
    otif_media = df_clientes['otif'].mean()

    with col1: st.metric("💰 Receita Total", f"R$ {receita_total/1e6:.2f}M", "+12.5%")
    with col2: st.metric("📈 Margem Líquida Média", fmt_pct(margem_liq_med), "-2.3%")
    with col3: st.metric("📦 Valor em Estoque", f"R$ {valor_estoque/1000:.0f}k", "+8.2%")
    with col4: st.metric("✅ OTIF Médio", fmt_pct(otif_media), "+1.2%")

    st.markdown("---")

    # Receita vs Meta + Crescimento MoM
    col1, col2 = st.columns(2)
    with col1:
        section_title("📈 Receita vs Meta (Mensal)")
        vendas_mes = df_vendas.groupby('mes')['receita'].sum().reset_index()
        vendas_mes.columns = ['mes', 'receita']
        meta = vendas_mes['receita'].mean() * 1.1

        fig = go.Figure()
        # Área preenchida
        fig.add_trace(go.Scatter(
            x=vendas_mes['mes'], y=vendas_mes['receita'],
            fill='tozeroy', fillcolor='rgba(199,125,255,0.12)',
            line=dict(color=COLORS['accent2'], width=2),
            mode='lines', name='Receita Real', hovertemplate='%{x}<br>R$ %{y:,.0f}<extra></extra>'
        ))
        # Linha de meta tracejada
        fig.add_hline(y=meta, line_dash='dot', line_color=COLORS['accent1'],
                      line_width=1.5, annotation_text=f"Meta: {fmt_brl(meta)}",
                      annotation_font_color=COLORS['accent1'], annotation_font_size=10)
        apply_template(fig)
        fig.update_xaxes(tickangle=45, nticks=12)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_title("📊 Crescimento MoM (%)")
        vendas_mes2 = df_vendas.groupby('mes')['receita'].sum()
        cresc = vendas_mes2.pct_change() * 100

        bar_colors = [COLORS['positive'] if v >= 0 else COLORS['negative'] for v in cresc.fillna(0)]
        fig = go.Figure(go.Bar(
            x=cresc.index, y=cresc.values,
            marker_color=bar_colors, marker_line_width=0,
            hovertemplate='%{x}<br>%{y:.1f}%<extra></extra>',
            name='MoM %'
        ))
        fig.add_hline(y=0, line_color=COLORS['border'], line_width=1)
        apply_template(fig)
        fig.update_xaxes(tickangle=45, nticks=12)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Rentabilidade por Produto + Pizza por Canal
    col1, col2 = st.columns([3, 2])
    with col1:
        section_title("💡 Rentabilidade por Produto", "Margem = Receita - Custo de Produção")
        vp = df_vendas.groupby('produto')['receita'].sum()
        cp = df_producao.groupby('produto')['custo_total'].sum()
        rent = pd.DataFrame({'receita': vp, 'custo': cp}).fillna(0)
        rent['margem'] = rent['receita'] - rent['custo']
        rent['margem_pct'] = (rent['margem'] / rent['receita'] * 100).replace([np.inf, -np.inf], 0)
        rent = rent.sort_values('margem')

        bar_c = [COLORS['positive'] if v >= 0 else COLORS['negative'] for v in rent['margem']]
        fig = go.Figure(go.Bar(
            y=rent.index, x=rent['margem'], orientation='h',
            marker_color=bar_c, marker_line_width=0,
            text=[f"{v:.1f}%" for v in rent['margem_pct']],
            textposition='outside', textfont=dict(color=COLORS['text_secondary'], size=11),
            hovertemplate='%{y}<br>Margem: R$ %{x:,.0f}<extra></extra>',
        ))
        apply_template(fig, height=280)
        fig.update_yaxes(tickfont=dict(size=11, color=COLORS['text_primary']))
        fig.update_layout(margin=dict(l=10, r=60, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_title("🎯 Share de Receita por Canal")
        vc = df_vendas.groupby('cliente_tipo')['receita'].sum()
        fig = go.Figure(go.Pie(
            values=vc.values, labels=vc.index, hole=0.55,
            marker=dict(colors=[COLORS['accent2'], COLORS['accent3'], COLORS['accent1'], COLORS['accent4']],
                        line=dict(color=COLORS['bg_card'], width=2)),
            textfont=dict(color=COLORS['text_primary'], size=11),
            hovertemplate='%{label}<br>R$ %{value:,.0f}<br>%{percent}<extra></extra>',
        ))
        fig.update_layout(
            paper_bgcolor=COLORS['bg_card'], plot_bgcolor=COLORS['bg_primary'],
            height=280, margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(font=dict(color=COLORS['text_secondary'], size=10),
                        bgcolor='rgba(0,0,0,0)', orientation='v', x=1, y=0.5),
            annotations=[dict(text='Canais', x=0.5, y=0.5, font_size=12,
                              font_color=COLORS['text_secondary'], showarrow=False)],
            hoverlabel=dict(bgcolor='#0f3460', bordercolor=COLORS['border'],
                            font=dict(color=COLORS['text_primary']))
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Orçado vs Realizado + OTIF
    col1, col2 = st.columns(2)
    with col1:
        section_title("📋 Orçado vs Realizado — Últimos 6 Meses (FP&A)")
        fpa = df_financeiro.tail(6).copy()
        fpa['orcado'] = fpa['receita'] * 0.95

        fig = go.Figure()
        fig.add_trace(go.Bar(x=fpa['mes'], y=fpa['orcado'], name='Orçado',
                             marker_color='rgba(72,202,228,0.5)', marker_line_width=0,
                             hovertemplate='%{x}<br>Orçado: R$ %{y:,.0f}<extra></extra>'))
        fig.add_trace(go.Bar(x=fpa['mes'], y=fpa['receita'], name='Realizado',
                             marker_color=COLORS['accent2'], marker_line_width=0,
                             hovertemplate='%{x}<br>Realizado: R$ %{y:,.0f}<extra></extra>'))
        # Linha de variação
        variacao = [(r - o) / o * 100 for r, o in zip(fpa['receita'], fpa['orcado'])]
        fig.add_trace(go.Scatter(x=fpa['mes'], y=fpa['receita'],
                                 mode='markers', marker=dict(size=6, color=COLORS['accent1'],
                                 symbol='diamond'), name='Var%',
                                 hovertemplate='%{x}<br>Var: ' +
                                 '<extra></extra>'))
        apply_template(fig, height=300)
        fig.update_layout(barmode='group')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_title("✅ OTIF — Top & Bottom Clientes", "Meta: 95%")
        otif_sorted = df_clientes.sort_values('otif', ascending=True).tail(20)
        bar_c = [COLORS['positive'] if v >= 95 else COLORS['negative'] for v in otif_sorted['otif']]
        fig = go.Figure(go.Bar(
            y=otif_sorted['cliente'], x=otif_sorted['otif'],
            orientation='h', marker_color=bar_c, marker_line_width=0,
            hovertemplate='%{y}<br>OTIF: %{x:.1f}%<extra></extra>',
        ))
        fig.add_vline(x=95, line_dash='dot', line_color=COLORS['warning'],
                      line_width=1.5, annotation_text='Meta 95%',
                      annotation_font_color=COLORS['warning'], annotation_font_size=10)
        apply_template(fig, height=300)
        fig.update_xaxes(range=[75, 103])
        fig.update_layout(margin=dict(l=80, r=20, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Indicadores operacionais
    section_title("⚙️ Indicadores de Eficiência Operacional")
    col1, col2, col3, col4 = st.columns(4)
    giro = df_vendas['receita'].sum() / df_estoque['valor_total'].sum()
    lead = df_estoque['giro_dias'].mean()
    cpu  = df_producao['custo_por_unidade'].mean()
    cap  = df_estoque['valor_total'].sum() / df_vendas['receita'].sum() * 30

    with col1: st.metric("📦 Giro de Estoque", f"{giro:.2f}×", "↑ 0.3×")
    with col2: st.metric("⏱️ Lead Time Médio", f"{lead:.0f} dias", "↓ 5 dias")
    with col3: st.metric("💵 Custo / Unidade", f"R$ {cpu:.2f}", "↓ R$ 0.50")
    with col4: st.metric("💰 Capital Parado", f"{cap:.1f} dias", "↑ 5 dias")

    st.markdown("---")

    # Insights automáticos
    section_title("🤖 Insights Automáticos do Negócio")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div style="font-size:13px; font-weight:600; color:{COLORS["accent3"]}; margin-bottom:8px;">📊 VENDAS</div>', unsafe_allow_html=True)
        for i in gerar_insights_vendas():
            st.markdown(f'<div class="insight-card">{i}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="font-size:13px; font-weight:600; color:{COLORS["accent2"]}; margin-bottom:8px;">📦 ESTOQUE</div>', unsafe_allow_html=True)
        for i in gerar_insights_estoque():
            st.markdown(f'<div class="insight-card">{i}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="font-size:13px; font-weight:600; color:{COLORS["accent4"]}; margin-bottom:8px;">💼 FINANCEIRO</div>', unsafe_allow_html=True)
        for i in gerar_insights_financeiro():
            st.markdown(f'<div class="insight-card">{i}</div>', unsafe_allow_html=True)


# ============================================================================
# PÁGINA: VENDAS
# ============================================================================
elif page == "🛍️  Vendas":
    st.markdown('<div class="page-title">🛍️ Análise de Vendas</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Visões mensais e análises detalhadas de desempenho comercial</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    meses_disp = sorted(df_vendas['mes'].unique(), reverse=True)
    with col1: mes_sel = st.selectbox("Mês", meses_disp)
    with col2: prod_filter = st.multiselect("Produtos", df_vendas['produto'].unique(), default=list(df_vendas['produto'].unique()))
    with col3: canal_filter = st.multiselect("Canais", df_vendas['cliente_tipo'].unique(), default=list(df_vendas['cliente_tipo'].unique()))

    df_f = df_vendas[(df_vendas['mes'] == mes_sel) &
                     (df_vendas['produto'].isin(prod_filter)) &
                     (df_vendas['cliente_tipo'].isin(canal_filter))]

    rec_mes = df_f['receita'].sum()
    qtd_mes = df_f['quantidade'].sum()
    n_ped   = len(df_f)
    ticket  = rec_mes / n_ped if n_ped > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("💰 Receita do Mês", f"R$ {rec_mes/1000:.1f}k")
    with col2: st.metric("📦 Qtd. Vendida", f"{qtd_mes:,.0f} un")
    with col3: st.metric("🛒 Pedidos", f"{n_ped}")
    with col4: st.metric("🎯 Ticket Médio", f"R$ {ticket:,.2f}")

    st.markdown("---")

    col1, col2 = st.columns([3, 2])
    with col1:
        section_title("Receita por Produto")
        vp = df_f.groupby('produto')['receita'].sum().sort_values()
        fig = go.Figure(go.Bar(
            y=vp.index, x=vp.values, orientation='h',
            marker=dict(color=list(range(len(vp))),
                        colorscale=[[0, COLORS['accent3']], [1, COLORS['accent2']]],
                        showscale=False),
            marker_line_width=0,
            text=[f"R$ {v/1000:.1f}k" for v in vp.values],
            textposition='outside', textfont=dict(color=COLORS['text_secondary'], size=11),
            hovertemplate='%{y}<br>R$ %{x:,.0f}<extra></extra>',
        ))
        apply_template(fig, height=320)
        fig.update_layout(margin=dict(l=10, r=60, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_title("Receita por Canal")
        vc = df_f.groupby('cliente_tipo')['receita'].sum()
        fig = go.Figure(go.Pie(
            values=vc.values, labels=vc.index, hole=0.5,
            marker=dict(colors=[COLORS['accent2'], COLORS['accent3'], COLORS['accent1'], COLORS['accent4']],
                        line=dict(color=COLORS['bg_card'], width=2)),
            textfont=dict(color=COLORS['text_primary'], size=10),
            hovertemplate='%{label}<br>R$ %{value:,.0f} (%{percent})<extra></extra>',
        ))
        fig.update_layout(
            paper_bgcolor=COLORS['bg_card'], plot_bgcolor=COLORS['bg_primary'],
            height=320, margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(font=dict(color=COLORS['text_secondary'], size=10), bgcolor='rgba(0,0,0,0)'),
            hoverlabel=dict(bgcolor='#0f3460', bordercolor=COLORS['border'],
                            font=dict(color=COLORS['text_primary']))
        )
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap de vendas por dia da semana x hora
    st.markdown("---")
    section_title("📅 Mapa de Calor — Receita por Dia da Semana")
    dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    df_heat = df_vendas.copy()
    df_heat['dia_semana'] = df_heat['data'].dt.dayofweek
    df_heat['dia_nome'] = df_heat['dia_semana'].map(dict(enumerate(dias)))
    df_heat['semana_num'] = df_heat['data'].dt.isocalendar().week.astype(int)
    pivot = df_heat.groupby(['semana_num', 'dia_semana'])['receita'].sum().unstack(fill_value=0)
    pivot.columns = [dias[c] for c in pivot.columns]

    fig = go.Figure(go.Heatmap(
        z=pivot.values[-20:], x=pivot.columns,
        y=[f"Sem {w}" for w in pivot.index[-20:]],
        colorscale=[[0, COLORS['bg_primary']], [0.5, COLORS['accent2']], [1, COLORS['accent1']]],
        hovertemplate='%{x} — %{y}<br>R$ %{z:,.0f}<extra></extra>',
        showscale=True,
        colorbar=dict(tickfont=dict(color=COLORS['text_secondary'], size=10),
                      bgcolor=COLORS['bg_card'])
    ))
    apply_template(fig, height=280)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    section_title("📋 Detalhamento de Vendas")
    df_tab = df_f[['data','produto','cliente_tipo','quantidade','preco_unitario','receita']].copy()
    df_tab['data'] = df_tab['data'].dt.strftime('%d/%m/%Y')
    df_tab['preco_unitario'] = df_tab['preco_unitario'].apply(lambda x: f'R$ {x:.2f}')
    df_tab['receita'] = df_tab['receita'].apply(lambda x: f'R$ {x:,.2f}')
    df_tab.columns = ['Data','Produto','Canal','Quantidade','Preço Unit.','Receita']
    st.dataframe(df_tab.sort_values('Data', ascending=False), use_container_width=True, hide_index=True)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    vp2 = df_f.groupby('produto')['receita'].sum()
    with col1: st.info(f"🎯 **Produto Destaque:** {vp2.idxmax() if len(vp2) > 0 else 'N/A'}")
    with col2: st.success(f"🛍️ **Melhor Canal:** {df_f.groupby('cliente_tipo')['receita'].sum().idxmax() if len(df_f) > 0 else 'N/A'}")
    with col3:
        if len(vp2) > 1: st.warning(f"⚠️ **Baixo Desempenho:** {vp2.idxmin()}")


# ============================================================================
# PÁGINA: ESTOQUE
# ============================================================================
elif page == "📦  Estoque":
    st.markdown('<div class="page-title">📦 Gestão de Estoque</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Posição, rupturas, inventários e análise de perdas</div>', unsafe_allow_html=True)

    val_est   = df_estoque['valor_total'].sum()
    n_rupt    = len(df_estoque[df_estoque['ruptura'] == 'SIM'])
    perda_tot = df_estoque['perda_valor'].sum()
    giro_med  = df_estoque['giro_dias'].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("💰 Valor Total Estoque", f"R$ {val_est/1000:.1f}k")
    with col2: st.metric("⚠️ Produtos em Ruptura", str(n_rupt), delta=None)
    with col3: st.metric("📉 Perda Estimada", f"R$ {perda_tot/1000:.1f}k")
    with col4: st.metric("⏱️ Giro Médio", f"{giro_med:.0f} dias")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        section_title("💵 Posição de Estoque por Produto")
        est_s = df_estoque.sort_values('valor_total')
        fig = go.Figure(go.Bar(
            y=est_s['produto'], x=est_s['valor_total'], orientation='h',
            marker=dict(color=est_s['valor_total'],
                        colorscale=[[0, COLORS['accent3']], [1, COLORS['accent2']]],
                        showscale=False),
            marker_line_width=0,
            text=[f"R$ {v/1000:.1f}k" for v in est_s['valor_total']],
            textposition='outside', textfont=dict(color=COLORS['text_secondary'], size=11),
            hovertemplate='%{y}<br>R$ %{x:,.0f}<extra></extra>',
        ))
        apply_template(fig, height=300)
        fig.update_layout(margin=dict(l=10, r=70, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_title("📦 Giro de Estoque (Dias)")
        giro_s = df_estoque.sort_values('giro_dias')
        bar_c = [COLORS['warning'] if v > 45 else COLORS['positive'] for v in giro_s['giro_dias']]
        fig = go.Figure(go.Bar(
            y=giro_s['produto'], x=giro_s['giro_dias'], orientation='h',
            marker_color=bar_c, marker_line_width=0,
            text=[f"{v}d" for v in giro_s['giro_dias']],
            textposition='outside', textfont=dict(color=COLORS['text_secondary'], size=11),
            hovertemplate='%{y}<br>%{x} dias<extra></extra>',
        ))
        fig.add_vline(x=45, line_dash='dot', line_color=COLORS['warning'],
                      annotation_text='Alerta 45d', annotation_font_color=COLORS['warning'],
                      annotation_font_size=10)
        apply_template(fig, height=300)
        fig.update_layout(margin=dict(l=10, r=40, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Rupturas
    section_title("⚠️ Análise de Rupturas")
    rupt_df = df_estoque[df_estoque['ruptura'] == 'SIM'].copy()
    if len(rupt_df) > 0:
        st.error(f"🚨 **{len(rupt_df)} Produto(s) em Ruptura — Ação Imediata Necessária**")
        col1, col2 = st.columns(2)
        with col1:
            section_title("Produtos em Ruptura")
            fig = go.Figure(go.Bar(
                y=rupt_df.sort_values('valor_total')['produto'],
                x=rupt_df.sort_values('valor_total')['valor_total'],
                orientation='h', marker_color=COLORS['negative'], marker_line_width=0,
                text=[f"R$ {v/1000:.1f}k" for v in rupt_df.sort_values('valor_total')['valor_total']],
                textposition='outside', textfont=dict(color=COLORS['text_secondary'], size=11),
                hovertemplate='%{y}<br>R$ %{x:,.0f}<extra></extra>',
            ))
            apply_template(fig, height=220)
            fig.update_layout(margin=dict(l=10, r=70, t=30, b=10))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            section_title("Impacto Estimado / Mês")
            rupt_df['impacto'] = rupt_df['valor_total'] * 0.15
            for _, row in rupt_df.iterrows():
                st.markdown(f"""
                <div style="background:{COLORS['bg_card']}; border:1px solid {COLORS['negative']};
                     border-radius:8px; padding:12px 16px; margin-bottom:8px;">
                    <div style="font-weight:600; color:{COLORS['text_primary']};">📌 {row['produto']}</div>
                    <div style="color:{COLORS['negative']}; font-size:16px; font-weight:700; margin-top:4px;">
                        R$ {row['impacto']:,.2f} / mês em risco
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("✅ Todos os produtos estão com estoque disponível!")

    st.markdown("---")

    # Perdas
    section_title("📉 Análise de Perdas")
    col1, col2 = st.columns(2)
    with col1:
        section_title("Perda por Produto (R$)")
        per_s = df_estoque.sort_values('perda_valor')
        fig = go.Figure(go.Bar(
            y=per_s['produto'], x=per_s['perda_valor'], orientation='h',
            marker=dict(color=per_s['perda_valor'],
                        colorscale=[[0, COLORS['bg_primary']], [1, COLORS['negative']]],
                        showscale=False),
            marker_line_width=0,
            hovertemplate='%{y}<br>R$ %{x:,.2f}<extra></extra>',
        ))
        apply_template(fig, height=280)
        fig.update_layout(margin=dict(l=10, r=20, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        section_title("Perda por Produto (%)")
        per_s2 = df_estoque.sort_values('perda_percentual')
        fig = go.Figure(go.Bar(
            y=per_s2['produto'], x=per_s2['perda_percentual'], orientation='h',
            marker_color=COLORS['warning'], marker_line_width=0,
            text=[f"{v:.2f}%" for v in per_s2['perda_percentual']],
            textposition='outside', textfont=dict(color=COLORS['text_secondary'], size=11),
            hovertemplate='%{y}<br>%{x:.2f}%<extra></extra>',
        ))
        apply_template(fig, height=280)
        fig.update_layout(margin=dict(l=10, r=50, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    section_title("📋 Detalhamento de Estoque")
    df_tab = df_estoque.copy()
    df_tab['valor_total'] = df_tab['valor_total'].apply(lambda x: f'R$ {x:,.2f}')
    df_tab['perda_valor'] = df_tab['perda_valor'].apply(lambda x: f'R$ {x:,.2f}')
    df_tab['valor_unitario'] = df_tab['valor_unitario'].apply(lambda x: f'R$ {x:.2f}')
    df_tab.columns = ['Produto','Quantidade','Valor Unit.','Valor Total','Giro (dias)','Ruptura','Perda %','Perda R$']
    st.dataframe(df_tab, use_container_width=True, hide_index=True)


# ============================================================================
# PÁGINA: FINANÇAS
# ============================================================================
elif page == "💼  Finanças":
    st.markdown('<div class="page-title">💼 Análise Financeira</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">DRE, fluxo de caixa, margens e rentabilidade detalhada</div>', unsafe_allow_html=True)

    rec_tot = df_financeiro['receita'].sum()
    luc_tot = df_financeiro['lucro_liquido'].sum()
    mar_med = df_financeiro['margem_liquida'].mean()
    cus_tot = df_financeiro['custo_producao'].sum()

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("💰 Receita Total (YTD)", f"R$ {rec_tot/1000:.1f}k")
    with col2: st.metric("💵 Lucro Total", f"R$ {luc_tot/1000:.1f}k")
    with col3: st.metric("📈 Margem Média", fmt_pct(mar_med))
    with col4: st.metric("🏭 Custo Produção", f"R$ {cus_tot/1000:.1f}k")

    st.markdown("---")

    # DRE
    section_title("📊 Demonstração de Resultado (DRE) — Últimos 6 Meses")
    dre = df_financeiro.tail(6).copy()
    df_dre = dre[['mes','receita','custo_producao','lucro_bruto','despesas_operacionais','lucro_liquido']].copy()
    for col in ['receita','custo_producao','lucro_bruto','despesas_operacionais','lucro_liquido']:
        df_dre[col] = df_dre[col].apply(lambda x: f'R$ {x:,.2f}')
    df_dre.columns = ['Período','Receita','Custo Produção','Lucro Bruto','Despesas Op.','Lucro Líquido']
    st.dataframe(df_dre, use_container_width=True, hide_index=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        section_title("💡 Rentabilidade por Produto")
        vp = df_vendas.groupby('produto')['receita'].sum()
        cp = df_producao.groupby('produto')['custo_total'].sum()
        rent = pd.DataFrame({'receita': vp, 'custo': cp}).fillna(0)
        rent['lucro'] = rent['receita'] - rent['custo']
        rent['pct'] = (rent['lucro'] / rent['receita'] * 100).replace([np.inf, -np.inf], 0)
        rent = rent.sort_values('lucro')

        fig = go.Figure(go.Bar(
            y=rent.index, x=rent['lucro'], orientation='h',
            marker_color=[COLORS['positive'] if v >= 0 else COLORS['negative'] for v in rent['lucro']],
            marker_line_width=0,
            text=[f"{v:.1f}%" for v in rent['pct']],
            textposition='outside', textfont=dict(color=COLORS['text_secondary'], size=11),
            hovertemplate='%{y}<br>Lucro: R$ %{x:,.0f}<extra></extra>',
        ))
        apply_template(fig, height=300)
        fig.update_layout(margin=dict(l=10, r=60, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)
        neg = rent[rent['lucro'] < 0]
        if len(neg) > 0:
            st.error("⚠️ **Produtos com Margem Negativa:** " + ", ".join(neg.index.tolist()))

    with col2:
        section_title("💰 Rentabilidade por Canal")
        vc = df_vendas.groupby('cliente_tipo')['receita'].sum()
        custo_c = vc * 0.4
        rl = pd.DataFrame({'receita': vc, 'custo': custo_c})
        rl['lucro'] = rl['receita'] - rl['custo']
        rl['pct'] = (rl['lucro'] / rl['receita'] * 100)

        fig = go.Figure(go.Bar(
            x=rl.index, y=rl['lucro'],
            marker=dict(color=list(range(len(rl))),
                        colorscale=[[0, COLORS['accent3']], [1, COLORS['accent2']]],
                        showscale=False),
            marker_line_width=0,
            text=[f"{v:.1f}%" for v in rl['pct']],
            textposition='outside', textfont=dict(color=COLORS['text_secondary'], size=11),
            hovertemplate='%{x}<br>Lucro: R$ %{y:,.0f}<extra></extra>',
        ))
        apply_template(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Fluxo de caixa — Waterfall
    section_title("📊 Fluxo de Caixa — Entradas vs Saídas (Últimos 6 Meses)")
    fluxo = df_financeiro.tail(6).copy()
    saidas = fluxo['custo_producao'] + fluxo['despesas_operacionais']

    fig = go.Figure()
    fig.add_trace(go.Bar(x=fluxo['mes'], y=fluxo['receita'], name='Entradas (Receita)',
                         marker_color=COLORS['positive'], marker_line_width=0,
                         hovertemplate='%{x}<br>Receita: R$ %{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Bar(x=fluxo['mes'], y=-saidas, name='Saídas (Custos + Despesas)',
                         marker_color=COLORS['negative'], marker_line_width=0,
                         hovertemplate='%{x}<br>Saída: R$ %{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Scatter(
        x=fluxo['mes'], y=fluxo['lucro_liquido'],
        mode='lines+markers', name='Lucro Líquido',
        line=dict(color=COLORS['accent4'], width=2, dash='dot'),
        marker=dict(size=8, color=COLORS['accent4']),
        hovertemplate='%{x}<br>Lucro: R$ %{y:,.0f}<extra></extra>'
    ))
    apply_template(fig, height=340)
    fig.update_layout(barmode='relative')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Evolução de margens
    section_title("📈 Evolução de Margens — Últimos 12 Meses")
    mar = df_financeiro.tail(12).copy()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mar['mes'], y=mar['margem_bruta'], name='Margem Bruta %',
        mode='lines+markers', fill='tozeroy', fillcolor='rgba(199,125,255,0.08)',
        line=dict(color=COLORS['accent2'], width=2), marker=dict(size=6),
        hovertemplate='%{x}<br>Margem Bruta: %{y:.1f}%<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=mar['mes'], y=mar['margem_liquida'], name='Margem Líquida %',
        mode='lines+markers', fill='tozeroy', fillcolor='rgba(72,202,228,0.08)',
        line=dict(color=COLORS['accent3'], width=2), marker=dict(size=6),
        hovertemplate='%{x}<br>Margem Líquida: %{y:.1f}%<extra></extra>'
    ))
    fig.add_hline(y=15, line_dash='dot', line_color=COLORS['warning'],
                  annotation_text='Meta mín. 15%', annotation_font_color=COLORS['warning'],
                  annotation_font_size=10)
    apply_template(fig, height=320)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# PÁGINA: PRODUÇÃO
# ============================================================================
elif page == "🏭  Produção":
    st.markdown('<div class="page-title">🏭 Análise de Produção</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Volume produzido, custos hora/homem e eficiência operacional</div>', unsafe_allow_html=True)

    vol_tot  = df_producao['volume_produzido'].sum()
    hrs_tot  = df_producao['horas_trabalhadas'].sum()
    cus_tot  = df_producao['custo_total'].sum()
    cpu_med  = df_producao['custo_por_unidade'].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("📦 Volume Total", f"{vol_tot:,.0f} un")
    with col2: st.metric("⏱️ Horas Trabalhadas", f"{hrs_tot:,.0f} h")
    with col3: st.metric("💵 Custo Total", f"R$ {cus_tot/1000:.1f}k")
    with col4: st.metric("💰 Custo Médio/Un.", f"R$ {cpu_med:.2f}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        section_title("📦 Volume Produzido por Produto")
        vp = df_producao.groupby('produto')['volume_produzido'].sum().sort_values()
        fig = go.Figure(go.Bar(
            y=vp.index, x=vp.values, orientation='h',
            marker=dict(color=list(range(len(vp))),
                        colorscale=[[0, COLORS['accent3']], [1, COLORS['accent2']]],
                        showscale=False),
            marker_line_width=0,
            text=[f"{v:,.0f} un" for v in vp.values],
            textposition='outside', textfont=dict(color=COLORS['text_secondary'], size=11),
            hovertemplate='%{y}<br>%{x:,.0f} unidades<extra></extra>',
        ))
        apply_template(fig, height=300)
        fig.update_layout(margin=dict(l=10, r=80, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_title("💰 Custo Total por Produto")
        cp = df_producao.groupby('produto')['custo_total'].sum().sort_values()
        fig = go.Figure(go.Bar(
            y=cp.index, x=cp.values, orientation='h',
            marker_color=COLORS['accent4'], marker_line_width=0,
            text=[f"R$ {v/1000:.1f}k" for v in cp.values],
            textposition='outside', textfont=dict(color=COLORS['text_secondary'], size=11),
            hovertemplate='%{y}<br>R$ %{x:,.0f}<extra></extra>',
        ))
        apply_template(fig, height=300)
        fig.update_layout(margin=dict(l=10, r=70, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        section_title("💵 Custo Unitário Médio por Produto")
        cu = df_producao.groupby('produto')['custo_por_unidade'].mean().sort_values()
        bar_c = [COLORS['negative'] if v > cu.mean() else COLORS['positive'] for v in cu.values]
        fig = go.Figure(go.Bar(
            y=cu.index, x=cu.values, orientation='h',
            marker_color=bar_c, marker_line_width=0,
            text=[f"R$ {v:.2f}" for v in cu.values],
            textposition='outside', textfont=dict(color=COLORS['text_secondary'], size=11),
            hovertemplate='%{y}<br>R$ %{x:.2f}/un<extra></extra>',
        ))
        fig.add_vline(x=cu.mean(), line_dash='dot', line_color=COLORS['warning'],
                      annotation_text=f"Média: R$ {cu.mean():.2f}",
                      annotation_font_color=COLORS['warning'], annotation_font_size=10)
        apply_template(fig, height=300)
        fig.update_layout(margin=dict(l=10, r=70, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_title("⏱️ Horas por Produto")
        hp = df_producao.groupby('produto')['horas_trabalhadas'].sum().sort_values()
        fig = go.Figure(go.Bar(
            y=hp.index, x=hp.values, orientation='h',
            marker=dict(color=list(range(len(hp))),
                        colorscale=[[0, COLORS['accent1']], [1, COLORS['accent2']]],
                        showscale=False),
            marker_line_width=0,
            text=[f"{v:,.0f}h" for v in hp.values],
            textposition='outside', textfont=dict(color=COLORS['text_secondary'], size=11),
            hovertemplate='%{y}<br>%{x:,.0f} horas<extra></extra>',
        ))
        apply_template(fig, height=300)
        fig.update_layout(margin=dict(l=10, r=70, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        section_title("⚙️ Produtividade — Unidades por Hora")
        prod = (df_producao.groupby('produto')['volume_produzido'].sum() /
                df_producao.groupby('produto')['horas_trabalhadas'].sum()).sort_values()
        bar_c = [COLORS['positive'] if v >= prod.mean() else COLORS['warning'] for v in prod.values]
        fig = go.Figure(go.Bar(
            y=prod.index, x=prod.values, orientation='h',
            marker_color=bar_c, marker_line_width=0,
            text=[f"{v:.1f} un/h" for v in prod.values],
            textposition='outside', textfont=dict(color=COLORS['text_secondary'], size=11),
            hovertemplate='%{y}<br>%{x:.1f} un/hora<extra></extra>',
        ))
        fig.add_vline(x=prod.mean(), line_dash='dot', line_color=COLORS['accent2'],
                      annotation_text=f"Média: {prod.mean():.1f}",
                      annotation_font_color=COLORS['accent2'], annotation_font_size=10)
        apply_template(fig, height=300)
        fig.update_layout(margin=dict(l=10, r=80, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_title("📅 Evolução Mensal de Produção")
        pm = df_producao.groupby('mes')['volume_produzido'].sum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=pm.index, y=pm.values, mode='lines+markers',
            fill='tozeroy', fillcolor='rgba(199,125,255,0.1)',
            line=dict(color=COLORS['accent2'], width=2), marker=dict(size=6, color=COLORS['accent2']),
            hovertemplate='%{x}<br>%{y:,.0f} unidades<extra></extra>',
        ))
        apply_template(fig, height=300)
        fig.update_xaxes(tickangle=45, nticks=12)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    section_title("📋 Detalhamento de Produção")
    df_tab = df_producao[['data','produto','volume_produzido','horas_trabalhadas',
                           'custo_hora','custo_total','custo_por_unidade']].copy()
    df_tab['data'] = df_tab['data'].dt.strftime('%d/%m/%Y')
    df_tab['horas_trabalhadas'] = df_tab['horas_trabalhadas'].apply(lambda x: f'{x:.1f}h')
    df_tab['custo_hora'] = df_tab['custo_hora'].apply(lambda x: f'R$ {x:.2f}')
    df_tab['custo_total'] = df_tab['custo_total'].apply(lambda x: f'R$ {x:.2f}')
    df_tab['custo_por_unidade'] = df_tab['custo_por_unidade'].apply(lambda x: f'R$ {x:.2f}')
    df_tab.columns = ['Data','Produto','Volume (un)','Horas','Custo/Hora','Custo Total','Custo/Un']
    st.dataframe(df_tab.sort_values('Data', ascending=False), use_container_width=True, hide_index=True)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1: st.info(f"📌 **Maior volume:** {df_producao.groupby('produto')['volume_produzido'].sum().idxmax()}")
    with col2: st.success(f"✅ **Menor custo/un:** {df_producao.groupby('produto')['custo_por_unidade'].mean().idxmin()}")
    with col3: st.warning(f"⚠️ **Maior custo/un:** {df_producao.groupby('produto')['custo_por_unidade'].mean().idxmax()}")


# ============================================================================
# FOOTER
# ============================================================================
st.markdown(f"""
<div style='text-align:center; color:{COLORS["text_secondary"]}; font-size:11px; padding:24px 0 12px 0;
     border-top: 1px solid {COLORS["border"]}; margin-top:8px;'>
    🍫 <strong style="color:{COLORS['text_primary']};">Mica Chocolates — BI Premium</strong>
    &nbsp;|&nbsp; Desenvolvido com Python · Streamlit · Plotly
    &nbsp;|&nbsp; © 2026 Arthur Rodrigues
</div>
""", unsafe_allow_html=True)