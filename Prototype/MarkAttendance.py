import csv
from datetime import datetime
import ConnectDatabase

# Function to generate CSV file from MongoDB
def generate_csv_from_document(document, output_file):
    # Prepare data for CSV file
    csv_data = [['Class', 'Period', 'Date', 'Time', 'Present Students', 'Absent Students'],
                [document['class'], document['period'], document['date'], document['time'], ','.join(document.get('present', [])), ','.join(document.get('absent', []))]]
    
    # Write data to CSV file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)
    
    print("CSV file generated successfully.")




def mark_attendance(batch,period,date,time,present,absent):
    client=ConnectDatabase.connect_db()
    db=client['students']
    
    attendance_collection=db['attendance']
    
# Insert document into MongoDB collection
    inserted_document = {"class": batch, "period": period, "date": date, "time": time, "present": present, "absent": absent}
    attendance_collection.insert_one(inserted_document)
# Generate CSV file immediately after inserting the document
    generate_csv_from_document(inserted_document, 'Data/attendance.csv')
