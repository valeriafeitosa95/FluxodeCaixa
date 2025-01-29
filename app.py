# Importando as bibliotecas
import streamlit as st
import pandas as pd
import plotly_express as px

# Configuração da página
st.set_page_config(page_title= 'Fluxo de Caixa', layout='wide', page_icon='📈')

# Link CSS
with open('style.css') as f:st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Título principal
st.header('Fluxo de Caixa', divider='red')
st.write('')
st.write('')

# Leitura dos dados
dfDados = pd.read_excel('data/FluxodeCaixa.xlsx')
dfDados['Ano'] = dfDados['Ano'].astype(str)

# Filtros sidebar
selec_local = st.sidebar.radio('Selecione o Local', ['Todos os Locais','Porto Alegre','Rio de Janeiro','São Paulo'])
if selec_local == 'Todos os Locais':
    filtro = dfDados
elif selec_local == 'Porto Alegre':
    filtro = dfDados.query('Local == "Porto Alegre"')
elif selec_local == 'Rio de Janeiro':
    filtro = dfDados.query('Local == "Rio de Janeiro"')
else:
    filtro = dfDados.query('Local == "São Paulo"')

selec_custo = st.sidebar.radio('Selecione o Centro de Custos', ['Todos os Centros de Custos','Administrativo','Comercial','Financeiro', 'Marketing', 'Operacional'])
if selec_custo == 'Todos os Centros de Custos':
    filtro2 = filtro
elif selec_custo == 'Administrativo':
    filtro2 = filtro.query('Centro_de_Custos == "Administrativo"')
elif selec_custo == 'Comercial':
    filtro2 = filtro.query('Centro_de_Custos == "Comercial"')
elif selec_custo == 'Financeiro':
    filtro2 = filtro.query('Centro_de_Custos == "Financeiro"')
elif selec_custo == 'Marketing':
    filtro2 = filtro.query('Centro_de_Custos == "Marketing"')
else:
    filtro2 = filtro.query('Centro_de_Custos == "Operacional"')

selec_ano = st.sidebar.radio('Selecione o ano', ['Todos os anos','2019', '2020', '2021'])
if selec_ano == 'Todos os anos':
    filtro3 = filtro2
elif selec_ano == '2019':
    filtro3 = filtro2.query('Ano == "2019"')
elif selec_ano == '2020':
    filtro3 = filtro2.query('Ano == "2020"')
else:
    filtro3 = filtro2.query('Ano == "2021"')

# Mostrando quais filtro estão selecionados no momento
st.html(f'<span class="Tvisual">Visualizando Agora:</span><p class="visual">{selec_local}</p><p class="visual">{selec_custo}</p><p class="visual">{selec_ano}</p>')
st.write('')
st.write('')
st.write('')

# Separando a coluna movimentação em entradas e saídas, utilizando a base com os 3 filtros, e agrupando por classificação para os dois gráficos de colunas
entradas = filtro3.query('Movimentação == "Entradas"')
Class = entradas.groupby('Classificação', as_index=True)['Valor'].sum()
saidas = filtro3.query('Movimentação == "Saídas"')
Class_ = saidas.groupby('Classificação', as_index=True)['Valor'].sum().abs()

# Separando a coluna movimentação em entradas e saídas, utilizando a base com os 3 filtros, e somando os valores para calcular o saldo e a margem de lucro
EntradasM = filtro3.loc[filtro3['Movimentação'] == 'Entradas', 'Valor'].sum()
SaidasM = filtro3.loc[filtro3['Movimentação'] == 'Saídas', 'Valor'].abs().sum()
Saldo = EntradasM - SaidasM
margem_lucro = (EntradasM - SaidasM) / EntradasM * 100

# Métricas gerais nas colunas 1, 2, 3 e 4
col1, col2, col3, col4 = st.columns(4, vertical_alignment= 'center')
with col1:
    with st.container(border=True):
        entrada = entradas['Valor'].sum()
        entrada = '{0:,}'.format(entrada).replace(',','.')
        st.metric(label='**Entradas**', value= entrada)
with col2:
    with st.container(border=True):
        saida = saidas['Valor'].abs().sum()
        saida = '{0:,}'.format(saida).replace(',','.')
        st.metric(label='**Saídas**', value= saida)
with col3:
    with st.container(border=True):
        saldo = Saldo
        saldo = '{0:,}'.format(saldo).replace(',','.')
        st.metric(label='**Saldo Final**', value= saldo)
with col4:
    with st.container(border=True):
        margem = round(margem_lucro, 2)
        st.metric(label='**Margem de Lucro %**', value= margem)
st.write(' ')
st.write(' ')

# Gráficos de barras de entradas e saídas por classificação
col5, col6 = st.columns(2)
with col5:
    fig = px.bar(Class, color_discrete_sequence=px.colors.diverging.Picnic_r, text_auto=True)
    fig.update_layout(title_text = 'Entradas')
    fig.update_layout(font={'family':'Arial','size': 14, 'color': 'white'}, separators=".,", showlegend = False)
    fig.update_layout(paper_bgcolor='#9E0000', plot_bgcolor='#9E0000')
    fig.update_yaxes(visible=False)
    fig.update_xaxes(title = ' ')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True)
with col6:  
    fig = px.bar(Class_, color_discrete_sequence=px.colors.diverging.Picnic_r, text_auto=True)
    fig.update_layout(title_text = 'Saídas', title_xref='paper')
    fig.update_layout(font={'family':'Arial','size': 14, 'color': 'white'}, separators=".,", showlegend = False)
    fig.update_layout(paper_bgcolor='#9E0000', plot_bgcolor='#9E0000')
    fig.update_yaxes(visible=False)
    fig.update_xaxes(title = ' ')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True)

# Separando os valores de entradas e saidas, utilizando a base com apenas 2 dos 3 filtros, agrupando por ano e somando os valores
Entradas = filtro2.query('Movimentação == "Entradas"')
Saidas = filtro2.query('Movimentação == "Saídas"')

# Filtrando os valores por movimentação e por ano, e somando os valores
E2019 = Entradas.loc[Entradas['Ano'] == '2019', 'Valor'].sum()
E2020 = Entradas.loc[Entradas['Ano'] == '2020', 'Valor'].sum()
E2021 = Entradas.loc[Entradas['Ano'] == '2021', 'Valor'].sum()

S2019 = Saidas.loc[Saidas['Ano'] == '2019', 'Valor'].abs().sum()
S2020 = Saidas.loc[Saidas['Ano'] == '2020', 'Valor'].abs().sum()
S2021 = Saidas.loc[Saidas['Ano'] == '2021', 'Valor'].abs().sum()

# Criando um novo data frame utilizando os valores filtrados acima.
ano = {'Ano':['2019','2020','2021'], 'Entradas': [E2019, E2020, E2021], 'Saídas':[S2019, S2020, S2021]}
dfano = pd.DataFrame(ano)

# Tooltip 
st.html('<div class="tooltip"><div class="icon">🛈</div><span class="tooltiptext">Clique na legenda para filtrar.</span></div>')

# Gráfico de linha que mostrará o valores de todos os locais e centro de custos em todos os anos
fig = px.line(dfano, x='Ano', y=['Entradas', 'Saídas'], markers= True, color_discrete_sequence=px.colors.diverging.Picnic_r)
fig.update_layout(title_text = 'Entradas x Saídas por Ano', title_xref='paper')
fig.update_layout(font={'family':'Arial','size': 14, 'color': 'white'}, separators=".,", autotypenumbers='strict')
fig.update_layout(yaxis = dict (showgrid = True, gridcolor='grey'), paper_bgcolor='#9E0000', plot_bgcolor='#9E0000')
fig.update_layout(showlegend = True, legend_title=' ')
fig.update_yaxes(title = '')
fig.update_xaxes(title = ' ')
st.plotly_chart(fig, use_container_width=True)


