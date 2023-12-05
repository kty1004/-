from math import e
from Classes.file_management_tools import File_manager, File_name_manager
from Classes.face_recog_tools import face_endcoding_tools
from Classes.Search import naver_search
import face_recognition
face_endcoding_tools = face_endcoding_tools()
naver_search = naver_search()
file_manager = File_manager()
file_name_manager = File_name_manager()
import random

def naver_profile_crawling(name_list:list, img_num:int = 15):
    '''naver_profile 폴더에 네이버 프로필을 수집한다. 이후 본격적으로 네이버에서 프로필 주인 사진을 찾기 위해 필요한 사람들의 이름을 반환한다.'''
    ## dir check and create
    profile_folder_dir='naver_profile'
    file_manager.dir_check_and_create(profile_folder_dir)

    ## naver profile crawling
    file_name_in_dir=file_name_manager.get_file_names_in_folder_without_ext(profile_folder_dir)
    search_name_list = [item for item in name_list if item not in file_name_in_dir] # name_list는 찾으라고 준 명단이고, search_name_list는 이미 네이버 프로필을 찾은 사람들을 제외한 사람들의 명단이다. 즉, 실제로 찾아야 할 사람들의 명단이다.
    print('이미 네이버 프로필을 찾은 사람들 :',file_name_in_dir)
    print('네이버 프로필을 찾을 사람들 :',search_name_list, '\n')

    if not search_name_list:
        print('네이버 프로필을 이미 다 확보했습니다.')
        return name_list
    else:
        search_status_list=[]
        for search_name in search_name_list:
            is_search_successful=naver_search.collect_naver_profile(search_name)
            search_status_list.append(is_search_successful)
        check_for_seccess=file_manager.check_files_in_folder(profile_folder_dir,search_name_list) # 폴더 내에 search_name_list 에 있는 사람들 프로필이 있는지 확인
        
        if check_for_seccess:
            print('성공적으로 네이버 프로필을 찾았습니다.')
            print('찾은 사람들 :',search_name_list)
            # 이 때는 search_name_list == name_list이다.
            return name_list
        else:
            fail_search_name_list=[]
            for index,search_status in enumerate(search_status_list):
                if search_status == False:
                    fail_search_name_list.append(search_name_list[index])
            print('찾지 못한 사람들 :',fail_search_name_list)
            return list(set(name_list)-set(fail_search_name_list)) # 찾지 못한 사람들을 제외한 사람들의 이름을 반환
        
def rename_files_in_dir_ordered(img_results_dir: str, search_name_list: list):
    # renaming files in img_results_dir
    results_file_names=file_name_manager.get_file_names_in_folder_without_ext(img_results_dir) # img_results_dir에 있는 파일들의 이름들을 리스트로 반환
    results_file_path=file_name_manager.get_file_names_in_folder(img_results_dir) # img_results_dir에 있는 파일들의 경로들을 리스트로 반환
    for search_name in search_name_list: # search_name_list에 있는 이름들을 하나씩 꺼내서 results_file_names에 있는 파일 이름들 중에 search_name이 있는 파일들을 찾아서 리스트로 묶는다.
        same_person_files_names=[]
        for results_file_name in results_file_names:
            if search_name in results_file_name:
                same_person_files_names.append(results_file_name)
        
        # 중복된 파일 이름이 있을 수 있음으로 기존의 이름에다가 인덱스를 붙여서 새로운 이름(dummy_name)을 만든다. 그러면 이름_숫자_숫자 형태로 이름이 만들어진다. 이후에 다시 이름을 바꿔서 이름_숫자 형태로 만든다.
        dummy_name_list=[]
        for same_person_file_name_index,same_person_file_name in enumerate(same_person_files_names):
            dummy_name=f'{same_person_file_name}_{same_person_file_name_index}'
            file_name_manager.rename_file_in_dir(img_results_dir,same_person_file_name,dummy_name)
            dummy_name_list.append(dummy_name)

        for dummy_name_index,dummy_name in enumerate(dummy_name_list):
            file_name_manager.rename_file_in_dir(img_results_dir,dummy_name,f'{search_name}_{dummy_name_index}')


def manage_and_crawing_image(search_name_list,client_id: str,client_password: str, display_info: int, start: int):
    '''img_source 폴더에 이미지를 수집한다. 이 때 search_name_list에 있는 사람들의 이름을 찾아서 이미지를 수집한다. 이후 img_source 폴더에 있는 이미지들 중에서 찾고자 하는 사람의 사진만 골라서 img_results 폴더로 옮긴다.'''
    #print('img_source 폴더에 다음 인물의 이미지를 수집합니다.',search_name_list,'\n')

    # naver image crawling based on naver profile name.
    ## dir check and create
    img_source_folder_dir='img_source' # 네이버에서 크롤링한 이미지들을 저장할 폴더
    file_manager.dir_check_and_create(img_source_folder_dir)
    
    for search_name in search_name_list:
        naver_search.Naver_image_collector(id=client_id,password=client_password,search_word= search_name, display=display_info,start=start)


    #find dir
    ## known faces dir
    profile_folder_dir='naver_profile'
    profile_dirs=file_manager.get_image_file_paths_in_folder(profile_folder_dir)

    ## unknown faces dir
    img_source_folder_dir='img_source'
    file_manager.dir_check_and_create(img_source_folder_dir)
    img_source_dirs=file_manager.get_image_file_paths_in_folder(img_source_folder_dir)


    # face encoding
    ## known faces encoding
    known_faces_encodings=face_endcoding_tools.oneface_encoding_onebyone(profile_dirs)

    ## unknown faces encoding
    unknown_faces_encodings=face_endcoding_tools.each_face_endcodings_eachbyone(img_source_dirs)
    '''unknown_faces_encodings의 형태
    리스트 안에 리스트가 들어있는 형태이다. 이유는 unknown_image에는 여러 얼굴이 있을 수 있기 때문인데 이 unknown_image가 여러개 있기 때문이다.
    '''


    # compare faces
    print('img_source 중에서 필요한 사진과 필요없는 사진을 골라냄.','\n')
    treasure_of_source=[] # img_source_dirs 중에서 아는 사람이 있는 사진들의 경로를 저장할 리스트
    trash_of_source=[] # img_source_dirs 중에서 아는 사람이 없는 사진들의 경로를 저장할 리스트

    known_faces_index=0
    for index,unknown_faces_image in enumerate(unknown_faces_encodings):
        '''어차피 img_source_dirs와 unknown_faces_encodings의 인덱스는 같으므로 index를 사용한다.'''

        face_count=face_endcoding_tools.count_faces_in_image(img_source_dirs[index]) # unknown_faces_image[0]은 unknown_faces_encodings의 인덱스를 의미한다.
        if face_count>1:
            trash_of_source.append(img_source_dirs[index])
        else:
            if not unknown_faces_image:
                '''가끔 unknown_faces_image에 얼굴이 없는 경우가 있다. 이 경우에는 unknown_faces_image[0]의 형태가 []이므로 이 경우를 제외하고 진행한다.'''
                continue
            unknown_face=unknown_faces_image[0] # 사진에 사람이 한 명만 있으면 unknown_faces_image의 형태는 [face_encoding]이므로 [face_encoding]을 face_encoding으로 바꿔준다.
            result = face_recognition.compare_faces(known_faces_encodings, unknown_face) # 알려진 얼굴 인코딩 리스트가 3개의 요소를 가지고 있고, 알 수 없는 얼굴 인코딩이 첫 번째와 세 번째 알려진 얼굴과 일치한다면, 반환값은 [True, False, True]가 된다.
            if result[known_faces_index] ==False: # 현재 찾고자 하는 사람이 사진에 존재하지 않을 경우 trash_of_source에 저장한다.
                #print("- img_source에서 건진 파일의 경로: {}".format(img_source_dirs[index]))
                trash_of_source.append(img_source_dirs[index])
            else:
                #print("- img_source에서 건진 파일의 경로: {}".format(img_source_dirs[index]))
                treasure_of_source.append(img_source_dirs[index])

    #print('\n','treasure_of_source :',treasure_of_source)
    #print('trash_of_source :',trash_of_source, '\n')


    # file management
    ## delete useless files
    file_manager.delete_files_in_folder(img_source_folder_dir,trash_of_source)

    ## move useful files(move to img_results folder)
    img_results_dir='img_results'
    file_manager.move_files_to_folder(img_source_folder_dir,img_results_dir,treasure_of_source)

    # renaming files in img_results
    rename_files_in_dir_ordered(img_results_dir, search_name_list)


def check_dict_values_goal(dictionary, goal):
    '''dictionary의 value가 모두 goal(parameter)이상인지 확인'''
    for value in dictionary.values():
        if value < goal:
            return False
    return True

# 특정 문자를 포함하는 문자열을 찾는 함수
def find_strings_with_char(list, char):
    return [string for string in list if char in string]


def img_num_flatten(dir: str, flatten_num: int, name_list: list):
    ''' flatten_target인 사람의 원래 사진 분포에서 num을 가지고 와서 그 수의 범위에서 랜덤으로 num-random수를 뽑는다. 그리고 그 수에 해당하는 사진을 제거한다.'''
    img_results_distribution=file_manager.get_num_of_same_H_img(dir,name_list)
    files_path=file_manager.get_image_file_paths_in_folder(dir)
    flatten_target_person_dict={}
    for key,value in img_results_distribution.items():
        if value > flatten_num:
            flatten_target_person_dict[key]=value
    
    # 랜덤으로 제거할 파일 경로 리스트를 만들기 위해서 파일 경로에 포함된 인덱스를 사용할 것이다.
    for key,value in flatten_target_person_dict.items():
        delete_img_index_list=[]
        for index in range(value-1-flatten_num-1):
            '''value랑 마찬가지로 flatten_num은 인덱스가 아니라 개수이므로, value-1-flatten_num-1을 해줘야 한다.'''
            while True:
                '''random.randint(a,b)는 a와 b를 포함한 a~b 사이의 정수를 랜덤으로 반환한다. while문을 사용한 이유은 중복되는 delete_img_index_list에 index를 제거하기 위해서이다.'''
                random_index=random.randint(0,value-1)
                if random_index not in delete_img_index_list:
                    delete_img_index_list.append(random_index)
                    break
        print('delete_img_index_list :',delete_img_index_list, 'len(delete_img_index_list) :',len(delete_img_index_list))
        having_key_files_path_list=find_strings_with_char(files_path,key)

        # 제거할 파일 경로 리스트
        delete_imgs_path=[]
        for delete_img_index in delete_img_index_list:
            '''delete_img_index_list에 있는 index에 해당하는 파일 경로를 delete_imgs_path에 추가'''
            delete_imgs_path.append(having_key_files_path_list[delete_img_index])

        # 파일 제거
        file_manager.delete_files_in_folder(dir,delete_imgs_path)
