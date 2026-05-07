import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure the Streamlit page
st.set_page_config(
    page_title="Titanic Survival Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional look
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0b1120;
        color: #f8fafc;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Metrics containers */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        color: #38bdf8 !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Cards for charts */
    .css-1r6slb0, .css-12oz5g7 {
        background: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_excel('datasets/titanic.xls')
    
    # Preprocessing
    df['survived'] = df['survived'].astype(str)
    df['pclass'] = df['pclass'].astype(str)
    
    # Map Embarked
    port_map = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
    df['embarked_full'] = df['embarked'].map(port_map).fillna('Unknown')
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- Sidebar Filters ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3052/3052187.png", width=100)
st.sidebar.title("Filters")
st.sidebar.markdown("Use these filters to explore the Titanic dataset.")

# Passenger Class Filter
pclass_options = ["All"] + sorted(df['pclass'].unique().tolist())
selected_class = st.sidebar.selectbox("Passenger Class", pclass_options)

# Gender Filter
gender_options = ["All"] + sorted(df['sex'].dropna().unique().tolist())
selected_gender = st.sidebar.selectbox("Gender", gender_options)

# Embarkation Port Filter
port_options = ["All"] + sorted(df['embarked_full'].unique().tolist())
selected_port = st.sidebar.selectbox("Embarked From", port_options)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard developed for data analysis deployment.")

# --- Apply Filters ---
filtered_df = df.copy()
if selected_class != "All":
    filtered_df = filtered_df[filtered_df['pclass'] == selected_class]
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df['sex'] == selected_gender]
if selected_port != "All":
    filtered_df = filtered_df[filtered_df['embarked_full'] == selected_port]

# --- Main Dashboard Header ---
st.title("🚢 RMS Titanic Analysis Dashboard")
st.markdown("Interactive analysis of passenger demographics and survival rates aboard the RMS Titanic.")
st.markdown("---")

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)

total_passengers = len(filtered_df)
survived_count = len(filtered_df[filtered_df['survived'] == '1'])
survival_rate = (survived_count / total_passengers * 100) if total_passengers > 0 else 0
avg_age = filtered_df['age'].mean()
avg_fare = filtered_df['fare'].mean()

with col1:
    st.metric(label="Total Passengers", value=f"{total_passengers:,}")
with col2:
    st.metric(label="Overall Survival Rate", value=f"{survival_rate:.1f}%", delta=f"{survived_count} survived", delta_color="normal")
with col3:
    st.metric(label="Average Age", value=f"{avg_age:.1f}" if pd.notnull(avg_age) else "N/A")
with col4:
    st.metric(label="Average Fare", value=f"${avg_fare:.2f}" if pd.notnull(avg_fare) else "N/A")

st.markdown("---")

# --- Charts ---
# Colors mapping
surv_color_map = {'1': '#10b981', '0': '#f43f5e'}
surv_labels = {'survived': 'Status', '1': 'Survived', '0': 'Perished'}

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Survival by Age Distribution")
    # Using Histogram for age distribution
    fig_age = px.histogram(
        filtered_df, x="age", color="survived", 
        nbins=20, 
        color_discrete_map=surv_color_map,
        labels={'age': 'Age (Years)', 'survived': 'Survival Status'},
        barmode="stack",
        template="plotly_dark"
    )
    fig_age.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    # Rename legend traces
    fig_age.for_each_trace(lambda t: t.update(name = 'Survived' if t.name == '1' else 'Perished'))
    st.plotly_chart(fig_age, use_container_width=True)

with col_chart2:
    st.subheader("Gender Distribution & Survival")
    # Sunburst or Pie for gender and survival
    gender_surv = filtered_df.groupby(['sex', 'survived']).size().reset_index(name='count')
    # Remap for better labels
    gender_surv['Status'] = gender_surv['survived'].map({'1': 'Survived', '0': 'Perished'})
    fig_gender = px.sunburst(
        gender_surv, path=['sex', 'Status'], values='count',
        color='Status',
        color_discrete_map={'Survived': '#10b981', 'Perished': '#f43f5e'},
        template="plotly_dark"
    )
    fig_gender.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, l=10, r=10, b=10)
    )
    st.plotly_chart(fig_gender, use_container_width=True)


col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.subheader("Survival by Passenger Class")
    class_surv = filtered_df.groupby(['pclass', 'survived']).size().reset_index(name='count')
    fig_class = px.bar(
        class_surv, x="pclass", y="count", color="survived",
        barmode="group",
        color_discrete_map=surv_color_map,
        labels={'pclass': 'Passenger Class', 'count': 'Number of Passengers'},
        template="plotly_dark"
    )
    fig_class.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_class.for_each_trace(lambda t: t.update(name = 'Survived' if t.name == '1' else 'Perished'))
    st.plotly_chart(fig_class, use_container_width=True)

with col_chart4:
    st.subheader("Embarkation Port Analysis")
    port_counts = filtered_df['embarked_full'].value_counts().reset_index()
    port_counts.columns = ['Port', 'Count']
    fig_port = px.pie(
        port_counts, names='Port', values='Count',
        hole=0.4,
        color_discrete_sequence=['#f59e0b', '#0ea5e9', '#ec4899', '#8b5cf6'],
        template="plotly_dark"
    )
    fig_port.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, l=10, r=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_port, use_container_width=True)

st.markdown("---")
st.subheader("Raw Data Sample")
# Displaying a cleaned up version of the dataframe
display_df = filtered_df[['name', 'pclass', 'sex', 'age', 'fare', 'embarked_full', 'survived']].copy()
display_df['survived'] = display_df['survived'].map({'1': 'Yes', '0': 'No'})
display_df = display_df.rename(columns={
    'name': 'Name', 'pclass': 'Class', 'sex': 'Gender', 
    'age': 'Age', 'fare': 'Fare', 'embarked_full': 'Port', 'survived': 'Survived'
})
st.dataframe(display_df.head(100), use_container_width=True)
