import pandas as pd  # Import pandas for data manipulation and analysis
import sqlite3  # Import sqlite3 for database operations
 
import socket  # Import socket for network-related operations
import platform  # Import platform for system-specific parameters and functions
 
# Load customer and orders data from CSV files
customers_df = pd.read_csv('customer.csv')
orders_df = pd.read_csv('orders.csv')
 
# Merge the customer and orders dataframes on the 'CustomerID' column
merged_df = pd.merge(orders_df, customers_df, on='CustomerID', how='inner')
 
# Calculate the total amount for each order by multiplying Quantity and Price
merged_df['TotalAmount'] = merged_df['Quantity'] * merged_df['Price']
 
# Determine the order status based on whether the order date starts with '2025-03'
merged_df['Status'] = merged_df['OrderDate'].apply(lambda d: 'New' if d.startswith('2025-03') else 'Old')
 
# Filter out orders with a total amount greater than 5000
high_value_orders = merged_df[merged_df['TotalAmount'] > 5000]
 
# Connect to the SQLite database
conn = sqlite3.connect('ecommerce.db')
 
# Create the 'HighValueOrders' table if it does not exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS HighValueOrders (
    OrderID INTEGER,
    CustomerID INTEGER,
    Name TEXT,
    Email TEXT,
    Product TEXT,
    Quantity INTEGER,
    Price REAL,
    OrderDate TEXT,
    TotalAmount REAL,
    Status TEXT
)
'''
conn.execute(create_table_query)
 
# Insert the high-value orders into the 'HighValueOrders' table, replacing any existing data
high_value_orders.to_sql('HighValueOrders', conn, if_exists='replace', index=False)
 
# Fetch and print all rows from the 'HighValueOrders' table
result = conn.execute('SELECT * FROM HighValueOrders')
for row in result.fetchall():
    print(row)
 
# Function to get the machine's IP address
def get_machine_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address
 
# Function to get the machine's name
def get_machine_name():
    machine_name = platform.node()
    return machine_name
 
if __name__ == "__main__":
    # Get and print the machine's IP address and name
    ip = get_machine_ip()
    name = get_machine_name()
    print(f"Machine IP: {ip}")
    print(f"Machine Name: {name}")
    print("my name is Eladio")  # Print a personal message
 
# Close the database connection
conn.close()
 
# Print a success message indicating the ETL process is complete
print("ETL process completed successfully!")