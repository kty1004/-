import certifi
import os
from Classes.file_management_tools import File_manager
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote # 한글을 url에 넣기 위해 사용
file_manager = File_manager()

class naver_search:
    def Naver_image_collector(self,id: str, password: str,search_word: str,display: int,start: int):
        '''네이버 검색 Open API 사용 요청 시 얻게 되는 정보를 입력합니다. start는 검색 시작 위치입니다. display는 검색 결과 출력 건수입니다. 최대 100개까지 요청 가능합니다.'''
        encText = quote(search_word) # 한글을 유니코드로 변환
        url = f"https://openapi.naver.com/v1/search/image?query={encText}&display={display}&start={start}"
        print(url)
        client_id =id
        client_secret = password
        headers={
            'X-Naver-Client-Id':client_id,
            'X-Naver-Client-Secret':client_secret
        }
        res = requests.get(url, headers=headers, verify=certifi.where())
        rescode = res.status_code

        img_url_result=[]
        if(rescode==200):
            data=res.json()
            #print(data)
            items=data['items']

            for item in items:
                img_link=item['link'].replace("\\","")
                img_url_result.append(img_link)
        else:
            print("Error Code:" + str(rescode))
            exit()

        def download_image(img_url:str, filename:str, dir_path:str):
            '''이미지를 filename이라는 이름으로 다운로드한다. 다운로드에 성공하면 True를 리턴하고, 실패하면 False를 리턴한다.'''
            file_path = os.path.join(dir_path, filename)
            try:
                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                    return True
                else:
                    return False
            except Exception as e:
                print(f"이미지를 다운로드할 때 에러가 발생함 : {e}")
                return False
        
        success_download_count=0
        for index, img_link in enumerate(img_url_result):
            success = download_image(img_link, f'{search_word}_{index}.jpg','img_source')
            if not success:
                print(f"해당 이미지 링크에서 이미지 다운로드 실패: {img_link}")
            else:
                success_download_count+=1
        print(f'{search_word} 이미지 {success_download_count}개 다운로드 완료')

    def collect_naver_profile(self,search_name):
        '''네이버 프로필을 수집한다. 이 때 search_name이 본명이 아닌 활동명일 경우 프로필을 찾지 못할 수 있다. 찾지 못했을 경우 False를 리턴하고, 찾았을 경우 True를 리턴한다.'''
        # 웹 페이지 URL
        url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={quote(search_name)}"

        # 웹 페이지를 가져옴
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, verify=certifi.where(), headers=headers)
        if response.status_code != 200:
            print('status code:', response.status_code)
            raise Exception('invalid url:', response.url)
        soup=BeautifulSoup(response.text, 'html.parser')
        #profile_a=soup.find('a', data_id='main_profile')

        profile_img = None
        for name_part in search_name.split():
            # 이 코드는 search_name을 공백으로 나누어서 각각의 단어를 name_part로 받는다. 그리고 이 name_part를 포함하는 img 태그를 찾는다.
            profile_img = soup.select_one(f'img._img[alt*="{name_part}"]')
            if profile_img is not None:
                break
        if profile_img is None:
            print(f'{search_name}의 프로필을 찾을 수 없습니다. 본명이 아닌 활동명을 입력해주세요.')
            return False
        else:
            profile_src=profile_img['src']
            # src 다운로드
            profile_response=requests.get(profile_src)
            profile_response_content=profile_response.content
            with open(f'./naver_profile/{search_name}.jpg', 'wb') as f:
                f.write(profile_response_content)

            print(f'{search_name} naver 프로필 저장완료')
            return True

