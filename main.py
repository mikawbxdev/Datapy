import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV file
data = pd.read_csv('data.csv')

# Set up the page
st.set_page_config(page_title='Bundesliga Dashboard', layout='wide')
st.title('🏆 Bundesliga Player Dashboard')

# Sidebar for filtering
st.sidebar.header('🔍 Filter')
nationalities = st.sidebar.multiselect('Select Nationality', options=data['nationality'].unique(), default=data['nationality'].unique())
clubs = st.sidebar.multiselect('Select Club', options=data['club'].unique(), default=data['club'].unique())
position = st.sidebar.selectbox('Select Position', options=['All'] + list(data['position'].unique()))

# Apply filters
filtered_data = data[data['nationality'].isin(nationalities) & data['club'].isin(clubs)]
if position != 'All':
    filtered_data = filtered_data[filtered_data['position'] == position]

# Main Dashboard Content
with st.container():
    st.subheader('📊 Key Figures')
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric('👥 Number of Players', len(filtered_data))
    with col2:
        st.metric('💰 Average Price (M€)', f"{filtered_data['price'].mean():,.2f}")
    with col3:
        st.metric('🎯 Highest Market Value (M€)', f"{filtered_data['price'].max():,.2f}")
    with col4:
        st.metric('📏 Average Height (cm)', f"{filtered_data['height'].mean():.1f}")

# Visualizations
st.subheader('📈 Data Visualization')

# Age distribution
fig_age = px.histogram(filtered_data, x='age', nbins=20, title='Player Age Distribution')
st.plotly_chart(fig_age, use_container_width=True)

# Market value by club
fig_value = px.bar(filtered_data.groupby('club')['price'].mean().sort_values(ascending=False).head(10).reset_index(),
                   x='club', y='price', title='Top 10 Clubs by Average Market Value')
st.plotly_chart(fig_value, use_container_width=True)

# Table view
st.subheader('📝 Detailed Player Data')
st.dataframe(filtered_data)

# Footer
st.markdown('---')
st.markdown('⚽️ Bundesliga Dashboard OAMK Project')
