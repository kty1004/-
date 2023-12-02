import os

class File_name_manager:
    def get_file_names_in_folder(self, folder_path: str):
            '''폴더 내의 파일 이름들을 확장자를 포함하여 리스트로 반환 '''
            return os.listdir(folder_path)
        
    def get_file_names_in_folder_without_ext(self,directory:str):
        '''폴더 내의 파일 이름들을 확장자를 제외하여 리스트로 반환'''
        file_names = []
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                name, ext = os.path.splitext(file)
                file_names.append(name)
        return file_names
    
    def rename_file_in_dir(self, directory: str, old_name: str, new_name: str):
        '''디렉토리 내의 특정 이름을 가진 파일을 새로운 이름으로 변경 (확장자 유지)'''
        #print(f'rename_file_in_dir activated !: {old_name} -> {new_name}')
        file_names = self.get_file_names_in_folder(directory)
        for file in file_names:
            name, ext = os.path.splitext(file)
            if os.path.isfile(os.path.join(directory, file)) and name == old_name:
                os.rename(os.path.join(directory, file), os.path.join(directory, new_name + ext))


class File_manager(File_name_manager):
    def dir_check_and_create(self, dir_name: str):
        '''디렉토리가 없으면 생성 있으면 상대 위치를 출력'''
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"'{dir_name}' 디렉토리가 생성되었습니다. 상대 위치는: {os.path.relpath(dir_name)}")
            
    def get_image_file_paths_in_folder(self, folder_path: str):
        '''폴더 내의 이미지 파일 경로들을 리스트로 반환'''
        file_names = self.get_file_names_in_folder(folder_path)
        image_file_paths = []
        for name in file_names:
            if name.endswith(('.png', '.jpg', '.jpeg')):  # 이미지 파일만 처리
                image_file_paths.append(os.path.join(folder_path, name))
        return image_file_paths

    def check_files_in_folder(self,folder_path:str, name_list: list):
        '''폴더 내의 파일들이 name_list에 있는지 확인'''
        file_names = self.get_file_names_in_folder(folder_path)
        for name in name_list: 
            if name not in file_names:
                # name_list에 있는 이름들이 file_names에 없으면 False를 리턴
                return False
        return True
    
    def read_textFile_and_convert_list(self,filename: str):
        with open(filename, 'r') as file:
            lines = file.readlines()
        stripped_lines = [line.strip() for line in lines if line.strip() != '']
        return stripped_lines

    def delete_files_in_folder(self, folder_path: str, target_file_path_list: list):
        '''폴더 내의 파일들을 name_list에 있는 파일만 제거'''
        file_paths = self.get_image_file_paths_in_folder(folder_path)
        for file_path in file_paths:
            if file_path in target_file_path_list:
                os.remove(file_path)
                #print(f"'{file_path}' 파일을 제거했습니다.")
                # vscoode에서는 제거된 게 바로 반영이 안될 수 있음. 그러나 파일 탐색기에서 확인해보면 제거된 것을 확인할 수 있음.
    
    def move_files_to_folder(self, from_folder: str,to_folder: str , target_file_path_list: list):
        '''폴더 내의 파일들을 target_file_path_list에 있는 파일만 이동. from_folder에서 to_folder로 이동'''
        # to_folder,from_folder가 없으면 생성
        self.dir_check_and_create(to_folder)
        self.dir_check_and_create(from_folder)

        # 파일 이동
        file_paths = self.get_image_file_paths_in_folder(from_folder)
        for file_path in file_paths:
            if file_path in target_file_path_list:
                new_path = os.path.join(to_folder, os.path.basename(file_path))
                os.rename(file_path, new_path) # 파일 이동
                #print(f"'{file_path}' 파일을 '{to_folder}' 폴더로 이동했습니다.")
                '''vscoode에서는 제거된 게 바로 반영이 안될 수 있음. 그러나 파일 탐색기에서 확인해보면 제거된 것을 확인할 수 있음.'''

    def get_num_of_same_H_img(self, dir: str ,name_list: list):# -> dict[str, int]:
        '''폴더 내의 파일들 이름에 name_list에 있는지 확인하고 이들의 개수를 센다. get file number of same Human image'''
        file_names=self.get_file_names_in_folder_without_ext(directory=dir)
        file_names_count={name:0 for name in name_list}
        for file_name in file_names:
            name=file_name.split('_')[0]
            if name in file_names_count.keys():
                file_names_count[name]+=1
            else:
                file_names_count[name]=1
        return file_names_count