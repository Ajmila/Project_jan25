# Function to import data from CSV to MongoDB
def import_csv_to_mongodb(csv_file, collection):
    # Read CSV file into a pandas DataFrame
    data = pd.read_csv(csv_file)
    

    
    
    # Convert DataFrame to dictionary
    data_dict = data.to_dict(orient='records')
    
    # Insert data into MongoDB collection
    collection.insert_many(data_dict)
    
   
    
    print("Data imported successfully into MongoDB.")

# Example usage
if __name__ == "__main__":
    csv_file = 'Data/names.csv'  # Path to your CSV file
    collection_name = student_collection  # Name of the MongoDB collection
    
    
    import_csv_to_mongodb(csv_file, collection_name)

