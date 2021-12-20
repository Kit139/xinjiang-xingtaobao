import requests, re, time, random, csv, urllib

# cookies = input('请输入cookies:')
# keys = input('请输入查询商品的名称:')
cookies = 'cna=e1PlGQ5BrWwCAd9yveJawLGt; _m_h5_tk=47bf7bde478c09e27d666197fd40d561_1639420573564; _m_h5_tk_enc=bb2e0e0fb3c8ccc2a325d9202096706c; cookie2=1d1c147c52230d2db4db8dc60d4d4122; t=f5cfcafec8d24646fe1dd4fb4d7434f3; _tb_token_=e7e5766e33076; _samesite_flag_=true; xlly_s=1; sgcookie=E100rzx3PgscMDKxpgGLsyeHy8bgNhK9ES5iFIKTlWzMPJTZYufsCoBcexy4ctr9DKflc3+7yRG3coyGIAi7+sohtZ4xfOa1F23by8verXDRLC0=; unb=2201549484267; uc3=lg2=WqG3DMC9VAQiUQ==&id2=UUphy/eB/EyAM6TwuA==&nk2=F5RNbBrtI/oQ3uk=&vt3=F8dCvUr12FyG0cO33sQ=; csg=a0162b7f; lgc=tb892656134; cancelledSubSites=empty; cookie17=UUphy/eB/EyAM6TwuA==; dnk=tb892656134; skt=80f00676c3e3afdf; existShop=MTYzOTQxMTk2Mg==; uc4=nk4=0@FY4Gu65hipufpzK1EUVV+ws8lPBhNg==&id4=0@U2grEJAStzY8CQg8YoUZa+WhczW3D3og; tracknick=tb892656134; _cc_=V32FPkk/hw==; _l_g_=Ug==; sg=47d; _nk_=tb892656134; cookie1=AV10u4O4qhKlirp93II7MDbKctRk/fSlNnwAKLV7cKo=; mt=ci=0_1; thw=cn; uc1=cookie21=U+GCWk/7pY/F&cookie16=VFC/uZ9az08KUQ56dCrZDlbNdA==&cookie15=V32FPkk/w0dUvg==&cookie14=Uoe3fohuiilCaQ==&pas=0&existShop=false; tfstk=cFpRBRXxLq0kFdjvbQhDdGGH7EicZYrR-u_LpmZ-PnDU3MwdiWvMBPKnNM7NymC..; l=eBLV-lCIjdfokQTwBOfZourza779jIRAIuPzaNbMiOCP_N1p5HAVW6Qka689CnGVh6DHR35QT-EXBeYBqC22sWRKIosM_CMmn; isg=BEtLmd1TrqW4J_M1MvIRXWym2u814F9iKTccWL1IFwrh3Go-RbWfsj9ystwyXbda'
keys = '新疆杏'
headers = {
    # 'cache-control': 'no-cache',
    # 'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    # 'pragma': 'no-cache',
    # 'sec-fetch-dest': 'document',
    # 'referer': 'https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20210413&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E5%9D%9A%E6%9E%9C+%E6%96%B0%E7%96%86&suggest=history_1&_input_charset=utf-8&wq=%E5%9D%9A%E6%9E%9C&suggest_query=%E5%9D%9A%E6%9E%9C&source=suggest&sort=sale-desc&bcoffset=18&p4ppushleft=%2C44&s=0&ntoffset=18',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57',
    'cookie': str(cookies),
    # 'cookie': '_m_h5_tk=5e0e5a82316c88955cef8fa2c81d36f6_1618248317667;_m_h5_tk_enc=2855c23bb04fa6152a67aea548051094;cookie2=26cc6833bacbfbc258631d43131b8c47;t=0f8721830c536a03a2cf3f12ae33697f;cna=I2PeGCUxn00CAd9yv1T9gVuk;xlly_s=1;_samesite_flag_=true;sgcookie=E100yzC1pzTSmdcVFmFEVWmg264Z2hjqsbKgXzRzcsiwCGTYdavv5a/1gfpMFVF4ef81miSveTqrm3IIdnmPPiBJxw==;uc3=nk2=F5RNbBrtI/oQ3uk=&id2=UUphy/eB/EyAM6TwuA==&vt3=F8dCuwuR80ZJhEX8fUI=&lg2=WqG3DMC9VAQiUQ==;csg=ebfb5a8e;lgc=tb892656134;dnk=tb892656134;skt=3753168dfb55c522;existShop=MTYxODIzODY0Mg==;uc4=nk4=0@FY4Gu65hipufpzK1EUVXgkDCkM7jgg==&id4=0@U2grEJAStzY8CQg8YoUZa+fTHoAt3/0W;tracknick=tb892656134;_cc_=V32FPkk/hw==;enc=gN10t2SNLjQ7dbgflw438DpxL5nOrFkaCDWrkLeT1ViSrgTLPHMFzDEmtmGn4eodxKlqF7G+PLsjkAVN8PyK4IEJJ0SxOU/L0VrUceMrgTs=;mt=ci=0_1;thw=cn;hng=CN|zh-CN|CNY|156;v=0;uc1=existShop=false&pas=0&cookie14=Uoe1iuKIOP8uWg==&cookie21=Vq8l+KCLjA+l&cookie16=Vq8l+KCLySLZMFWHxqs8fwqnEw==;_tb_token_=5353033b83ef3;tfstk=cVSVBng6GhfWPmK_JntZ1TBVIzpAa66cI0JBoa2wsbN3ZSTyTsAt6LXUGLJsw_Lc.;l=eBTehG1Hj1_znEOtBO5ZRurza77TeIdf1mFzaNbMiIncC6xP1l9Y8wtQDY1LYptRJ8XcTk8B4UxpBT9trFZYWyvjJ0YEae1VivEBCOf..;isg=BPLyLZF1xnhZYPpFsL4yANu0Qz7Ug_Ydopxdw7zKpKGwT5FJpBEOL36tOutzbG61;JSESSIONID=CAD7383B91520FC40EA5349C26DC2C8E',
}

columns = ['标题', '图片链接', '详情页', '价格', '运费', '所在地', '销量', '评论数', '店铺名称', '标识']

def get_data(url, page):
    try:
        res = requests.get(url, headers=headers)
        print('正在爬取第{}页'.format(page))
        if res.status_code == 200:
            return res.text
    except requests.RequestException as e:
        print(e, url)

def parse(html):
    datas = re.findall(re.compile(',"raw_title":"(.*?)","pic_url":"(.*?)","detail_url":"(.*?)","view_price":"(.*?)","view_fee":"(.*?)","item_loc":"(.*?)","view_sales":"(.*?)","comment_count":"(.*?)",.*?,"nick":"(.*?)",.*?,"icon":(.*?),"comment_url":', re.S), html)
    print(datas)
    for data in datas:
        yield [data[0], 'https:' + data[1], 'https:' + data[2], data[3], data[4], data[5].replace(' ', ''), data[6].replace('人收货', ''), data[7], data[8], re.findall(re.compile('"title":"(.*?)",', re.S), data[9])]

def save_datas(datas):
    with open(keys+'淘宝销售.csv', mode='a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(datas)

def main(page):
    q_keys = {
        'q': str(keys)
    }
    q_keys = urllib.parse.urlencode(q_keys)
    url = 'https://s.taobao.com/search?q={}&sort=sale-desc&bcoffset=9&p4ppushleft=%2C44&s={}&ntoffset=-3'.format(q_keys, (page - 1)*44)
    # url = 'https://s.taobao.com/search?q=%E6%A0%B8%E6%A1%83+%E6%96%B0%E7%96%86&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210413&ie=utf8&sort=sale-desc&bcoffset=-3&p4ppushleft=%2C44&s={}&ntoffset=-3'.format((page - 1)*44)
    print(url)
    html = get_data(url, page)
    for i in parse(html):
        save_datas(i)

save_datas(columns)
page = 1
while 1:
    main(page)
    page += 1
    tim = random.uniform(5, 8)
    print('要等待{}s'.format(tim))
    time.sleep(tim)