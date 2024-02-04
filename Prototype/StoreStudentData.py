from deepface import DeepFace as df
import pandas as pd
from deepface.commons import functions
from tqdm import tqdm
import ConnectDatabase
import KnownfacesPath

def store_student_data():
    client=ConnectDatabase.connect_db()

    mydb=client['Student']
    mycollection=mydb['stud_table']
    

    instances = []
    img_paths=KnownfacesPath.find_img_path()
    
    #find embeddings of known_faces
    for i in tqdm(range(0, len(img_paths))):
        facial_img_path = img_paths[i]    
        embedding = df.represent(img_path = facial_img_path, model_name = "Facenet",enforce_detection=False)[0]["embedding"]

        instance = []
        instance.append(facial_img_path)
        instance.append(embedding)
        instances.append(instance)

    dframe = pd.DataFrame(instances, columns = ["img_name", "embedding"])
    
    #insert_query
    for index, instance in tqdm(dframe.iterrows(), total = dframe.shape[0]):
        mydb['stud_table'].insert_one({"img_name": instance["img_name"], "embedding" : instance["embedding"]})
