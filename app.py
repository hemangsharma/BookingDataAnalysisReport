import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Booking Data Dashboard", layout="wide")
sns.set(style="whitegrid")

# Load and clean data
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)

    date_cols = ['Check-in', 'Check-out', 'Booked on', 'Cancellation date']
    for col in date_cols:
        data[col] = pd.to_datetime(data[col], errors='coerce')

    data['Price'] = data['Price'].replace({'\$': '', 'AUD': '', ',': ''}, regex=True).astype(float)
    data['Commission amount'] = data['Commission amount'].replace({'\$': '', 'AUD': '', ',': ''}, regex=True).astype(float)
    data['Payment method'] = pd.to_numeric(data['Payment method'], errors='coerce')
    data.dropna(subset=['Price', 'Commission amount'], inplace=True)

    return data

# Upload file or use default
uploaded_file = st.file_uploader("Upload Booking CSV File", type="csv")
if uploaded_file:
    data = load_data(uploaded_file)
else:
    st.info("Using default sample file. Upload your own CSV for analysis.")
    data = load_data("file.csv")  # Replace with your default file

# Sidebar Filters
st.sidebar.header("Filters")

status_filter = st.sidebar.multiselect("Select Booking Status", options=data['Status'].dropna().unique(), default=data['Status'].dropna().unique())
country_filter = st.sidebar.multiselect("Select Booker Country", options=data['Booker country'].dropna().unique(), default=data['Booker country'].dropna().unique())
purpose_filter = st.sidebar.multiselect("Select Travel Purpose", options=data['Travel purpose'].dropna().unique(), default=data['Travel purpose'].dropna().unique())

filtered_data = data[
    (data['Status'].isin(status_filter)) &
    (data['Booker country'].isin(country_filter)) &
    (data['Travel purpose'].isin(purpose_filter))
]

st.title("📊 Booking Data Interactive Dashboard")

# Total Bookings Over Time
st.subheader("Total Bookings Over Time")
bookings_by_month = filtered_data['Booked on'].dt.to_period('M').value_counts().sort_index()
fig1, ax1 = plt.subplots(figsize=(12, 4))
bookings_by_month.plot(kind='bar', color='skyblue', ax=ax1)
ax1.set_xlabel("Month")
ax1.set_ylabel("Number of Bookings")
st.pyplot(fig1)

# Price Distribution
st.subheader("Distribution of Booking Prices")
fig2, ax2 = plt.subplots(figsize=(12, 4))
sns.histplot(filtered_data['Price'], bins=30, kde=True, color='purple', ax=ax2)
ax2.set_xlabel("Price")
ax2.set_ylabel("Frequency")
st.pyplot(fig2)

# Bookings by Status
st.subheader("Bookings by Status")
fig3, ax3 = plt.subplots(figsize=(12, 4))
sns.countplot(data=filtered_data, x='Status', order=filtered_data['Status'].value_counts().index, ax=ax3)
st.pyplot(fig3)

# Average Price by Travel Purpose
st.subheader("Average Price by Travel Purpose")
avg_price = filtered_data.groupby('Travel purpose')['Price'].mean().sort_values()
fig4, ax4 = plt.subplots(figsize=(12, 4))
avg_price.plot(kind='barh', color='teal', ax=ax4)
st.pyplot(fig4)

# Bookings by Device
st.subheader("Bookings by Device")
fig5, ax5 = plt.subplots(figsize=(12, 4))
sns.countplot(data=filtered_data, x='Device', order=filtered_data['Device'].value_counts().index, ax=ax5)
st.pyplot(fig5)

# Bookings by Rooms
st.subheader("Bookings by Number of Rooms")
fig6, ax6 = plt.subplots(figsize=(12, 4))
sns.countplot(data=filtered_data, x='Rooms', order=filtered_data['Rooms'].value_counts().index, palette='pastel', ax=ax6)
st.pyplot(fig6)

# Average Price by Adults
st.subheader("Average Price by Number of Adults")
fig7, ax7 = plt.subplots(figsize=(12, 4))
filtered_data.groupby('Adults')['Price'].mean().sort_index().plot(kind='bar', color='orange', ax=ax7)
ax7.set_xlabel("Number of Adults")
ax7.set_ylabel("Average Price")
st.pyplot(fig7)

# Bookings by Country
st.subheader("Bookings by Country")
fig8, ax8 = plt.subplots(figsize=(12, 4))
sns.countplot(data=filtered_data, x='Booker country', order=filtered_data['Booker country'].value_counts().index, palette='pastel', ax=ax8)
plt.xticks(rotation=45)
st.pyplot(fig8)

# Show raw data
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_data)
