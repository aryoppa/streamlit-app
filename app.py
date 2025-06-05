import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration for a wider layout
st.set_page_config(layout="wide")

# Title of the dashboard
st.title("Simple Dashboard Presentasi Data Simulasi")

# --- Data Loading ---
@st.cache_data
def load_data():
    """Loads the data from data_simulasi.csv."""
    try:
        df = pd.read_csv('data_simulasi.csv')
        # Convert 'Jam Login' to datetime objects
        df['Jam Login'] = pd.to_datetime(df['Jam Login'])
        # Extract 'Jam' (Hour) and 'Hari' (Day) for analysis, if not already present
        if 'Jam' not in df.columns:
            df['Jam'] = df['Jam Login'].dt.hour
        if 'Hari' not in df.columns:
            df['Hari'] = df['Jam Login'].dt.day_name()
        return df
    except FileNotFoundError:
        st.error("Error: 'data_simulasi.csv' not found. Please make sure the file is in the same directory.")
        return pd.DataFrame() # Return an empty DataFrame on error

df = load_data()

if not df.empty:
    # --- Sidebar Filters ---
    st.sidebar.header("Filter Data")

    # Merk HP (Mobile Phone Brand) filter
    selected_merk_hp = st.sidebar.multiselect(
        "Pilih Merk HP:",
        options=df['Merk HP'].unique(),
        default=df['Merk HP'].unique()
    )

    # Tipe Lokasi (Location Type) filter
    selected_tipe_lokasi = st.sidebar.multiselect(
        "Pilih Tipe Lokasi:",
        options=df['Tipe Lokasi'].unique(),
        default=df['Tipe Lokasi'].unique()
    )

    # Kategori Usia (Age Category) filter
    selected_kategori_usia = st.sidebar.multiselect(
        "Pilih Kategori Usia:",
        options=df['Kategori Usia'].unique(),
        default=df['Kategori Usia'].unique()
    )

    # Apply filters
    filtered_df = df[
        (df['Merk HP'].isin(selected_merk_hp)) &
        (df['Tipe Lokasi'].isin(selected_tipe_lokasi)) &
        (df['Kategori Usia'].isin(selected_kategori_usia))
    ]

    # --- Main Content Area ---

    st.subheader("Sekilas Data (Filtered)")
    st.write(f"Jumlah baris setelah filter: {len(filtered_df)} dari {len(df)}")
    st.dataframe(filtered_df.head())

    st.subheader("Statistik Deskriptif")
    st.write("Statistik Numerik:")
    st.dataframe(filtered_df.describe())
    st.write("Statistik Kategorikal:")
    st.dataframe(filtered_df.describe(include='object'))
    st.write("Tipe Data:")
    st.dataframe(filtered_df.dtypes.astype(str).rename('Data Type').to_frame())

    # --- Visualizations ---
    st.header("Visualisasi Data")

    # Row 1: Distribution of Minat Digital
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribusi Minat Digital")
        fig_hist = px.histogram(filtered_df, x='Minat Digital', nbins=20,
                                title='Histogram Minat Digital',
                                labels={'Minat Digital': 'Skor Minat Digital'},
                                color_discrete_sequence=px.colors.qualitative.Plotly)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        st.subheader("Minat Digital Berdasarkan Merk HP")
        avg_interest_by_merk = filtered_df.groupby('Merk HP')['Minat Digital'].mean().reset_index()
        fig_bar_merk = px.bar(avg_interest_by_merk, x='Merk HP', y='Minat Digital',
                              title='Rata-rata Minat Digital per Merk HP',
                              labels={'Merk HP': 'Merk HP', 'Minat Digital': 'Rata-rata Minat Digital'},
                              color='Merk HP',
                              color_discrete_sequence=px.colors.qualitative.Set1)
        st.plotly_chart(fig_bar_merk, use_container_width=True)

    # Row 2: Minat Digital by Tipe Lokasi and Jam Login Trend
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Minat Digital Berdasarkan Tipe Lokasi")
        avg_interest_by_lokasi = filtered_df.groupby('Tipe Lokasi')['Minat Digital'].mean().reset_index()
        fig_bar_lokasi = px.bar(avg_interest_by_lokasi, x='Tipe Lokasi', y='Minat Digital',
                                title='Rata-rata Minat Digital per Tipe Lokasi',
                                labels={'Tipe Lokasi': 'Tipe Lokasi', 'Minat Digital': 'Rata-rata Minat Digital'},
                                color='Tipe Lokasi',
                                color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_bar_lokasi, use_container_width=True)

    with col4:
        st.subheader("Minat Digital Berdasarkan Waktu Login (Jam)")
        # Group by hour and calculate mean of 'Minat Digital'
        interest_by_hour = filtered_df.groupby('Jam')['Minat Digital'].mean().reset_index()
        fig_line_hour = px.line(interest_by_hour, x='Jam', y='Minat Digital',
                                title='Rata-rata Minat Digital Berdasarkan Jam Login',
                                labels={'Jam': 'Jam Login (0-23)', 'Minat Digital': 'Rata-rata Minat Digital'},
                                markers=True,
                                line_shape='linear',
                                color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_line_hour.update_xaxes(dtick=1) # Ensure all hours are visible on x-axis
        st.plotly_chart(fig_line_hour, use_container_width=True)

else:
    st.warning("Tidak ada data untuk ditampilkan. Pastikan 'data_simulasi.csv' tersedia dan berisi data.")

