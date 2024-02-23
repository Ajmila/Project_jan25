from deepface import DeepFace as df
import ConnectDatabase
import pickle
from bson.binary import Binary
import tempfile
import shutil

def store_pkl():
    #store pkl file to db
    client=ConnectDatabase.connect_db()
    db=client['students']
    classes_collection=db['classes']
    known_faces_collection=db['known_faces']
    attendance_collection=db['attendance']
    student_collection=db['stud_details']
    # Load data from a Pickle file
    pkl_file='Data/pkl/representations_facenet.pkl'
    with open(pkl_file, 'rb') as file:
        data_to_store = pickle.load(file)

    # Convert the loaded data to binary using pickle
    binary_data = Binary(pickle.dumps(data_to_store))

    # Insert the binary data into MongoDB
    classes_collection.insert_one({'class':'2k20','pkl': binary_data})

def recognize(detected_faces):
#recognize faces and find present students
    client=ConnectDatabase.connect_db()
    db=client['students']
    classes_collection=db['classes']
    known_faces_collection=db['known_faces']
    attendance_collection=db['attendance']
    student_collection=db['stud_details']
    # Specify the condition for fetching documents
    
    condition = {"class": "2k20"}

    # Retrieve the document from MongoDB based on the condition
    document = classes_collection.find_one(condition)

    if document:
        # Retrieve the binary data from the MongoDB document
        binary_data_from_mongo = document['pkl']

        # Create a temporary folder
        temp_folder = tempfile.mkdtemp()

        # Path to the Pickle file inside the temporary folder
        pickle_file_path = f"{temp_folder}/representations_facenet.pkl"

        # Save the binary data to the temporary folder
        with open(pickle_file_path, 'wb') as file:
            file.write(binary_data_from_mongo)


        # Load the Pickle file from mongodb
        with open(pickle_file_path, 'rb') as file:
            loaded_data = pickle.load(file)
        # Perform some processing with the loaded data-face recognition
        models=[]
        res=[]
        present=[]
        for i in range(len(detected_faces)):
            model=df.find(img_path=detected_faces[i],db_path=temp_folder,model_name="Facenet",distance_metric="euclidean",enforce_detection=False,normalization="Facenet",detector_backend='mediapipe')
            models.append(model)
        print()
        count = 0
        for model in models:
            if len(model[0]) > 0:
                name=model[0]['identity'].values[0].split('\\')[-1].split('/')[-1].split('.')[-2]
                print(count , "_ ", name)
                if name not in present:
                    present.append(name)
            else:
                print('Unknown Face detected')
            count += 1
        
        # Clean up: Delete the temporary folder and its contents
        shutil.rmtree(temp_folder)
    else:
        print("No document found with class attribute '2k20' in MongoDB.")
    return present


# Function to get absent students
def get_absent_students(present):
    client=ConnectDatabase.connect_db()
    db=client['students']
    classes_collection=db['classes']
    known_faces_collection=db['known_faces']
    attendance_collection=db['attendance']
    student_collection=db['stud_details']
    
    # Query MongoDB for students not present
    absent_students = student_collection.find({'name': {'$nin': present}})
    
    # Extract student names from MongoDB cursor
    absent = [student['name'] for student in absent_students]
    
    return absent

