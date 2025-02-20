import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV file
data = pd.read_csv('data.csv')

# Set up the page
st.set_page_config(page_title='Bundesliga Dashboard', layout='wide')
st.title('🏆 Bundesliga Spieler-Dashboard')

# Sidebar for filtering
st.sidebar.header('🔍 Filter')
nationalities = st.sidebar.multiselect('Nationalität auswählen', options=data['nationality'].unique(), default=data['nationality'].unique())
clubs = st.sidebar.multiselect('Verein auswählen', options=data['club'].unique(), default=data['club'].unique())
position = st.sidebar.selectbox('Position auswählen', options=['Alle'] + list(data['position'].unique()))

# Apply filters
filtered_data = data[data['nationality'].isin(nationalities) & data['club'].isin(clubs)]
if position != 'Alle':
    filtered_data = filtered_data[filtered_data['position'] == position]

# Main Dashboard Content
with st.container():
    st.subheader('📊 Wichtige Kennzahlen')
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric('👥 Anzahl Spieler', len(filtered_data))
    with col2:
        st.metric('💰 Durchschnittspreis (€)', f"{filtered_data['price'].mean():,.2f}")
    with col3:
        st.metric('🎯 Höchster Marktwert (€)', f"{filtered_data['max_price'].max():,.2f}")
    with col4:
        st.metric('📏 Durchschnittsgröße (cm)', f"{filtered_data['height'].mean():.1f}")

# Visualizations
st.subheader('📈 Datenvisualisierung')

# Age distribution
fig_age = px.histogram(filtered_data, x='age', nbins=20, title='Altersverteilung der Spieler')
st.plotly_chart(fig_age, use_container_width=True)

# Market value by club
fig_value = px.bar(filtered_data.groupby('club')['price'].mean().sort_values(ascending=False).head(10).reset_index(),
                   x='club', y='price', title='Top 10 Vereine nach Durchschnittspreis')
st.plotly_chart(fig_value, use_container_width=True)

# Table view
st.subheader('📝 Detaillierte Spielerdaten')
st.dataframe(filtered_data)

# Footer
st.markdown('---')
st.markdown('⚽️ Bundesliga Dashboard OAMK Project')
