import streamlit as st
import pandas as pd
import plotly.express as px
import webbrowser 



st.set_page_config(
    page_title="Painel Geo Brasil",
    page_icon="🗺️",
    layout="wide"
)


st.write("## 🗺️ Seja Bem-Vindo ao Painel de Dados Geográficos Brasil")

# if "data" not in st.session_state:
#     df_data = pd.read_csv("dataset/FIFA23_official_data.csv", index_col=0)
#     st.session_state["data"] = df_data
#     df_data



st.sidebar.write('Desenvolvido por: Joniel Maycon')

btn = st.sidebar.button('Acesse o acesse meu GitHub')
if btn:
    webbrowser.open_new_tab("https://github.com/JonMaycon")



# Dados dos estados com suas coordenadas centrais aproximadas e população estimada
estado_data = {
    "estado": ["Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",
               "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul",
               "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro",
               "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", "Santa Catarina",
               "São Paulo", "Sergipe", "Tocantins"],
    "latitude": [-9.974, -9.571, 1.414, -3.416, -12.971, -3.717, -15.797,
                 -19.019, -15.827, -2.529, -12.642, -20.469, -18.512, -5.53, -7.121,
                 -25.428, -8.047, -5.093, -22.906, -5.794, -30.033, -8.761, 2.823, -27.595,
                 -23.550, -10.947, -10.184],
    "longitude": [-67.81, -36.556, -51.331, -65.858, -38.501, -38.543, -47.882,
                  -40.343, -47.921, -44.302, -55.424, -54.612, -44.555, -52.294, -34.877,
                  -49.273, -34.877, -42.811, -43.177, -35.209, -51.229, -63.904, -60.675, -48.548,
                  -46.633, -37.073, -48.327],
    "populacao": [906876, 3351543, 861773, 4207714, 14930634, 9187103, 3094325,
                  4064052, 7113540, 7114598, 3526220, 2809394, 21411923, 8777124, 4059905,
                  11516840, 9674793, 3281480, 17366189, 3560903, 11422973, 1805876, 652713, 7338473,
                  46649132, 2338474, 1590248]
}

estado_df = pd.DataFrame(estado_data)

# Criando o mapa com plotly express
fig_mapa = px.scatter_geo(
    estado_df,
    lat="latitude",
    lon="longitude",
    text="estado",
    size="populacao",
    color="populacao",
    hover_name="estado",
    color_continuous_scale=px.colors.sequential.Plasma,
    size_max=40,
    projection="natural earth"
)

# Atualizando o layout para focar no Brasil
fig_mapa.update_geos(
    center=dict(lat=-14.2350, lon=-51.9253),
    fitbounds="locations",
    showcountries=True,
    countrycolor="Black",
    showsubunits=True,
    subunitcolor="Blue",
    landcolor="lightgray",
    coastlinecolor="White",
    showland=True,
    showocean=True,
    oceancolor="LightBlue"
)

fig_mapa.update_layout(
    title_text="População dos Estados Brasileiros",
    margin={"r":0,"t":50,"l":0,"b":0}
)

# Exibindo o mapa no Streamlit
st.plotly_chart(fig_mapa, use_container_width=True)

# ------------------------------------------------------------------------
# Dados das 10 maiores cidades do Brasil por população
cidade_data = {
    "cidade": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza",
               "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Goiânia"],
    "estado": ["São Paulo", "Rio de Janeiro", "Distrito Federal", "Bahia", "Ceará",
               "Minas Gerais", "Amazonas", "Paraná", "Pernambuco", "Goiás"],
    "populacao": [12325232, 6747815, 3055149, 2886698, 2686612,
                  2521564, 2182763, 1963726, 1653461, 1536097]
}

cidade_df = pd.DataFrame(cidade_data)

# Criando o gráfico de barras
fig_cidades = px.bar(
    cidade_df.sort_values(by="populacao", ascending=False),
    x="cidade",
    y="populacao",
    text="populacao",
    labels={"cidade": "Cidade", "populacao": "População"},
    color="populacao",
    color_continuous_scale=px.colors.sequential.Viridis,
    title="População das 10 Maiores Cidades do Brasil"
)

fig_cidades.update_traces(texttemplate='%{text:.3s}', textposition='outside')
fig_cidades.update_layout(
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    xaxis_tickangle=-45,
    margin=dict(t=50, b=100),
    yaxis=dict(title="População", showgrid=True),
    plot_bgcolor='rgba(0,0,0,0)'
)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig_cidades, use_container_width=True)


# Exibindo a tabela com os dados
st.dataframe(estado_data)







