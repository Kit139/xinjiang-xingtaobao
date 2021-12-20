#-*-encoding:utf-8-*-
import requests,re,execjs,urllib,json,jsonpath,time,random
from copyheaders import headers_raw_to_dict
from pandas.io.json import json_normalize
import pandas as pd

session = requests.session()

def get_datas(href,headers_same):
    headers=headers_raw_to_dict(
        b'''
        content-encoding: gzip
        content-language: zh-CN
        content-type: text/html;charset=UTF-8
        date: Sat, 18 Dec 2021 08:34:04 GMT
        eagleeye-traceid: 2128019c16398164439313534ef3a2
        server: Tengine/Aserver
        set-cookie: JSESSIONID=943BDA8F467CE498B55428A3B98CD33F; Path=/; HttpOnly
        strict-transport-security: max-age=31536000
        timing-allow-origin: *
        vary: Accept-Encoding
        authority: s.taobao.com
        method: GET
        path: /search?q=%E6%96%B0%E7%96%86%E6%9D%8F&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=0
        scheme: https
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        accept-encoding: gzip, deflate, br
        accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
        sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"
        sec-ch-ua-mobile: ?0
        sec-ch-ua-platform: "Windows"
        sec-fetch-dest: document
        sec-fetch-mode: navigate
        sec-fetch-site: none
        sec-fetch-user: ?1
        upgrade-insecure-requests: 1
        '''
    )
    headers = dict(headers,**headers_same)
    s = session.get(url=href, headers=headers)
    if s.status_code==200:
        html = s.text
        datas = re.findall('g_page_config = (.*?);\n    g_srp_loadCss',html)[0]
        return  datas

def parser(json_data):
    data = json.loads(json_data)
    data = jsonpath.jsonpath(data,'$..auctions')[0]
    df = pd.json_normalize(data, max_level=4)
    return df


def save_datas(df,datas):
    df_concat = pd.concat([df,datas])
    df_concat.to_csv('./taobao/1++数据.csv',index=False)


if __name__=="__main__":
    key_words = "新疆杏"
    cookie = "cna=e1PlGQ5BrWwCAd9yveJawLGt; sgcookie=E100rzx3PgscMDKxpgGLsyeHy8bgNhK9ES5iFIKTlWzMPJTZYufsCoBcexy4ctr9DKflc3%2B7yRG3coyGIAi7%2BsohtZ4xfOa1F23by8verXDRLC0%3D; uc3=lg2=WqG3DMC9VAQiUQ%3D%3D&id2=UUphy%2FeB%2FEyAM6TwuA%3D%3D&nk2=F5RNbBrtI%2FoQ3uk%3D&vt3=F8dCvUr12FyG0cO33sQ%3D; lgc=tb892656134; uc4=nk4=0%40FY4Gu65hipufpzK1EUVV%2Bws8lPBhNg%3D%3D&id4=0%40U2grEJAStzY8CQg8YoUZa%2BWhczW3D3og; tracknick=tb892656134; _cc_=V32FPkk%2Fhw%3D%3D; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; mt=ci=-1_0; enc=thNJywEYTb2rtk%2FQJLqLpa3wtoTdru8Ob0334qQ53iT1CeIpPCfEPt1Ixb1oKzgLKAI7rL%2FCHpzmAevdBLk7tvAE7Hy87tTFM%2FBoeOHqcIk%3D; _m_h5_tk=fd3ff9562f9b7a02b71e5ea66199d43d_1639483902519; _m_h5_tk_enc=a878bdaddb36670dc03c2fb767815e21; cookie2=16e2a5879cf3db46363a0760474351b1; t=f13a554b0ae0d611311e69d0266564bd; _tb_token_=e60e31e5b6551; xlly_s=1; uc1=cookie14=Uoe3foTcUJ0gBw%3D%3D; JSESSIONID=7056F2F40B11129EECC26991BB0C6E93; tfstk=cKSVBNZlsoE43qt_JntalHnFQq0AaCdMO0JeoZy3L09xHyIyTs2o6LA8vLJZUfYc.; l=eBLV-lCIjdfok3bbBO5wourza77O4QRf1tVzaNbMiIncC6UCs7vGGJ-QcpHjTpxRR8XVTeYB4LIMpB9tWeE88yD6nSFpne1Vivh6CeYC.; isg=BD4-Q2JK01RYRAY-hz3cFhFRj1SAfwL5PTwNd-hFdQGVi91lUA-VCOYhA1dHkfoR"
    headers_same = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57",
        "cookie": cookie,
    }
    href = "https://s.taobao.com/search?q="+urllib.parse.quote(key_words)+"&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s="
    parser(get_datas(href+'0',headers_same)).to_csv('./taobao/1++数据.csv',index=False)
    page = 2
    while 1:
        ts = random.uniform(5,8)
        time.sleep(ts)
        print('正要爬取第{}页数据，需等待{}s'.format(page,ts))
        df = pd.read_csv('./taobao/1++数据.csv')
        data = parser(get_datas(href+str((page - 1)*44),headers_same))
        save_datas(df,data)
        page+=1
