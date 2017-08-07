import requests
import re
import http.cookiejar as  cookielib
import time
session =requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print('cookie fail to load')


agent ='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
header = {

    "Host":"www.zhihu.com",
    'User-Agent': agent
}

def get_xsrf():
    #获取xsrf code
    response = session.get("https://www.zhihu.com", headers=header)
    response_text = response.text
    #reDOTAll 匹配全文
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL)
    xsrf = ''
    if match_obj:
        xsrf = (match_obj.group(1))
        return xsrf


def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    print(captcha_url)
    response =requests.get(captcha_url,headers=header)
    with open('capacha_url.gif','wb') as f:
        f.write(response.content)
        f.close()

    from PIL import Image
    try:
        picture= Image.open('capacha_url.gif')
        picture.show()
        picture.close()
    except:
        pass
    captcha = input('输出验证码')
    return captcha








def login_zhihu(account,password):
    if re.match("^1\d{10}",account):
        print('login by mobile phone')
        post_url ='https://www.zhihu.com/login/phone_num'
        post_data = {'_xsrf':get_xsrf(),
                    'phone_num': account,
                    'password': password,
                    'captcha': get_captcha()
                     }
        response =session.post(post_url,data=post_data, headers=header)
        print(response.text)

        session.cookies.save()
    else:
        if '@' in account:
            if re.match("^1\d{10}", account):
                print('login by email')
                post_url = 'https://www.zhihu.com/login/email'
                post_data = {'_xsrf': get_xsrf(),
                             'email': account,
                             'password': password,
                             'captcha_type': 'cn',
                             }
    response = session.post(post_url, data=post_data, headers=header)

    session.cookies.save()

def get_index():
    response = session.get("https://www.zhihu.com",headers=header)
    with open('intex.html','wb') as f:
        f.write(response.text.encode('utf-8'))


    print('ok')

    

def is_login():
    url = "https://www.zhihu.com/settings/profile"
    response=session.get(url,headers=header,allow_redirects=False)
    if response.status_code == 200:
         print('success')
    else:
        print('fail')




login_zhihu('15817302742','pk11215717')


