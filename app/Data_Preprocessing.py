import pandas as pd

# Load the data
file_path = '../payment_information.csv'
data = pd.read_csv(file_path)

# Seems like the data requires some preprocessing before it can be fed to the DB
data['payee_added_date'] = pd.to_datetime(data['payee_added_date_utc'], unit='s', errors='coerce')
print(data['payee_added_date'] )
# # Drop the original Unix timestamp column
data.drop('payee_added_date_utc', axis=1, inplace=True)

# Step 2: Standardize `payee_payment_status` to lowercase
data['payee_payment_status'] = data['payee_payment_status'].str.lower().str.strip()

# Step 3: Ensure numeric fields are clean and valid
numeric_columns = ['discount_percent', 'tax_percent', 'due_amount']
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)  # Coerce invalid values to 0

# Step 4: Standardize `payee_due_date` to consistent datetime format
data['payee_due_date'] = pd.to_datetime(data['payee_due_date'], errors='coerce')

# Step 5: Standardize text fields to lowercase and strip extra spaces
text_columns = ['payee_first_name', 'payee_last_name', 'payee_address_line_1',
                'payee_address_line_2', 'payee_city', 'payee_country', 'payee_province_or_state']
for col in text_columns:
    data[col] = data[col].str.lower().str.strip()

# Step 6: Clean phone numbers (retain only numeric characters)
data['payee_phone_number'] = data['payee_phone_number'].astype(str).str.replace(r'\D', '', regex=True)

# Step 7: Clean email addresses
data['payee_email'] = data['payee_email'].str.replace(r'[^\w\.\@\+-]', '', regex=True).str.lower()

# Step 8: Handle missing values for `payee_country` by filling with a default value (e.g., 'unknown')
data['payee_country'] = data['payee_country'].fillna('unknown')

# Step 9: Ensure the currency field is consistent and lowercase
data['currency'] = data['currency'].str.lower().str.strip()

# Print normalized data for review
print("Normalized Data:")
print(data.head())

# Save normalized data to a new CSV file for verification (optional)
data.to_csv("normalized_payment_information.csv", index=False)