import os


def find_img_path():

    image_directory = "Data\known_faces"
    file_list = os.listdir(image_directory)
    paths = [os.path.join(image_directory, file) for file in file_list]
    names = []
    for path in paths:
        name=path.split('\\')
        names.append(name[-1])
    known_faces = []
    for i in range(len(names)):
        known_faces.append([paths[i], names[i]])
    
    img_paths=[]
    for img_dir in paths:
        if img_dir[-3:] != 'pkl':
            file_list = os.listdir(img_dir)
            img_paths.extend([os.path.join(img_dir, file) for file in file_list if file.lower().endswith('.jpg')])
    return img_paths