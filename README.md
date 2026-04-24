# 🍫 Mica Chocolates - BI Premium

## Protótipo de Sistema de Business Intelligence para Gestão Integrada

Um sistema completo de BI/ERP desenvolvido em Python com foco em **excelência operacional**, **automação de insights** e **design premium** com paleta de cores em tons pastel.

---

## 📋 Funcionalidades

### 1. **Dashboard Executivo (Corp)**
- Performance geral do negócio (Receita vs Meta, Crescimento MoM/YoY)
- Análise de rentabilidade por produto, cliente e canal
- Curva ABC para identificar concentração de receita
- Indicadores de eficiência operacional (OTIF, Giro de Estoque, Lead Time)
- Risco & Impacto Financeiro (Rupturas, Fornecedores)
- Planejamento vs Realizado (FP&A)
- **Insights automáticos** com recomendações inteligentes

### 2. **Vendas** 🛍️
- Análise mensal com múltiplos filtros
- Receita por produto, canal e cliente
- Ticket médio e quantidade vendida
- KPIs: Receita, Quantidade, Número de Pedidos
- Tabela detalhada de todas as operações
- Insights automáticos de desempenho

### 3. **Estoque** 📦
- Posição de estoque em R$
- Análise de rupturas com impacto estimado
- Inventários detalhados por produto
- Análise de perdas (% e R$)
- Giro de estoque
- Alertas automáticos

### 4. **Finanças** ���
- **Retorno por Produto** (foco: lucratividade real, não só volume)
- DRE integrado (Receita, Custos, Lucro Bruto/Líquido)
- Análise de entradas e saídas
- Rentabilidade por cliente/canal
- Evolução de margens
- Identificação de produtos com margem negativa

### 5. **Produção** 🏭
- Volume produzido por produto
- Custo H/H (hora/homem)
- Custo unitário por produto
- Produtividade (unidades/hora)
- Análise de eficiência
- Evolução mensal de produção

---

## 🎨 Design

### Cores (Tons Pastel)
- 🟣 Roxo: `#B19CD9`
- 🟪 Violeta: `#DDA0DD`
- 🔵 Azul Claro: `#ADD8E6`
- 🌸 Rosa: `#FFB6C1`
- 🟡 Amarelo: `#FFFACD`
- ⚪ Branco: `#FFFFFF`

### Características
- Abas dedicadas para cada área (sem encavalamento de informações)
- Gráficos interativos com Plotly
- Design limpo e premium
- Responsivo para desktop e tablet

---

## 🤖 Insights Automáticos

O sistema gera automaticamente recomendações inteligentes como:

✅ "Produto X tem alta venda, mas margem negativa"  
✅ "Fornecedor Y representa risco de R$ 120k/mês"  
✅ "Canal Z cresceu 25% MoM"  
✅ "3 produtos em ruptura com impacto estimado em R$"  

---

## 🚀 Como Usar

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes)

### Instalação

1. **Clone ou descompacte o projeto**
```bash
git clone https://github.com/ArthurRodrigues0811/mica-chocolates-bi.git
cd mica-chocolates-bi
```

2. **Crie um ambiente virtual (opcional, mas recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
streamlit run app.py
```

5. **Acesse no navegador**
```
http://localhost:8501
```

---

## 📊 Dados

O protótipo utiliza **dados simulados realistas** que cobrem:
- 24+ meses de histórico (jan/2024 - abr/2026)
- 6 produtos diferentes
- 4 canais de vendas
- 50+ clientes simulados
- Sazonalidade automática (Páscoa, Natal)
- Rupturas aleatórias com impacto

Esses dados podem ser facilmente substituídos por dados reais da empresa em Excel.

---

## 💡 Diferencial: Por que Vale 30k+?

### Automação Completa
✅ Sem necessidade de atualização manual  
✅ Insights gerados automaticamente  
✅ Alertas inteligentes  

### Excelência e Rigor
✅ Design premium com paleta personalizada  
✅ Informações bem estruturadas (sem poluição visual)  
✅ KPIs alinhados com decisões estratégicas  

### Foco em Rentabilidade
✅ Sai de "quanto vendeu?" para "onde ganha dinheiro?"  
✅ Análise de margem por produto  
✅ Curva ABC de clientes  

### Escalável
✅ Fácil integração com dados reais (Excel, SQL, APIs)  
✅ Preparado para crescimento da empresa  
✅ Interface profissional para apresentações  

---

## 🔧 Personalização para Mica Chocolates

Para adaptar ao dados reais da empresa:

1. **Substitua os geradores de dados** nas funções `gerar_dados_*()` com leitura de arquivos Excel
2. **Ajuste os produtos** para as linhas reais (ex: Linha Premium, Linha Infantil)
3. **Configure os canais** de distribuição atuais
4. **Integre com banco de dados** SQL quando necessário

---

## 📞 Suporte

Para dúvidas ou customizações:
- Documentação: Veja os comentários no código
- Email: arthur.rodrigues@seu-email.com

---

## 📄 Licença

Protótipo desenvolvido para Mica Chocolates - 2026