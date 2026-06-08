import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# CONFIGURACIÓN
# ======================

st.set_page_config(
    page_title="IA e Inventarios",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inteligencia Artificial para la Optimización de Inventarios")
st.markdown("""
### Pregunta de investigación
**¿Cómo se utiliza la Inteligencia Artificial para optimizar la gestión de inventarios en empresas comerciales?**

**Keywords:**
- Artificial Intelligence
- Inventory Management
- Supply Chain
- Demand Forecasting
""")

# ======================
# CSV
# ======================

st.sidebar.header("Fuente de datos")

uploaded_file = st.sidebar.file_uploader(
    "Subir otro CSV",
    type=["csv"]
)

GITHUB_CSV_URL = "https://github.com/Gustavox2019/PA3/blob/main/scopus_inventory_ai.csv"

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.sidebar.success("CSV cargado manualmente")

else:

    df = pd.read_csv(GITHUB_CSV_URL)

    st.sidebar.success("CSV cargado desde GitHub")

# ======================
# LIMPIEZA
# ======================

df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["citation_count"] = pd.to_numeric(df["citation_count"], errors="coerce")

# ======================
# FILTROS
# ======================

st.sidebar.header("Filtros")

years = sorted(df["year"].dropna().unique())

selected_years = st.sidebar.multiselect(
    "Selecciona años",
    years,
    default=years
)

df_filtered = df[df["year"].isin(selected_years)]

# ======================
# KPIs
# ======================

c1, c2, c3, c4 = st.columns(4)

c1.metric("Artículos", len(df_filtered))
c2.metric("Revistas", df_filtered["publication_name"].nunique())
c3.metric("Autores", df_filtered["authors"].nunique())
c4.metric(
    "Citas Totales",
    int(df_filtered["citation_count"].fillna(0).sum())
)

st.divider()

# ======================
# PUBLICACIONES POR AÑO
# ======================

st.subheader("📈 Publicaciones por Año")

pub_year = (
    df_filtered
    .groupby("year")
    .size()
    .reset_index(name="Cantidad")
)

fig_year = px.line(
    pub_year,
    x="year",
    y="Cantidad",
    markers=True
)

st.plotly_chart(fig_year, use_container_width=True)

# ======================
# TOP ARTÍCULOS CITADOS
# ======================

st.subheader("🏆 Top 10 Artículos Más Citados")

top_cited = (
    df_filtered
    .sort_values("citation_count", ascending=False)
    .head(10)
    .copy()
)

# Acortar títulos largos
top_cited["short_title"] = top_cited["title"].apply(
    lambda x: x[:60] + "..." if len(str(x)) > 60 else str(x)
)

fig_cited = px.bar(
    top_cited,
    x="citation_count",
    y="short_title",
    orientation="h",
    hover_data=["title"],  # muestra título completo al pasar el mouse
    labels={
        "citation_count": "Número de citas",
        "short_title": "Artículo"
    }
)

fig_cited.update_layout(
    height=700,
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(fig_cited, use_container_width=True)
# ======================
# TOP REVISTAS
# ======================

st.subheader("📚 Revistas con Más Publicaciones")

top_journals = (
    df_filtered["publication_name"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_journals.columns = ["Revista", "Publicaciones"]

fig_journal = px.bar(
    top_journals,
    x="Publicaciones",
    y="Revista",
    orientation="h"
)

st.plotly_chart(fig_journal, use_container_width=True)

# ======================
# DISTRIBUCIÓN DE CITAS
# ======================

st.subheader("📊 Distribución de Citas")

fig_hist = px.histogram(
    df_filtered,
    x="citation_count",
    nbins=30
)

st.plotly_chart(fig_hist, use_container_width=True)

# ======================
# TABLA
# ======================

st.subheader("📄 Dataset")

st.dataframe(
    df_filtered,
    use_container_width=True
)

# ======================
# CONCLUSIÓN
# ======================

st.subheader("📝 Conclusión")

st.write(
    """
    El análisis de artículos indexados en Scopus permite observar
    el crecimiento del interés científico en el uso de Inteligencia Artificial
    para la gestión de inventarios, predicción de demanda y optimización
    de cadenas de suministro.
    """
)
