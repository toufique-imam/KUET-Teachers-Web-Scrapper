import requests
from bs4 import BeautifulSoup, Comment
import json

url_first = 'http://www.kuet.ac.bd/department/'
url_last = '/index.php/welcome/facultymember'


def download_data(url_mid):
    url_main = url_first+url_mid+url_last
    try:
        page = requests.get(url_main)
        f_name = 'teacher'+url_mid+'.html'
        f = open(f_name, 'w+')
        x = str(page.content)
        f.write(x)
        f.close()
        return
    except requests.ConnectionError:
        return
    except requests.ConnectTimeout:
        return


def get_soup(url_mid="CSE"):
    download_data(url_mid)
    f_name = 'teacher'+url_mid+'.html'
    f = open(f_name, 'r', encoding='utf-8')
    soup = BeautifulSoup(f, 'html5lib')
    f.close()
    return soup


dept = ["CE", "URP", "BECM", "ARCH", "MATH", "PHY", "CHEM", "HUM", "EEE", "CSE",
        "ECE", "BME", "MSE", "ME", "IEM", "ESE", "LE", "TE", "Chemical", "Mechat"]

def get_data():
    full_data = {}
    soup_data = []
    for dept_name in (dept):
        print(dept_name)
        soup_data.append(get_soup(dept_name))
    cnt = 0
    for soup in soup_data:
        dept_name = dept[cnt]
        first_class = 'syndicate'
        if(dept_name == "CSE" or dept_name == "CE"):
            first_class = 'facultymember'
        teacher_data = []
        fx = soup.find(class_=first_class)
        all_teacher = fx.findAll(class_='col-sm-6 col-xs-12')
        print("work ", dept_name, " ", first_class, " ", len(all_teacher))

        for teacher in all_teacher:
            image = teacher.find('img')['src']
            weblink = teacher.find('a')['href']
            h6 = teacher.findAll('h6')
            name = h6[0].text.strip()
            designation = h6[1].text.strip()
            phone = h6[2].text.strip()
            mail = h6[3].text.strip()
            teacher_class = {
                "name": name,
                "weblink": weblink,
                "designation": designation,
                "image": image,
                "phone": phone,
                "mail": mail
            }
            teacher_data.append(teacher_class)
            # print(teacher_class)
            # break
        full_data.update({dept_name: teacher_data})
        cnt = cnt+1
    return full_data


def write_data(s="data.json"):
    f = open(s, 'w')
    fd = get_data()
    json.dump(fd, f)
    f.close()


# if __name__ == "__main__":
#     write_data()
