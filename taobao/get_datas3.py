#-*-encoding:utf-8-*-
import requests,re,execjs,urllib,json,jsonpath,time,random
from copyheaders import headers_raw_to_dict
from pandas.io.json import json_normalize
import pandas as pd
import time

session = requests.session()

def get_datas(href,headers_same):
    headers=headers_raw_to_dict(
        b'''
        authority: s.taobao.com
        method: GET
        path: /search?data-key=s&data-value=44&ajax=true&_ksTS=1639844292740_1169&callback=jsonp1170&q=%E6%96%B0%E7%96%86%E6%9D%8F&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&ntoffset=-282&s=0
        scheme: https
        accept: */*
        accept-encoding: gzip, deflate, br
        accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
        cookie: cna=e1PlGQ5BrWwCAd9yveJawLGt; sgcookie=E100rzx3PgscMDKxpgGLsyeHy8bgNhK9ES5iFIKTlWzMPJTZYufsCoBcexy4ctr9DKflc3%2B7yRG3coyGIAi7%2BsohtZ4xfOa1F23by8verXDRLC0%3D; uc3=lg2=WqG3DMC9VAQiUQ%3D%3D&id2=UUphy%2FeB%2FEyAM6TwuA%3D%3D&nk2=F5RNbBrtI%2FoQ3uk%3D&vt3=F8dCvUr12FyG0cO33sQ%3D; lgc=tb892656134; uc4=nk4=0%40FY4Gu65hipufpzK1EUVV%2Bws8lPBhNg%3D%3D&id4=0%40U2grEJAStzY8CQg8YoUZa%2BWhczW3D3og; tracknick=tb892656134; _cc_=V32FPkk%2Fhw%3D%3D; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; mt=ci=-1_0; enc=thNJywEYTb2rtk%2FQJLqLpa3wtoTdru8Ob0334qQ53iT1CeIpPCfEPt1Ixb1oKzgLKAI7rL%2FCHpzmAevdBLk7tvAE7Hy87tTFM%2FBoeOHqcIk%3D; _m_h5_tk=fd3ff9562f9b7a02b71e5ea66199d43d_1639483902519; _m_h5_tk_enc=a878bdaddb36670dc03c2fb767815e21; cookie2=16e2a5879cf3db46363a0760474351b1; t=f13a554b0ae0d611311e69d0266564bd; xlly_s=1; _samesite_flag_=true; JSESSIONID=1F3AABF7D3A113E78BE1F7F5B7686191; v=0; _tb_token_=ee3d67755ee85; uc1=cookie14=Uoe3foTesptkZw%3D%3D; tfstk=cVlPB7OmxQdPH_PBB7NeF5HfQnCRCIE3fszaEY8GsYwewh-8D450oMU0DCU48ZS3E; l=eBLV-lCIjdfokO-vBO5w-urza77tyBdfGtVzaNbMiIncC6nF6v9LYd-Qcpf-RpKRR8XVGZ8p4LIMpB9tPe308yDjJ0YEae1VivQ2deTC.; isg=BA0NXvMnUFIyCvUzIMi_Mz5cHCmH6kG8YmEeOk-V8aZQRin4FjqbjY6QsNogpFl0
        referer: https://s.taobao.com/search?q=%E6%96%B0%E7%96%86%E6%9D%8F&sort=sale-desc&bcoffset=12&p4ppushleft=%2C44&ntoffset=12&s=0
        sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"
        sec-ch-ua-mobile: ?0
        sec-ch-ua-platform: "Windows"
        sec-fetch-dest: script
        sec-fetch-mode: no-cors
        sec-fetch-site: same-origin
        user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57
        '''
    )
    # headers = dict(headers,**headers_same)
    s = session.get(url=href, headers=headers)
    if s.status_code==200:
        html = s.text
        print(html)
        # datas = re.findall('g_page_config = (.*?);\n    g_srp_loadCss',html)[0]
        return  html

def parser(json_data):
    data = json.loads(json_data)
    data = jsonpath.jsonpath(data,'$..auctions')[0]
    df = pd.json_normalize(data, max_level=4)
    return df


def save_datas(df,datas):
    df_concat = pd.concat([df,datas])
    df_concat.to_csv('./taobao/1数据.csv',index=False)


if __name__=="__main__":
    key_words = "新疆杏"
    cookie = "cna=e1PlGQ5BrWwCAd9yveJawLGt; sgcookie=E100rzx3PgscMDKxpgGLsyeHy8bgNhK9ES5iFIKTlWzMPJTZYufsCoBcexy4ctr9DKflc3%2B7yRG3coyGIAi7%2BsohtZ4xfOa1F23by8verXDRLC0%3D; uc3=lg2=WqG3DMC9VAQiUQ%3D%3D&id2=UUphy%2FeB%2FEyAM6TwuA%3D%3D&nk2=F5RNbBrtI%2FoQ3uk%3D&vt3=F8dCvUr12FyG0cO33sQ%3D; lgc=tb892656134; uc4=nk4=0%40FY4Gu65hipufpzK1EUVV%2Bws8lPBhNg%3D%3D&id4=0%40U2grEJAStzY8CQg8YoUZa%2BWhczW3D3og; tracknick=tb892656134; _cc_=V32FPkk%2Fhw%3D%3D; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; mt=ci=-1_0; enc=thNJywEYTb2rtk%2FQJLqLpa3wtoTdru8Ob0334qQ53iT1CeIpPCfEPt1Ixb1oKzgLKAI7rL%2FCHpzmAevdBLk7tvAE7Hy87tTFM%2FBoeOHqcIk%3D; _m_h5_tk=fd3ff9562f9b7a02b71e5ea66199d43d_1639483902519; _m_h5_tk_enc=a878bdaddb36670dc03c2fb767815e21; cookie2=16e2a5879cf3db46363a0760474351b1; t=f13a554b0ae0d611311e69d0266564bd; _tb_token_=e60e31e5b6551; xlly_s=1; uc1=cookie14=Uoe3foTcUJ0gBw%3D%3D; JSESSIONID=7056F2F40B11129EECC26991BB0C6E93; tfstk=cKSVBNZlsoE43qt_JntalHnFQq0AaCdMO0JeoZy3L09xHyIyTs2o6LA8vLJZUfYc.; l=eBLV-lCIjdfok3bbBO5wourza77O4QRf1tVzaNbMiIncC6UCs7vGGJ-QcpHjTpxRR8XVTeYB4LIMpB9tWeE88yD6nSFpne1Vivh6CeYC.; isg=BD4-Q2JK01RYRAY-hz3cFhFRj1SAfwL5PTwNd-hFdQGVi91lUA-VCOYhA1dHkfoR"
    t_param = time.time()
    t_list=str(t_param).split(".")
    headers_same = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57",
        "cookie": cookie,
    }
    href = "https://s.taobao.com/search?data-key=s&data-value=44&ajax=true&_ksTS=1639844292740_1169&callback={}&q=".format(t_list[0]+t_list[1][:3]+"_"+t_list[1][3:],str(int(t_list[1][3:])+1))+urllib.parse.quote(key_words)+"&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&ntoffset=-282&s="
    get_datas(href+'0',headers_same)
    # page = 2
    # while 1:
    #     ts = random.uniform(5,8)
    #     time.sleep(ts)
    #     print('正要爬取第{}页数据，需等待{}s'.format(page,ts))
    #     df = pd.read_csv('./taobao/1++数据.csv')
    #     data = parser(get_datas(href+str((page - 1)*44),headers_same))
    #     save_datas(df,data)
    #     page+=1
