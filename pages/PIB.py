import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import plotly.express as px

st.set_page_config(
    page_title="Dados PIB",
    page_icon="📊",
    layout="wide"
)

st.write("## 📊 Dados PIB por Estado")

# Dados dos estados com suas coordenadas centrais aproximadas e PIB em milhões de reais
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
    "pib": [21.374, 76.266, 20.100, 131.531, 352.618, 194.885, 286.944,
            186.337, 269.628, 124.981, 233.390, 142.204, 857.593, 262.905, 77.470,
            549.973, 220.814, 64.028, 949.301, 80.181, 581.284, 58.170, 18.203, 428.571,
            2719.751, 51.861, 51.781]
}

estado_df = pd.DataFrame(estado_data)

# Criando o mapa com Folium
mapa = folium.Map(location=[-14.2350, -51.9253], zoom_start=4, tiles='OpenStreetMap')

# Adicionando um choropleth para destacar o PIB dos estados
folium.Choropleth(
    geo_data="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
    name="choropleth",
    data=estado_df,
    columns=["estado", "pib"],
    key_on="feature.properties.name",
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="PIB (R$ milhões)"
).add_to(mapa)

# Adicionando marcadores para cada estado
marker_cluster = MarkerCluster().add_to(mapa)
for i in range(len(estado_df)):
    folium.Marker(
        location=[estado_df.iloc[i]['latitude'], estado_df.iloc[i]['longitude']],
        popup=f"{estado_df.iloc[i]['estado']} - PIB: R$ {estado_df.iloc[i]['pib']} milhões",
        icon=folium.Icon(color='green', icon='info-sign')
    ).add_to(marker_cluster)

# Exibindo o mapa no Streamlit com centralização
map_container = st.empty()
with map_container:
    folium_static(mapa, width=800, height=600)

# Criando o gráfico de bolhas com os valores de PIB nas bolhas
fig_bolha = px.scatter(
    estado_df.sort_values(by="pib", ascending=False),
    x="estado",
    y="pib",
    size="pib",
    color="pib",
    hover_name="estado",
    size_max=60,
    text="pib",  # Adiciona o PIB como texto dentro das bolhas
    title="PIB dos Estados Brasileiros",
    labels={"estado": "Estado", "pib": "PIB (R$ milhões)"},
    color_continuous_scale=px.colors.sequential.Blues
)

fig_bolha.update_traces(texttemplate='%{text:.2f}', textposition='middle center')

fig_bolha.update_layout(
    xaxis_tickangle=-45,
    margin=dict(t=50, b=100),
    yaxis=dict(title="PIB (R$ milhões)", showgrid=True),
    plot_bgcolor='rgba(0,0,0,0)'
)

# Exibindo o gráfico de bolhas no Streamlit com centralização
st.plotly_chart(fig_bolha, use_container_width=True)
