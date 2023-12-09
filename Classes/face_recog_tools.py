import face_recognition

class face_endcoding_tools:
    def oneface_encoding_onebyone(self,face_locations: list):
        '''얼굴들의 위치가 담긴 리스트를 받아서 각 얼굴들의 encoding을 반환'''
        faces_encodings = []
        for index, face_location in enumerate(face_locations):
            # face_encodeings에 이미지 자체를 넣은 후 이를 꺼내서 encoding을 돌린다음 다시 넣는다.
            faces_encodings.append(face_recognition.load_image_file(face_location))
            faces_encodings_results = face_recognition.face_encodings(faces_encodings[index])
            if not faces_encodings_results:
                '''가끔 얼굴 인코딩을 못하는 경우가 있다. 이 경우에는 faces_encodings_results의 형태가 []이므로 이 경우에는 None을 넣어준다.'''
                faces_encodings[index] = None
            else:
                '''얼굴을 찾은 경우'''
                faces_encodings[index] = faces_encodings_results[0] # [0]인덱스를 넣어준 이유는 얼굴이 하나만 있기 때문이다.
        
        return faces_encodings

    def each_face_endcodings_eachbyone(self, image_path_list: list):
        '''이미지 하나에 있는 얼굴들의 encoding을 반환
        주로 unknown_image를 넣어서 사용 이유는 unknown_image에는 여러 얼굴이 있을 수 있기 때문이다.'''
        result = []
        for image_path in image_path_list:
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            result.append(face_encodings)

        return result
    
    def count_faces_in_image(self,image_path: str): 
        '''이미지에 있는 얼굴들의 수를 반환. 인덱스로 반환하지 않음.'''
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        return len(face_locations)