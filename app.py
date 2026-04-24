import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Mica Chocolates - BI Premium",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cores personalizadas (tons pastel)
COLORS = {
    'roxo': '#B19CD9',
    'violeta': '#DDA0DD',
    'azul_claro': '#ADD8E6',
    'branco': '#FFFFFF',
    'amarelo': '#FFFACD',
    'rosa': '#FFB6C1',
    'background': '#F8F5FF',
    'text_dark': '#4A3F45'
}

# CSS customizado
st.markdown(f"""
    <style>
    body {{
        background-color: {COLORS['background']};
    }}
    .main {{
        padding: 20px;
    }}
    .metric-card {{
        background: linear-gradient(135deg, {COLORS['violeta']}, {COLORS['rosa']});
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# GERADOR DE DADOS SIMULADOS
# ============================================================================

@st.cache_data
def gerar_dados_vendas():
    """Gera dados realistas de vendas"""
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
        
        # Aplicar sazonalidade (páscoa, natal)
        mes = data.month
        if mes in [3, 4, 12]:
            quantidade = int(quantidade * np.random.uniform(1.3, 1.8))
        
        mes_str = data.strftime('%Y-%m')
        
        dados.append({
            'data': data,
            'produto': produto,
            'cliente_tipo': cliente,
            'preco_unitario': preco_unitario,
            'quantidade': quantidade,
            'receita': preco_unitario * quantidade,
            'mes': mes_str,
            'semana': data.isocalendar()[1]
        })
    
    return pd.DataFrame(dados)

@st.cache_data
def gerar_dados_estoque():
    """Gera dados de estoque"""
    np.random.seed(42)
    produtos = ['Dark 70%', 'Leite Clássico', 'Branco Premium', 'Recheado Morango', 'Nibs Crocante', 'Trufa Gourmet']
    
    dados = []
    for produto in produtos:
        quantidade = np.random.randint(500, 5000)
        valor_unitario = np.random.uniform(12, 85)
        valor_total = quantidade * valor_unitario
        
        ruptura = 'SIM' if np.random.random() < 0.05 else 'NÃO'
        
        dados.append({
            'produto': produto,
            'quantidade': quantidade,
            'valor_unitario': valor_unitario,
            'valor_total': valor_total,
            'giro_dias': np.random.randint(15, 60),
            'ruptura': ruptura,
            'perda_percentual': np.random.uniform(0, 5),
            'perda_valor': valor_total * np.random.uniform(0, 0.05)
        })
    
    return pd.DataFrame(dados)

@st.cache_data
def gerar_dados_producao():
    """Gera dados de produção"""
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
            'data': data,
            'produto': produto,
            'volume_produzido': volume,
            'horas_trabalhadas': horas_trabalho,
            'custo_hora': custo_hora,
            'custo_total': horas_trabalho * custo_hora,
            'custo_por_unidade': (horas_trabalho * custo_hora) / volume,
            'mes': mes_str
        })
    
    return pd.DataFrame(dados)

@st.cache_data
def gerar_dados_financeiro():
    """Gera dados financeiros"""
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
            'mes': mes_str,
            'receita': receita,
            'custo_producao': custo_producao,
            'despesas_operacionais': despesas_operacionais,
            'lucro_bruto': lucro_bruto,
            'lucro_liquido': lucro_liquido,
            'margem_bruta': (lucro_bruto / receita) * 100,
            'margem_liquida': (lucro_liquido / receita) * 100
        })
    
    return pd.DataFrame(dados)

@st.cache_data
def gerar_dados_clientes():
    """Gera dados de clientes"""
    np.random.seed(42)
    clientes = [f'Cliente_{i}' for i in range(1, 51)]
    
    dados = []
    for cliente in clientes:
        receita_anual = np.random.uniform(5000, 500000)
        ticket_medio = np.random.uniform(500, 5000)
        num_pedidos = int(receita_anual / ticket_medio)
        
        dados.append({
            'cliente': cliente,
            'receita_anual': receita_anual,
            'ticket_medio': ticket_medio,
            'num_pedidos': num_pedidos,
            'canal': np.random.choice(['Varejo', 'Distribuidor', 'E-commerce', 'Corporate']),
            'otif': np.random.uniform(0.80, 1.0) * 100
        })
    
    return pd.DataFrame(dados)

# Carregar dados
df_vendas = gerar_dados_vendas()
df_estoque = gerar_dados_estoque()
df_producao = gerar_dados_producao()
df_financeiro = gerar_dados_financeiro()
df_clientes = gerar_dados_clientes()

# ============================================================================
# FUNÇÕES DE INSIGHTS AUTOMÁTICOS
# ============================================================================

def gerar_insights_vendas():
    """Gera insights automáticos de vendas"""
    insights = []
    
    vendas_por_produto = df_vendas.groupby('produto')['receita'].sum()
    melhor_produto = vendas_por_produto.idxmax()
    insights.append(f"🎯 **Melhor produto:** {melhor_produto} com R$ {vendas_por_produto[melhor_produto]:,.2f}")
    
    vendas_mes = df_vendas.groupby('mes')['receita'].sum()
    if len(vendas_mes) > 1:
        ultimo_mes = vendas_mes.iloc[-1]
        mes_anterior = vendas_mes.iloc[-2]
        crescimento = ((ultimo_mes - mes_anterior) / mes_anterior) * 100
        emoji = "📈" if crescimento > 0 else "📉"
        insights.append(f"{emoji} **Crescimento MoM:** {crescimento:+.1f}%")
    
    vendas_canal = df_vendas.groupby('cliente_tipo')['receita'].sum()
    melhor_canal = vendas_canal.idxmax()
    insights.append(f"🛍️ **Melhor canal:** {melhor_canal}")
    
    return insights

def gerar_insights_estoque():
    """Gera insights automáticos de estoque"""
    insights = []
    
    rupturas = df_estoque[df_estoque['ruptura'] == 'SIM']
    if len(rupturas) > 0:
        insights.append(f"⚠️ **{len(rupturas)} produto(s) em ruptura!**")
        for _, row in rupturas.iterrows():
            insights.append(f"   - {row['produto']}: Impacto estimado R$ {row['valor_total']/10:,.2f}/mês")
    
    valor_total_estoque = df_estoque['valor_total'].sum()
    insights.append(f"💰 **Capital parado em estoque:** R$ {valor_total_estoque:,.2f}")
    
    perda_total = df_estoque['perda_valor'].sum()
    insights.append(f"📉 **Perda estimada:** R$ {perda_total:,.2f}")
    
    return insights

def gerar_insights_financeiro():
    """Gera insights automáticos financeiros"""
    insights = []
    
    ultimo_mes = df_financeiro.iloc[-1]
    
    margem_bruta = ultimo_mes['margem_bruta']
    insights.append(f"📊 **Margem bruta:** {margem_bruta:.1f}%")
    
    margem_liquida = ultimo_mes['margem_liquida']
    emoji = "✅" if margem_liquida > 15 else "⚠️"
    insights.append(f"{emoji} **Margem líquida:** {margem_liquida:.1f}%")
    
    insights.append(f"💵 **Receita mês atual:** R$ {ultimo_mes['receita']:,.2f}")
    
    return insights

# ============================================================================
# NAVEGAÇÃO - BARRA LATERAL
# ============================================================================

st.sidebar.markdown("---")
st.sidebar.title("🍫 Mica Chocolates BI")
st.sidebar.markdown("**Sistema Premium de Inteligência de Negócios**")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📑 **Navegação**",
    ["📊 Dashboard Corp", "🛍�� Vendas", "📦 Estoque", "💼 Finanças", "🏭 Produção"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"*Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}*")

# ============================================================================
# PÁGINA: DASHBOARD CORP
# ============================================================================

if page == "📊 Dashboard Corp":
    st.title("🏆 Dashboard Executivo Premium")
    st.markdown("Visão holística do negócio com foco em rentabilidade e eficiência operacional")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        receita_total = df_vendas['receita'].sum()
        st.metric("💰 Receita Total", f"R$ {receita_total/1000:.0f}k", "+12.5%", delta_color="inverse")
    
    with col2:
        margem_liquida = df_financeiro['margem_liquida'].mean()
        st.metric("📈 Margem Líquida Média", f"{margem_liquida:.1f}%", "-2.3%")
    
    with col3:
        valor_estoque = df_estoque['valor_total'].sum()
        st.metric("📦 Valor Estoque", f"R$ {valor_estoque/1000:.0f}k", "+8.2%")
    
    with col4:
        otif_media = df_clientes['otif'].mean()
        st.metric("✅ OTIF Médio", f"{otif_media:.1f}%", "+1.2%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Receita vs Meta (MoM)")
        vendas_mes = df_vendas.groupby('mes')['receita'].sum()
        meta = vendas_mes.mean() * 1.1
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=vendas_mes.index,
            y=vendas_mes.values,
            name='Receita Real',
            marker_color=COLORS['violeta']
        ))
        fig.add_hline(y=meta, line_dash="dash", line_color=COLORS['rosa'], annotation_text="Meta", annotation_position="right")
        fig.update_layout(template='plotly_white', hovermode='x unified', margin=dict(l=0, r=0, t=30, b=0), height=350, plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Crescimento YoY / MoM")
        vendas_mes_ano = df_vendas.groupby('mes')['receita'].sum()
        crescimento_mom = vendas_mes_ano.pct_change() * 100
        
        fig = go.Figure()
        colors = [COLORS['roxo'] if x >= 0 else COLORS['rosa'] for x in crescimento_mom]
        fig.add_trace(go.Bar(x=crescimento_mom.index, y=crescimento_mom.values, marker_color=colors, name='Crescimento %'))
        fig.update_layout(template='plotly_white', hovermode='x unified', margin=dict(l=0, r=0, t=30, b=0), height=350, plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💡 Rentabilidade por Produto")
        vendas_produto = df_vendas.groupby('produto')['receita'].sum()
        custo_produto = df_producao.groupby('produto')['custo_total'].sum()
        
        rentabilidade = pd.DataFrame({'receita': vendas_produto, 'custo': custo_produto}).fillna(0)
        rentabilidade['margem'] = rentabilidade['receita'] - rentabilidade['custo']
        rentabilidade['margem_pct'] = (rentabilidade['margem'] / rentabilidade['receita'] * 100).replace([np.inf, -np.inf], 0)
        rentabilidade = rentabilidade.sort_values('margem', ascending=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(y=rentabilidade.index, x=rentabilidade['margem'], orientation='h', marker_color=COLORS['azul_claro'], text=rentabilidade['margem_pct'].round(1).astype(str) + '%', textposition='outside'))
        fig.update_layout(template='plotly_white', height=300, margin=dict(l=150, r=0, t=30, b=0), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Rentabilidade por Cliente/Canal")
        vendas_canal = df_vendas.groupby('cliente_tipo').agg({'receita': 'sum', 'quantidade': 'count'})
        vendas_canal['receita_por_pedido'] = vendas_canal['receita'] / vendas_canal['quantidade']
        
        fig = px.pie(values=vendas_canal['receita'], names=vendas_canal.index, color_discrete_sequence=[COLORS['violeta'], COLORS['rosa'], COLORS['azul_claro'], COLORS['roxo']], hole=0.4)
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0), paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📉 Curva ABC - Concentração de Receita")
        vendas_cliente = df_vendas.groupby('cliente_tipo')['receita'].sum().sort_values(ascending=False)
        vendas_cliente_pct = (vendas_cliente / vendas_cliente.sum() * 100).cumsum()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(vendas_cliente_pct))), y=vendas_cliente_pct.values, mode='lines+markers', name='Concentração Acumulada', line=dict(color=COLORS['violeta'], width=3), marker=dict(size=10, color=COLORS['rosa'])))
        fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Regra 80/20")
        fig.update_layout(template='plotly_white', yaxis_title='% Receita Acumulada', xaxis_title='Clientes (ordenados)', height=350, plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("✅ OTIF por Cliente")
        otif_data = df_clientes.sort_values('otif', ascending=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(y=otif_data['cliente'], x=otif_data['otif'], orientation='h', marker_color=[COLORS['roxo'] if x >= 95 else COLORS['rosa'] for x in otif_data['otif']], text=otif_data['otif'].round(1).astype(str) + '%', textposition='outside'))
        fig.add_vline(x=95, line_dash="dash", line_color="green", annotation_text="Meta 95%")
        fig.update_layout(template='plotly_white', height=350, xaxis_title='OTIF (%)', margin=dict(l=100, r=0, t=30, b=0), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'], showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚠️ Risco & Impacto Financeiro")
        estoque_risco = df_estoque[df_estoque['ruptura'] == 'SIM'].copy()
        estoque_risco['impacto_mensal'] = estoque_risco['valor_total'] * 0.15
        estoque_risco = estoque_risco.sort_values('impacto_mensal', ascending=False)
        
        if len(estoque_risco) > 0:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=estoque_risco['produto'], y=estoque_risco['impacto_mensal'], marker_color=COLORS['rosa'], text=estoque_risco['impacto_mensal'].round(0).astype(str), textposition='outside'))
            fig.update_layout(title_text='Impacto Estimado de Rupturas', template='plotly_white', height=300, yaxis_title='Impacto R$', margin=dict(l=0, r=0, t=40, b=0), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📋 Orçado vs Real (FP&A)")
        fp_a = df_financeiro.tail(6).copy()
        fp_a['orcado'] = fp_a['receita'] * 0.95
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=fp_a['mes'], y=fp_a['orcado'], name='Orçado', marker_color=COLORS['azul_claro']))
        fig.add_trace(go.Bar(x=fp_a['mes'], y=fp_a['receita'], name='Realizado', marker_color=COLORS['violeta']))
        fig.update_layout(template='plotly_white', barmode='group', height=300, margin=dict(l=0, r=0, t=40, b=0), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("⚙️ Indicadores de Eficiência Operacional")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        giro_estoque = (df_vendas['receita'].sum() / df_estoque['valor_total'].sum())
        st.metric("📦 Giro de Estoque", f"{giro_estoque:.2f}x", "↑ 0.3x")
    
    with col2:
        lead_time_medio = df_estoque['giro_dias'].mean()
        st.metric("⏱️ Lead Time Médio", f"{lead_time_medio:.0f} dias", "↓ 5 dias")
    
    with col3:
        custo_por_unidade = df_producao['custo_por_unidade'].mean()
        st.metric("💵 Custo por Unidade", f"R$ {custo_por_unidade:.2f}", "↓ R$ 0.50")
    
    with col4:
        exposicao_estoque = (df_estoque['valor_total'].sum() / df_vendas['receita'].sum() * 30)
        st.metric("💰 Capital Parado", f"{exposicao_estoque:.1f} dias", "↑ 5 dias")
    
    st.markdown("---")
    
    st.subheader("🤖 Insights Automáticos do Negócio")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Vendas")
        for insight in gerar_insights_vendas():
            st.write(insight)
    
    with col2:
        st.markdown("### 📦 Estoque")
        for insight in gerar_insights_estoque():
            st.write(insight)
    
    with col3:
        st.markdown("### 💼 Financeiro")
        for insight in gerar_insights_financeiro():
            st.write(insight)

elif page == "🛍️ Vendas":
    st.title("🛍️ Análise de Vendas")
    st.markdown("Visões mensais e análises detalhadas de desempenho comercial")
    
    col1, col2, col3 = st.columns(3)
    
    meses_disponiveis = sorted(df_vendas['mes'].unique(), reverse=True)
    
    with col1:
        mes_selecionado = st.selectbox("Selecione o Mês", meses_disponiveis)
    
    with col2:
        produto_filter = st.multiselect("Produtos", df_vendas['produto'].unique(), default=df_vendas['produto'].unique())
    
    with col3:
        canal_filter = st.multiselect("Canais", df_vendas['cliente_tipo'].unique(), default=df_vendas['cliente_tipo'].unique())
    
    df_vendas_filtrado = df_vendas[(df_vendas['mes'] == mes_selecionado) & (df_vendas['produto'].isin(produto_filter)) & (df_vendas['cliente_tipo'].isin(canal_filter))]
    
    col1, col2, col3, col4 = st.columns(4)
    
    receita_mes = df_vendas_filtrado['receita'].sum()
    quantidade_vendida = df_vendas_filtrado['quantidade'].sum()
    num_pedidos = len(df_vendas_filtrado)
    ticket_medio = receita_mes / num_pedidos if num_pedidos > 0 else 0
    
    with col1:
        st.metric("💰 Receita do Mês", f"R$ {receita_mes/1000:.1f}k")
    with col2:
        st.metric("📦 Quantidade Vendida", f"{quantidade_vendida:.0f} un")
    with col3:
        st.metric("🛒 Número de Pedidos", f"{num_pedidos}")
    with col4:
        st.metric("🎯 Ticket Médio", f"R$ {ticket_medio:.2f}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Receita por Produto")
        vendas_produto = df_vendas_filtrado.groupby('produto')['receita'].sum().sort_values(ascending=False)
        fig = px.bar(x=vendas_produto.values, y=vendas_produto.index, orientation='h', color_discrete_sequence=[COLORS['violeta']], labels={'x': 'Receita (R$)', 'y': 'Produto'})
        fig.update_layout(template='plotly_white', height=350, plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'], margin=dict(l=150))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Receita por Canal")
        vendas_canal = df_vendas_filtrado.groupby('cliente_tipo')['receita'].sum()
        fig = px.pie(values=vendas_canal.values, names=vendas_canal.index, color_discrete_sequence=[COLORS['roxo'], COLORS['violeta'], COLORS['azul_claro'], COLORS['rosa']])
        fig.update_layout(height=350, paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📋 Detalhamento de Vendas")
    df_tabela = df_vendas_filtrado.copy()
    df_tabela['data'] = df_tabela['data'].dt.strftime('%d/%m/%Y')
    df_tabela = df_tabela[['data', 'produto', 'cliente_tipo', 'quantidade', 'preco_unitario', 'receita']].sort_values('data', ascending=False)
    df_tabela['preco_unitario'] = df_tabela['preco_unitario'].apply(lambda x: f'R$ {x:.2f}')
    df_tabela['receita'] = df_tabela['receita'].apply(lambda x: f'R$ {x:.2f}')
    df_tabela.columns = ['Data', 'Produto', 'Canal', 'Quantidade', 'Preço Unit.', 'Receita']
    st.dataframe(df_tabela, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("💡 Insights Automáticos de Vendas")
    col1, col2, col3 = st.columns(3)
    with col1:
        produto_destaque = vendas_produto.idxmax() if len(vendas_produto) > 0 else "N/A"
        st.info(f"🎯 **Produto Destaque:** {produto_destaque}")
    with col2:
        canal_destaque = df_vendas_filtrado.groupby('cliente_tipo')['receita'].sum().idxmax() if len(df_vendas_filtrado) > 0 else "N/A"
        st.success(f"🛍️ **Melhor Canal:** {canal_destaque}")
    with col3:
        if len(vendas_produto) > 1:
            prod_menor = vendas_produto.idxmin()
            st.warning(f"⚠️ **Produto Baixo Desempenho:** {prod_menor}")

elif page == "📦 Estoque":
    st.title("📦 Gestão de Estoque")
    st.markdown("Análise integrada de posição, ruptura, inventários e perdas")
    
    col1, col2, col3, col4 = st.columns(4)
    valor_total_estoque = df_estoque['valor_total'].sum()
    num_rupturas = len(df_estoque[df_estoque['ruptura'] == 'SIM'])
    perda_total = df_estoque['perda_valor'].sum()
    giro_medio = df_estoque['giro_dias'].mean()
    
    with col1:
        st.metric("💰 Valor Total Estoque", f"R$ {valor_total_estoque/1000:.1f}k")
    with col2:
        st.metric("⚠️ Produtos em Ruptura", f"{num_rupturas}")
    with col3:
        st.metric("📉 Perda Estimada", f"R$ {perda_total/1000:.1f}k")
    with col4:
        st.metric("⏱️ Giro Médio", f"{giro_medio:.0f} dias")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💵 Posição de Estoque por Produto")
        fig = px.bar(df_estoque.sort_values('valor_total', ascending=True), y='produto', x='valor_total', orientation='h', color_discrete_sequence=[COLORS['azul_claro']], labels={'valor_total': 'Valor (R$)', 'produto': ''})
        fig.update_layout(template='plotly_white', height=300, margin=dict(l=150), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📦 Giro de Estoque (Dias)")
        fig = px.bar(df_estoque.sort_values('giro_dias', ascending=True), y='produto', x='giro_dias', orientation='h', color_discrete_sequence=[COLORS['violeta']], labels={'giro_dias': 'Dias', 'produto': ''})
        fig.update_layout(template='plotly_white', height=300, margin=dict(l=150), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("⚠️ Análise de Rupturas")
    rupturas_df = df_estoque[df_estoque['ruptura'] == 'SIM'].copy()
    
    if len(rupturas_df) > 0:
        st.error(f"🚨 **{len(rupturas_df)} Produto(s) em Ruptura!**")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Produtos em Ruptura")
            fig = px.bar(rupturas_df.sort_values('valor_total', ascending=True), y='produto', x='valor_total', orientation='h', color_discrete_sequence=[COLORS['rosa']], labels={'valor_total': 'Valor (R$)', 'produto': ''})
            fig.update_layout(template='plotly_white', height=250, margin=dict(l=150), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("Impacto Estimado")
            rupturas_df['impacto'] = rupturas_df['valor_total'] * 0.15
            for _, row in rupturas_df.iterrows():
                st.warning(f"📌 **{row['produto']}**: R$ {row['impacto']:,.2f}/mês em risco")
    else:
        st.success("✅ Todos os produtos estão com estoque disponível!")
    
    st.markdown("---")
    
    st.subheader("📉 Análise de Perdas")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Perda por Produto (R$)")
        fig = px.bar(df_estoque.sort_values('perda_valor', ascending=True), y='produto', x='perda_valor', orientation='h', color_discrete_sequence=[COLORS['rosa']], labels={'perda_valor': 'Perda (R$)', 'produto': ''})
        fig.update_layout(template='plotly_white', height=300, margin=dict(l=150), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Perda por Produto (%)")
        fig = px.bar(df_estoque.sort_values('perda_percentual', ascending=True), y='produto', x='perda_percentual', orientation='h', color_discrete_sequence=[COLORS['roxo']], labels={'perda_percentual': '% Perda', 'produto': ''})
        fig.update_layout(template='plotly_white', height=300, margin=dict(l=150), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📋 Detalhamento de Estoque")
    df_tabela = df_estoque.copy()
    df_tabela['valor_total'] = df_tabela['valor_total'].apply(lambda x: f'R$ {x:,.2f}')
    df_tabela['perda_valor'] = df_tabela['perda_valor'].apply(lambda x: f'R$ {x:,.2f}')
    df_tabela['valor_unitario'] = df_tabela['valor_unitario'].apply(lambda x: f'R$ {x:.2f}')
    df_tabela.columns = ['Produto', 'Quantidade', 'Valor Unit.', 'Valor Total', 'Giro (dias)', 'Ruptura', 'Perda %', 'Perda R$']
    st.dataframe(df_tabela, use_container_width=True, hide_index=True)

elif page == "💼 Finanças":
    st.title("💼 Análise Financeira")
    st.markdown("Retorno por produto, entradas e saídas, rentabilidade detalhada")
    
    col1, col2, col3, col4 = st.columns(4)
    receita_total = df_financeiro['receita'].sum()
    lucro_total = df_financeiro['lucro_liquido'].sum()
    margem_media = df_financeiro['margem_liquida'].mean()
    
    with col1:
        st.metric("💰 Receita Total (YTD)", f"R$ {receita_total/1000:.1f}k")
    with col2:
        st.metric("💵 Lucro Total", f"R$ {lucro_total/1000:.1f}k")
    with col3:
        st.metric("📈 Margem Média", f"{margem_media:.1f}%")
    with col4:
        custo_total = df_financeiro['custo_producao'].sum()
        st.metric("🏭 Custo Produção", f"R$ {custo_total/1000:.1f}k")
    
    st.markdown("---")
    
    st.subheader("📊 Demonstração de Resultado (DRE) - Últimos 6 Meses")
    dre_dados = df_financeiro.tail(6).copy()
    dre_dados['lucro_bruto'] = dre_dados['receita'] - dre_dados['custo_producao']
    dre_dados['lucro_liquido'] = dre_dados['lucro_bruto'] - dre_dados['despesas_operacionais']
    
    df_dre_display = dre_dados[['mes', 'receita', 'custo_producao', 'lucro_bruto', 'despesas_operacionais', 'lucro_liquido']].copy()
    df_dre_display['receita'] = df_dre_display['receita'].apply(lambda x: f'R$ {x:,.2f}')
    df_dre_display['custo_producao'] = df_dre_display['custo_producao'].apply(lambda x: f'R$ {x:,.2f}')
    df_dre_display['lucro_bruto'] = df_dre_display['lucro_bruto'].apply(lambda x: f'R$ {x:,.2f}')
    df_dre_display['despesas_operacionais'] = df_dre_display['despesas_operacionais'].apply(lambda x: f'R$ {x:,.2f}')
    df_dre_display['lucro_liquido'] = df_dre_display['lucro_liquido'].apply(lambda x: f'R$ {x:,.2f}')
    
    df_dre_display.columns = ['Período', 'Receita', 'Custo Produção', 'Lucro Bruto', 'Despesas Op.', 'Lucro Líquido']
    st.dataframe(df_dre_display, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💡 Rentabilidade por Produto")
        vendas_produto = df_vendas.groupby('produto')['receita'].sum()
        custo_produto = df_producao.groupby('produto')['custo_total'].sum()
        
        rentabilidade = pd.DataFrame({'receita': vendas_produto, 'custo': custo_produto}).fillna(0)
        rentabilidade['lucro'] = rentabilidade['receita'] - rentabilidade['custo']
        rentabilidade['margem_pct'] = (rentabilidade['lucro'] / rentabilidade['receita'] * 100).replace([np.inf, -np.inf], 0)
        rentabilidade = rentabilidade.sort_values('lucro', ascending=True)
        
        fig = go.Figure()
        colors = [COLORS['roxo'] if x > 0 else COLORS['rosa'] for x in rentabilidade['lucro']]
        fig.add_trace(go.Bar(y=rentabilidade.index, x=rentabilidade['lucro'], orientation='h', marker_color=colors, text=rentabilidade['margem_pct'].round(1).astype(str) + '%', textposition='outside'))
        fig.update_layout(template='plotly_white', height=300, xaxis_title='Lucro (R$)', margin=dict(l=150), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
        
        produtos_negativos = rentabilidade[rentabilidade['lucro'] < 0]
        if len(produtos_negativos) > 0:
            st.error("⚠️ **Produtos com Margem Negativa:**")
            for produto in produtos_negativos.index:
                st.write(f"- {produto}: R$ {produtos_negativos.loc[produto, 'lucro']:,.2f}")
    
    with col2:
        st.subheader("💰 Rentabilidade por Cliente/Canal")
        vendas_canal = df_vendas.groupby('cliente_tipo')['receita'].sum()
        custo_estimado_canal = (vendas_canal * 0.4)
        rentabilidade_canal = pd.DataFrame({'receita': vendas_canal, 'custo': custo_estimado_canal})
        rentabilidade_canal['lucro'] = rentabilidade_canal['receita'] - rentabilidade_canal['custo']
        
        fig = px.bar(rentabilidade_canal.reset_index(), x='cliente_tipo', y='lucro', color='lucro', color_continuous_scale=[COLORS['rosa'], COLORS['roxo']], labels={'cliente_tipo': '', 'lucro': 'Lucro (R$)'})
        fig.update_layout(template='plotly_white', height=300, plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'], showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📊 Fluxo de Caixa - Entradas vs Saídas (Últimos 6 Meses)")
    fluxo_dados = df_financeiro.tail(6).copy()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=fluxo_dados['mes'], y=fluxo_dados['receita'], name='Entradas (Receita)', marker_color=COLORS['roxo']))
    saidas = fluxo_dados['custo_producao'] + fluxo_dados['despesas_operacionais']
    fig.add_trace(go.Bar(x=fluxo_dados['mes'], y=saidas, name='Saídas (Custos + Despesas)', marker_color=COLORS['rosa']))
    fig.update_layout(template='plotly_white', barmode='group', height=350, plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'], hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📈 Evolução de Margens (Últimos 12 Meses)")
    margens_dados = df_financeiro.tail(12).copy()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=margens_dados['mes'], y=margens_dados['margem_bruta'], mode='lines+markers', name='Margem Bruta %', line=dict(color=COLORS['violeta'], width=2), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=margens_dados['mes'], y=margens_dados['margem_liquida'], mode='lines+markers', name='Margem Líquida %', line=dict(color=COLORS['azul_claro'], width=2), marker=dict(size=8)))
    fig.update_layout(template='plotly_white', height=350, yaxis_title='Margem (%)', plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'], hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

elif page == "🏭 Produção":
    st.title("🏭 Análise de Produção")
    st.markdown("Volume produzido, custos de hora/homem e eficiência operacional")
    
    col1, col2, col3, col4 = st.columns(4)
    volume_total = df_producao['volume_produzido'].sum()
    horas_total = df_producao['horas_trabalhadas'].sum()
    custo_total = df_producao['custo_total'].sum()
    custo_medio_unidade = df_producao['custo_por_unidade'].mean()
    
    with col1:
        st.metric("📦 Volume Total Produzido", f"{volume_total:,.0f} un")
    with col2:
        st.metric("⏱️ Total Horas Trabalhadas", f"{horas_total:,.0f} h")
    with col3:
        st.metric("💵 Custo Total Produção", f"R$ {custo_total/1000:.1f}k")
    with col4:
        st.metric("💰 Custo Médio por Unidade", f"R$ {custo_medio_unidade:.2f}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Volume Produzido por Produto")
        volume_produto = df_producao.groupby('produto')['volume_produzido'].sum().sort_values(ascending=True)
        fig = px.bar(x=volume_produto.values, y=volume_produto.index, orientation='h', color_discrete_sequence=[COLORS['violeta']], labels={'x': 'Volume (unidades)', 'y': ''})
        fig.update_layout(template='plotly_white', height=300, margin=dict(l=150), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Custo Total por Produto")
        custo_produto = df_producao.groupby('produto')['custo_total'].sum().sort_values(ascending=True)
        fig = px.bar(x=custo_produto.values, y=custo_produto.index, orientation='h', color_discrete_sequence=[COLORS['azul_claro']], labels={'x': 'Custo (R$)', 'y': ''})
        fig.update_layout(template='plotly_white', height=300, margin=dict(l=150), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💵 Custo Unitário por Produto")
        custo_unitario = df_producao.groupby('produto')['custo_por_unidade'].mean().sort_values(ascending=True)
        fig = px.bar(x=custo_unitario.values, y=custo_unitario.index, orientation='h', color_discrete_sequence=[COLORS['rosa']], labels={'x': 'Custo Unitário (R$)', 'y': ''})
        fig.update_layout(template='plotly_white', height=300, margin=dict(l=150), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⏱️ Horas Trabalhadas por Produto")
        horas_produto = df_producao.groupby('produto')['horas_trabalhadas'].sum().sort_values(ascending=True)
        fig = px.bar(x=horas_produto.values, y=horas_produto.index, orientation='h', color_discrete_sequence=[COLORS['roxo']], labels={'x': 'Horas', 'y': ''})
        fig.update_layout(template='plotly_white', height=300, margin=dict(l=150), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("⚙️ Análise de Produtividade")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Unidades por Hora (Produtividade)")
        produtividade = (df_producao.groupby('produto')['volume_produzido'].sum() / df_producao.groupby('produto')['horas_trabalhadas'].sum()).sort_values(ascending=True)
        fig = px.bar(x=produtividade.values, y=produtividade.index, orientation='h', color_discrete_sequence=[COLORS['azul_claro']], labels={'x': 'Un/Hora', 'y': ''})
        fig.update_layout(template='plotly_white', height=300, margin=dict(l=150), plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Evolução Mensal de Produção")
        producao_mes = df_producao.groupby('mes')['volume_produzido'].sum()
        fig = px.line(x=producao_mes.index, y=producao_mes.values, markers=True, color_discrete_sequence=[COLORS['violeta']], labels={'x': '', 'y': 'Volume (unidades)'})
        fig.update_layout(template='plotly_white', height=300, plot_bgcolor=COLORS['background'], paper_bgcolor=COLORS['background'])
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📋 Detalhamento de Produção")
    df_tabela = df_producao.copy()
    df_tabela['data'] = df_tabela['data'].dt.strftime('%d/%m/%Y')
    df_tabela = df_tabela[['data', 'produto', 'volume_produzido', 'horas_trabalhadas', 'custo_hora', 'custo_total', 'custo_por_unidade']].sort_values('data', ascending=False)
    
    df_tabela['horas_trabalhadas'] = df_tabela['horas_trabalhadas'].apply(lambda x: f'{x:.1f}h')
    df_tabela['custo_hora'] = df_tabela['custo_hora'].apply(lambda x: f'R$ {x:.2f}')
    df_tabela['custo_total'] = df_tabela['custo_total'].apply(lambda x: f'R$ {x:.2f}')
    df_tabela['custo_por_unidade'] = df_tabela['custo_por_unidade'].apply(lambda x: f'R$ {x:.2f}')
    
    df_tabela.columns = ['Data', 'Produto', 'Volume (un)', 'Horas', 'Custo/Hora', 'Custo Total', 'Custo/Un']
    st.dataframe(df_tabela, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("💡 Insights de Produção")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        produto_maior_volume = df_producao.groupby('produto')['volume_produzido'].sum().idxmax()
        st.info(f"📌 **Maior volume:** {produto_maior_volume}")
    
    with col2:
        produto_menor_custo = df_producao.groupby('produto')['custo_por_unidade'].mean().idxmin()
        st.success(f"✅ **Menor custo unitário:** {produto_menor_custo}")
    
    with col3:
        produto_maior_custo = df_producao.groupby('produto')['custo_por_unidade'].mean().idxmax()
        st.warning(f"⚠️ **Maior custo unitário:** {produto_maior_custo}")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999; font-size: 12px; padding: 20px;'>
    <p>🍫 <strong>Mica Chocolates - BI Premium</strong> | Protótipo de Demonstração</p>
    <p>Desenvolvido com Python, Streamlit e Plotly | Tons Pastel: Roxo, Violeta, Azul Claro, Rosa e Amarelo</p>
    <p>© 2026 - Arthur Rodrigues | Inteligência de Negócios</p>
</div>
""", unsafe_allow_html=True)