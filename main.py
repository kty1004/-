from Functions.functions import naver_profile_crawling,manage_and_crawing_image, check_dict_values_goal, img_num_flatten, rename_files_in_dir_ordered
from Classes.file_management_tools import File_manager
import os

# 환경변수에서 client_id와 client_password를 가져온다.
client_id=os.getenv('NAVER_CRAWLER_CLIENT_ID') 
client_password=os.getenv('NAVER_CRAWLER_CLIENT_PASSWORD')
file_manager=File_manager()

def Integration_process_crawling_names(search_name_list: list, start: int, display_info:int):
    real_seach_names=naver_profile_crawling(search_name_list) # real_seach_names는 네이버 프로필을 찾은 사람들의 이름들을 반환한다. 네이버 프로필을 찾지 못한 사람들의 경우 이름이 잘못되었거나, 네이버 프로필이 없는 경우이다. 이들은 제외한 체로 이미지를 크롤링한다.

    manage_and_crawing_image(display_info=display_info, start=start, search_name_list=real_seach_names, client_id=client_id, client_password=client_password)
    return real_seach_names


# img_results에 특정 이름을 포함하는 사진 파일의 개수를 센다.
search_name_list=file_manager.read_textFile_and_convert_list('Celebrity_name.txt')
img_results_dir='img_results'
num_img_want_to_crawl=3
start=1
display_info=15
modified_search_name_list=search_name_list # 이미 목표치(num_img_want_to_crawl)를 달성한 이름들은 modified_search_name_list에서 제거한다.
while True:
    print(f'{start}번째 item부터 {start+display_info-1}번째 item까지를 수집합니다.')
    real_crawling_names=Integration_process_crawling_names(modified_search_name_list,display_info=display_info,start=start)
    img_results__distribution=file_manager.get_num_of_same_H_img(img_results_dir,real_crawling_names)
    modified_search_name_list=real_crawling_names # 실제로 검색하는 이름들을 토대로 다음에 검색할 이름들을 정한다.
    print('img_results폴더 안의 사진 분포 : ',img_results__distribution)
    
    if check_dict_values_goal(img_results__distribution,num_img_want_to_crawl):
        print('이미지 수집이 완료되었습니다.')
        print('img_results 폴더에 있는 사진들의 분포입니다.',img_results__distribution)
        break
    else:
        start=display_info+start
        #img_distribution의 value 중에서 num_img_want_to_crawl보다 큰 value를 가진 key를 찾는다. 그리고 이를 search_name_list에서 제거한다.
        for key,value in img_results__distribution.items():
            if value >= num_img_want_to_crawl and key in modified_search_name_list:
                # 이미 목표치를 달성해서 modified_search_name_list에서 제거된 key는 또 다시 제거하려고 하지 않는다.
                modified_search_name_list.remove(key)
                print(f'{key}는 이미 목표치를 달성했습니다. {key}를 제외한 나머지 사람들의 이미지를 추가로 수집합니다.')
            print('다음 번에 또 크롤링할 사람들 :',modified_search_name_list)

# img 개수 flatten
print('\n','img_results 폴더 안의 사진 수를 균일하게 맞추겠습니다.')
img_num_flatten(img_results_dir, num_img_want_to_crawl, search_name_list)
img_distribution_after_flatten=file_manager.get_num_of_same_H_img(img_results_dir,real_crawling_names)
rename_files_in_dir_ordered(img_results_dir,search_name_list)
print('img_results 폴더 정리 후 사진 분포입니다.',img_distribution_after_flatten)