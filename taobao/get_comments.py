import re
from sys import path
import requests,json,jsonpath
import random
import time
import os
import pandas as pd
from copyheaders import headers_raw_to_dict

session = requests.session()

headers = headers_raw_to_dict(
b'''
content-encoding: gzip
content-language: zh-CN
content-type: text/html;charset=UTF-8
date: Sat, 18 Dec 2021 18:28:17 GMT
eagleeye-traceid: 0b01447016398520978532578ea50f
easytrace_app_name: tms
s_group: tao-session
s_ip: 4547514b636659525a55316e667145684f513d3d
s_read_unit: [CN:CENTER]
s_status: STATUS_NOT_EXISTED
s_tag: 283674001342464|4294967296^1|^^
s_tid: 0b01447016398520978532578ea50f
s_ucode: CN:CENTER
s_v: 4.0.4.6
server: Tengine/Aserver
spm-a
spm-b
strict-transport-security: max-age=31536000
timing-allow-origin: *
vary: Accept-Encoding
authority: rate.tmall.com
method: GET
path: /list_detail_rate.htm?itemId=621668204761&spuId=1730017853&sellerId=4070486739&order=3&currentPage=2&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvPpvpvB6vUvCkvvvvvjiWPsc9ljDER2SwAjthPmPwQjimPLqwgjEHPLLyzj3WRvhvCvvvphmvvpvZ7DA5umcw7Di48Ud5MUrw9liMz1V%2BvpvEvUjPlcvvvntfdvhvmpmC7y2QvvCaQ4QCvvyv9XmEP9vv847%2BvpvEvUjcsIgvvmkXmvhvLU2S1GwaiC4AdByaUE5xnqhTrmYCI8oYRqvtOvc6kbpB5fEep8mxDXgBnAtbk8p7%2Bi7JO3v3DBh7%2B3neLi7%2B53V6%2BA3wk8oaRqvtOCoUvpvVvpCmp%2FLOuvhvmvvvpLQqWqgzKvhv8vvvphvvvvvvvvCmmpvvvcyvvhXVvvmCWvvvByOvvUhwvvCVB9vv9BQvvpvVvUCvpvvv29hvCvvvMMGgvpvhvvCvp8OCvvpvvhHh39hvCvmvphm%2BvpvEvUHXpTvvvR7D&needFold=0&_ksTS=1639852100761_1685&callback=jsonp1686
scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
cookie: lid=tb892656134; cna=e1PlGQ5BrWwCAd9yveJawLGt; hng=CN%7Czh-CN%7CCNY%7C156; sgcookie=E100rzx3PgscMDKxpgGLsyeHy8bgNhK9ES5iFIKTlWzMPJTZYufsCoBcexy4ctr9DKflc3%2B7yRG3coyGIAi7%2BsohtZ4xfOa1F23by8verXDRLC0%3D; uc1=cookie14=Uoe3foTf0JMMWA%3D%3D; uc3=lg2=WqG3DMC9VAQiUQ%3D%3D&id2=UUphy%2FeB%2FEyAM6TwuA%3D%3D&nk2=F5RNbBrtI%2FoQ3uk%3D&vt3=F8dCvUr12FyG0cO33sQ%3D; t=f13a554b0ae0d611311e69d0266564bd; tracknick=tb892656134; uc4=nk4=0%40FY4Gu65hipufpzK1EUVV%2Bws8lPBhNg%3D%3D&id4=0%40U2grEJAStzY8CQg8YoUZa%2BWhczW3D3og; lgc=tb892656134; enc=thNJywEYTb2rtk%2FQJLqLpa3wtoTdru8Ob0334qQ53iT1CeIpPCfEPt1Ixb1oKzgLKAI7rL%2FCHpzmAevdBLk7tvAE7Hy87tTFM%2FBoeOHqcIk%3D; _tb_token_=e60e31e5b6551; cookie2=16e2a5879cf3db46363a0760474351b1; xlly_s=1; x5sec=7b22617365727665723b32223a226231353537653433623433626632343939373739386438343864636661353638434933512b493047454e766b762b376c6837662b4a686f504d6a49774d5455304f5451344e4449324e7a73784d4b3668385930434f674a724d513d3d227d; tfstk=chMcBVgsjjPjqJVoOKwj2TKUxsgGaxR4lAkrUv5CJZnUBM3Q0sXGa6yvw34vRE51.; l=eBQ2ZEDVgOH6r2-hBO5wlurza77tzIdf1tVzaNbMiIncC6LVGyvHQ4-Qcpj5RLtRR8XVt3LB4LIMpB9T7ey35PLfoTB7K9cdvdQ6Qe8C.; isg=BGhoyL8lnbV2obGK4qDIrASxOVZ6kcybB4obtSKYbOGzfQvnyqAZKcf7dRWN74Rz
referer: https://detail.tmall.com/item.htm?spm=a230r.1.14.4.5fdb2d22LxauMY&id=621668204761&ns=1&abbucket=10
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: script
sec-fetch-mode: no-cors
sec-fetch-site: same-site
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57
'''
)



def get_html(header,page):
    t_param = time.time()
    t_list=str(t_param).split(".")
    params={
        'itemId': 621668204761,
        'spuId': 1730017853,
        'sellerId': 4070486739,
        'order': 3,
        'currentPage': page,
        'append': 0,
        'content': 1,   
        "callback":str(int(t_list[1][3:])+1),
        "_ksTS":t_list[0]+t_list[1][:3]+"_"+t_list[1][3:]
    }
    url1 = 'https://rate.tmall.com/list_detail_rate.htm?itemId=621668204761&spuId=1730017853&sellerId=4070486739&order=1&currentPage={}&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvFQvnvPOvU9CkvvvvvjiWPsc96jnCRsLpgjYHPmPv1jEjRs5ytj38R2z9sjDEPL%2FvvpvWz%2FM6PHC4zYMN0vjwdvhvmpvUqpELZQC61L9Cvvpvvvvv29hvCvvvvvvUvpCWhnTFvvwTD7zvaB4AVAYlYU3nRFyiBt0U%2BE7rV169qN7QD40wjomU6flnhBODNKBlYE7r5C60knjEiLwBfvDrtjc6%2BultE8AU5O97%2BI9CvvOUvvVvJZ%2FIvpvUvvmvSIgwtlRgvpvIvvvvvhCvvvvvvvH9phvUAQvvvQCvpvACvvv2vhCv2RvvvvWvphvWgvvCvvOvCvvvphmevpvhvvmv9IOCvvpvCvvvdvhvhovWLv8DipCIToeSI2BvAxZ1RvhvCvvvvvv%3D&needFold=0&_ksTS={}&callback=jsonp{}'.format(page,t_list[0]+t_list[1][:3]+"_"+t_list[1][3:],str(int(t_list[1][3:])+1))
    print(url1)
    # r=requests.get(url1,headers=header,params=params)
    r=session.get(url1,headers=header,params=params)
    if r.status_code==200:
        contents_json = re.findall('(?<=\().*(?=\))',r.text)[0]
        print(contents_json)
        return contents_json
    else:
        print('网络连接异常')

def parser(json_data):
    data = json.loads(json_data)
    data = jsonpath.jsonpath(data,'$..rateList')[0]
    print(data)
    df = pd.json_normalize(data, max_level=4)
    return df

def save_datas(df,datas):
    df_concat = pd.concat([df,datas])
    df_concat.to_csv(path,index=False)

def get_item(num):
    for page in range(1,num):
        try:
            text=get_html(headers,page)
            ts = 2+random.uniform(1,3)
            print("第{}页爬取完毕，等待{}s".format(page,ts))
            time.sleep(ts)
            return text
        except:
            print("未爬取数据")

    
if __name__=='__main__':
    # num=4
    # get_item(num)
    path = './taobao/评论数据2.csv'
    parser(get_html(headers,1)).to_csv(path,index=False)
    page = 2
    while 1:
        ts = random.uniform(5,8)
        time.sleep(ts)
        print('正要爬取第{}页数据，需等待{}s'.format(page,ts))
        df = pd.read_csv(path)
        data = parser(get_html(headers,page))
        save_datas(df,data)
        page+=1
        # if page == 10:
        #     break
