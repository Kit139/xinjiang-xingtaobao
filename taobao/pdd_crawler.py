#-*-encoding:utf-8-*-
import requests,re,execjs,urllib,json,jsonpath,time,random
from copyheaders import headers_raw_to_dict
from pandas.io.json import json_normalize
import pandas as pd

session = requests.session()

def get_params(href,headers_same):
    headers=headers_raw_to_dict(
        b'''
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        Cache-Control: no-cache
        Pragma: no-cache
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36
        '''
    )
    headers = dict(headers,**headers_same)
    s = session.get(url=href, headers=headers)
    if s.status_code==200:
        html = s.text
        # html = html.replace("\\", "")

        list_id = re.findall('{"listID":"(.*?)"', html)[0]
        flip = re.findall(',"flip":"(.*?)",', html)[0]
        data_sums = int(re.findall('"filterTotalNumStr":"(.*?)件商品",',html)[0])
        datas = re.findall('window.rawData=(.*?);\n</script>',html)[0]
        return  list_id, flip, data_sums, datas

def gen_signature(href):
    js = open("./get_anti.js", mode="r").read()
    cxt = execjs.compile(js)
    signature = cxt.call("get_anti_content", href)
    return signature

def get_index(href,page,list_id,flip):
    api_url= "http://m.yangkeduo.com/proxy/api/search?"
    headers = dict(headers_same,**{
        "Referer": href,
        "AccessToken":accesstoken,
        "VerifyAuthToken":verifyauthtoken,
        "Cookie":cookie,
    })
    data = {
        # "pdduid": "4318316460",
        "item_ver": "lzqq",
        "source": "index",
        "search_met": "manual",
        # "track_data": "refer_page_id,10390_1639628868729_uf4kicx9cf",
        "list_id": list_id,
        "sort": "_sales",
        "filter": "",
        "q": key_words,
        "page": page,
        "is_new_query": "1",
        "size": "50",
        "flip": flip,
        "anti_content":gen_signature( href )
    }
    s = session.get(url=api_url+urllib.parse.urlencode(data),headers=headers)
    if s.status_code==200:
        return s.text

def parser1(json_data):
    data = json.loads(json_data)
    data = jsonpath.jsonpath(data,'$..ssrListData.list')[0]
    df = pd.json_normalize(data, max_level=4)
    return df

def parser(json_data):
    data = json.loads(json_data)
    data = jsonpath.jsonpath(data,'$..goods_model')
    df = pd.json_normalize(data, max_level=4)
    return df

def save_datas(datas):
    pass


if __name__=="__main__":
    key_words = "新疆杏"
    accesstoken = 'JZ26EXT5BFX3BWYPGU4PNT2SPWZRY2RAQ5BMBMC7ZWMY6RQXMW4A1134f16'
    verifyauthtoken = 'jffnw7pMdiXCegUDX58qAw88e5b9ece607e1d37'
    cookie = "api_uid=Ckhf2WG4Pa2bIgBSuqFfAg==; webp=1; _nano_fp=XpEqlpTjn0XjnqTJXT_~YsRcUJY1iUtGi_WBRINV; PDDAccessToken=JZ26EXT5BFX3BWYPGU4PNT2SPWZRY2RAQ5BMBMC7ZWMY6RQXMW4A1134f16; pdd_user_id=4235968942927; pdd_user_uin=YHBGB7KFDMZOOZ2IPPHA6GDBLI_GEXDA; pdd_vds=gazsWnfwqGDEBLYaWavEzavNWOfQvIpaYIrafmrEHmcETQcsZQZLHEBQBwpN"
    headers_same = {
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "m.yangkeduo.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57",
        "Cookie": cookie,
    }
    href = "http://m.yangkeduo.com/search_result.html?search_key="+urllib.parse.quote(key_words)+"&source=index&options=3&search_met_track=manual&is_back=&bsch_is_search_mall=&bsch_show_active_page=&sort_type=_sales&price_index=-1"
    list_id, flip, data_sums, datas = get_params(href,headers_same)
    pages = (data_sums-20)/20
    print("共需爬取{}页数据".format(pages))
    parser1(datas).to_csv('1.csv',index=False)
    parser(get_index(href,2,list_id,flip,)).to_csv('20+数据.csv',index=False,)
    for i in range(91,int(pages+1)):
        #139
    # for i in range(3,5):
        ts = random.uniform(10,16)
        time.sleep(ts)
        print('正要爬取第{}页数据，需等待{}s'.format(i,ts))
        df = pd.read_csv('./20+数据.csv')
        df1 = parser(get_index(href,i,list_id,flip,))
        # print(df1.columns.tolist())
        df_concat = pd.concat([df,df1])
        df_concat.to_csv('./20+数据.csv',index=False)

'https://s.taobao.com/search?data-key=s&data-value=220&ajax=true&_ksTS=1639813636268_982&callback=jsonp983&q=%E6%96%B0%E7%96%86%E6%9D%8F&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=176'
'https://s.taobao.com/search?data-key=s&data-value=264&ajax=true&_ksTS=1639813803404_1223&callback=jsonp1224&q=%E6%96%B0%E7%96%86%E6%9D%8F&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=220'
'https://s.taobao.com/search?data-key=s&data-value=308&ajax=true&_ksTS=1639814633342_1484&callback=jsonp1485&q=%E6%96%B0%E7%96%86%E6%9D%8F&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=264'
'https://s.taobao.com/search?data-key=s&data-value=308&ajax=true&_ksTS=1639815124_4481778&callback=jsonp4481779&q=%E6%96%B0%E7%96%86%E6%9D%8F&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=176'
'https://s.taobao.com/search?data-key=s&               ajax=true&_ksTS=1639815627782_0613&callback=jsonp614&q=%E6%96%B0%E7%96%86%E6%9D%8F&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=176'
'https://s.taobao.com/search?data-key=s&               ajax=true&_ksTS=1639815751201_234&callback=jsonp235&q=%E6%96%B0%E7%96%86%E6%9D%8F&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=176'
'https://s.taobao.com/search?data-key=s%2Cps&data-value=0%2C1&ajax=true&_ksTS=1639815830643_763&callback=jsonp764&q=%E6%96%B0%E7%96%86%E6%9D%8F&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=308'     
