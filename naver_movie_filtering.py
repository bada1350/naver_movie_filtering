import requests
from bs4 import BeautifulSoup
import webbrowser
import pprint

'''
WARNING:
이 프로그램은 VS Code Live Server Extension 실행 중 구동이 가능합니다.
'''

url = "https://movie.naver.com/movie/running/current.naver?view=list&tab=normal&order=point" # 네이버 영화 - 현재 상영영화 평점순 정렬
service_url = "http://127.0.0.1:5500/filtering_results.html"
res = requests.get(url)
if res.status_code == 200:
    html = res.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    # html 파일을 생성한다. 파일이 존재하면 덮어쓰기를 진행한다.
    file = open("filtering_results.html", "wt", encoding='utf-8')
    # html head + body 시작부분
    file.write("<!DOCTYPE html>\n<html lang='en'>\n<head>\n\t<meta charset='UTF-8'>\n\t<meta http-equiv='X-UA-Compatible' content='IE=edge'>\n\t\
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n\t<title>Filtering results</title>\n\n\t\
        <!-- Latest compiled and minified CSS -->\n\t<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'>\n\t\
        <!-- jQuery library -->\n\t<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script>\n\t\
        <!-- Popper JS -->\n\t<script src='https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js'></script>\n\t\
        <!-- Latest compiled JavaScript -->\n\t<script src='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js'></script>\n</head>\n<body>\n")
    file.write("\t<div class='row row-cols-1 row-cols-md-3 mx-5'>\n")
    
    user_rating = float(input('최소 평점 설정(1~10): '))    # 사용자 입력 1: 최소 평점
    user_participants = int(input('최소 참여자 수 설정: '))  # 사용자 입력 2: 최소 참여자 수
    
    movies = []
    movie_info = soup.select(".lst_detail_t1 > li")
    for idx in range(len(movie_info)):
        # 영화 평점
        num = float(movie_info[idx].select_one("span.num").string)
        # 네티즌 평점 참여자
        num2 = int(movie_info[idx].select_one("span.num2 > em").string.replace(",", ""))
        
        # 평점과 네티즌 평점 참여자 수가 사용자가 입력한 조건보다 크거나 같은 경우에만 영화 정보 수집
        if num >= user_rating and num2 >= user_participants:
            
            # 영화 제목
            title = movie_info[idx].img["alt"]
            
            # 영화 이미지
            img_src = movie_info[idx].img["src"]
            
            # 영화 평점
            num = movie_info[idx].select_one("span.num").string
            
            # 네티즌 평점 참여자
            num2 = movie_info[idx].select_one("span.num2 > em").string
            
            info = {
                "title": title,
                "img_src": img_src,
                "rating": num,
                "participants": num2
            }
            movies.append(info)
            
            file.write("\t\t<div class='col mb-4'>\n\t\t\t<div class='card h-100'>\n\t\t\t\t\
                <img style='width: auto;' src='{}' class='card-img-top' alt='...'>\n\t\t\t\t\
                <div class='card-body'>\n\t\t\t\t\t<h5 class='card-title'>{}</h5>\n\t\t\t\t\t\
                <h5 class='card-title'>평점: {}</h5>\n\t\t\t\t\t<h5 class='card-title'>\
                참여자 수: {}</h5>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n".format(img_src, title, num, num2))
    
    file.write("\t</div>\n")
    # html body 끝 부분
    file.write("</body>\n</html>")
    # 파일쓰기 종료
    file.close()

    # 생성한 html 파일을 새로운 탭으로 열기(단, VS code Live Server Extension 실행 중에만 가능)
    webbrowser.open_new_tab(service_url)
else:
    pass

pprint.pprint(movies)