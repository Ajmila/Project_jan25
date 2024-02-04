from retinaface import RetinaFace as rf
import cv2

def detect_faces(frames):
  
    detected_faces = []

    for frame in frames[:3]:
        obj = rf.detect_faces(frame)
        if isinstance(obj, dict):
            for key in obj.keys():
                faceid = obj[key]
                area = faceid['facial_area']
                x1,y1,x2,y2=area
                extracted_face=frame[y1:y2,x1:x2]
                extracted_face=cv2.cvtColor(extracted_face,cv2.COLOR_BGR2RGB)
                detected_faces.append(extracted_face)
    return detected_faces


def reduce_count(detected_faces):
    faces = []
    faces.append(cv2.convertScaleAbs(detected_faces[0]))
    orb = cv2.ORB_create()
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    for i in range(1, len(detected_faces)):
        img2 = cv2.convertScaleAbs(detected_faces[i])
        keypoints1, descriptors1 = orb.detectAndCompute(faces[-1], None)
        keypoints2, descriptors2 = orb.detectAndCompute(img2, None)
        if descriptors2 is None:
            continue
        matches = bf.match(descriptors1, descriptors2)

        
        if len(matches) < 200:
            faces.append(detected_faces[i])

    detected_faces[:]=faces[:]
    return detected_faces

   


