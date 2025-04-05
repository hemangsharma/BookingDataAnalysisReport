import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# Load the CSV file
file_path = 'file.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Display basic information about the dataset
print(data.info())
print(data.describe())

# Data Cleaning
# Convert date columns to datetime
data['Check-in'] = pd.to_datetime(data['Check-in'], errors='coerce')
data['Check-out'] = pd.to_datetime(data['Check-out'], errors='coerce')
data['Booked on'] = pd.to_datetime(data['Booked on'], errors='coerce')
data['Cancellation date'] = pd.to_datetime(data['Cancellation date'], errors='coerce')

# Clean the 'Price' column
data['Price'] = data['Price'].replace({'\$': '', 'AUD': '', ',': ''}, regex=True).astype(float)

# Clean the 'Commission amount' column if necessary
data['Commission amount'] = data['Commission amount'].replace({'\$': '', 'AUD': '', ',': ''}, regex=True).astype(float)

# Clean the 'Payment method' column if necessary
data['Payment method'] = pd.to_numeric(data['Payment method'], errors='coerce')

# Handle missing values (optional)
data.dropna(subset=['Price', 'Commission amount'], inplace=True)

# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Create a PDF report
with PdfPages('data_analysis_report.pdf') as pdf:
    # 1. Total Bookings Over Time
    plt.figure(figsize=(12, 6))
    data['Booked on'].dt.to_period('M').value_counts().sort_index().plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Total Bookings Over Time', fontsize=16)
    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Number of Bookings', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # 2. Distribution of Prices
    plt.figure(figsize=(12, 6))
    sns.histplot(data['Price'], bins=30, kde=True, color='purple', edgecolor='black')
    plt.title('Distribution of Prices', fontsize=16)
    plt.xlabel('Price', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # 3. Bookings by Status
    plt.figure(figsize=(12, 6))
    sns.countplot(data=data, x='Status', order=data['Status'].value_counts().index)  # Removed palette
    plt.title('Bookings by Status', fontsize=16)
    plt.xlabel('Status', fontsize=14)
    plt.ylabel('Number of Bookings', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # 4. Average Price by Travel Purpose
    plt.figure(figsize=(12, 6))
    avg_price_by_purpose = data.groupby('Travel purpose')['Price'].mean().sort_values()
    avg_price_by_purpose.plot(kind='barh', color='teal', edgecolor='black')
    plt.title('Average Price by Travel Purpose', fontsize=16)
    plt.xlabel('Average Price', fontsize=14)
    plt.ylabel('Travel Purpose', fontsize=14)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # 5. Bookings by Device
    plt.figure(figsize=(12, 6))
    sns.countplot(data=data, x='Device', order=data['Device'].value_counts().index)  # Removed palette
    plt.title('Bookings by Device', fontsize=16)
    plt.xlabel('Device', fontsize=14)
    plt.ylabel('Number of Bookings', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # 6. Bookings by Number of Rooms
    plt.figure(figsize=(12, 6))
    sns.countplot(data=data, x='Rooms', order=data['Rooms'].value_counts().index, palette='pastel')
    plt.title('Bookings by Number of Rooms', fontsize=16)
    plt.xlabel('Number of Rooms', fontsize=14)
    plt.ylabel('Number of Bookings', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # 7. Average Price by Number of Adults
    plt.figure(figsize=(12, 6))
    avg_price_by_adults = data.groupby('Adults')['Price'].mean().sort_index()
    avg_price_by_adults.plot(kind='bar', color='orange', edgecolor='black')
    plt.title('Average Price by Number of Adults', fontsize=16)
    plt.xlabel('Number of Adults', fontsize=14)
    plt.ylabel('Average Price', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # 8. Bookings by Country
    plt.figure(figsize=(12, 6))
    sns.countplot(data=data, x='Booker country', order=data['Booker country'].value_counts().index, palette='pastel')
    plt.title('Bookings by Country', fontsize=16)
    plt.xlabel('Country', fontsize=14)
    plt.ylabel('Number of Bookings', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

print("Data analysis report has been generated and saved as 'data_analysis_report.pdf'.")