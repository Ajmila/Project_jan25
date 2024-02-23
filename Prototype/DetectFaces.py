import mediapipe as mp
import cv2

def detect_faces(frames):
  
    detected_faces = []
    img=frames[0]
    mp_face_detction = mp.solutions.face_detection
    for frame in frames:
        with mp_face_detction.FaceDetection(model_selection = 1, min_detection_confidence = 0.5) as face_detection:
            results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            for detection in results.detections:
                box = detection.location_data.relative_bounding_box
                x_start, y_start = int(box.xmin * img.shape[1]), int(box.ymin * img.shape[0])
                x_end, y_end = int((box.xmin + box.width) * img.shape[1]), int((box.ymin + box.height) * img.shape[0])

                if x_start < 0 or y_start < 0:
                    continue

            face = frame[y_start:y_end, x_start:x_end]
            face = cv2.cvtColor(face,cv2.COLOR_BGR2RGB)
            detected_faces.append(face)
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

   


