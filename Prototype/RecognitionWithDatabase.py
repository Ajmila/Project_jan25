from deepface import DeepFace as df
import ConnectDatabase

def recognize(detected_faces):
    client=ConnectDatabase.connect_db()
    mydb=client['Student']
    mycollection=mydb['stud_table']
    
    #find embeddings of detected faces
    target_embeddings=[]
    for i in range(len(detected_faces)):
        target_embedding=df.represent(img_path = detected_faces[i], model_name = "Facenet",enforce_detection=False)[0]["embedding"]
        target_embeddings.append(target_embedding)


    #recognition by comparing with embeddings of known faces
    count=0
    for target_embedding in target_embeddings:
        newquery = mycollection.aggregate( [
    {
        "$addFields": { 
            "target_embedding": target_embedding
        }
    }
    , {"$unwind" : { "path" : "$embedding", "includeArrayIndex": "embedding_index"}}
    , {"$unwind" : { "path" : "$target_embedding", "includeArrayIndex": "target_embedding_index" }}
    , {
        "$project": {
            "img_name": 1,
            "embedding": 1,
            "target_embedding": 1,
            "compare": {
                "$cmp": ['$target_embedding_index', '$embedding_index']
            }
        }
    }
    ,{"$match":{"compare":0}}
    , {
      "$group": {
        "_id": "$img_name",
        "distance": {
                "$sum": {
                    "$pow": [{
                        "$subtract": ['$embedding', '$target_embedding']
                    }, 2]
                }
        }
      }
    }
    , { 
        "$project": {
            "_id": 1
            #, "distance": 1
            , "distance": {"$sqrt": "$distance"}
        }
    }
    , { 
        "$project": {
            "_id": 1
            , "distance": 1
            , "cond": { "$lte": [ "$distance", 10 ] }
        }
    }
    , {"$match": {"cond": True}}
    , { "$sort" : { "distance" : 1 } }
    ] )
        match=list(newquery)
        if len(match)>0:
            print(count," ",match[0]['_id'])
        else:
            print(count," no matches")
        count+=1