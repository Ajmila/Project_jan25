from deepface import DeepFace as df

def recognize(detected_faces):
    models=[]
    res=[]

    for i in range(len(detected_faces)):
        model=df.find(img_path=detected_faces[i],db_path='Data/known_faces',model_name="Facenet",distance_metric="euclidean",enforce_detection=False,normalization="Facenet")
        models.append(model)



    count = 0
    for model in models:
        if len(model[0]) > 0:
            print(count , "_ ", model[0]['identity'].values[0])
        else:
            print('Unknown Face detected')
        count += 1