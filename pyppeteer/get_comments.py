import logging,re
from os.path import exists
from os import makedirs, path
import json,time,random
import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError
from lxml import etree
import pandas as pd

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://item.taobao.com/item.htm?id=633095559175&ns=1&abbucket=10&on_comment=1'
TIMEOUT = 15
TOTAL_PAGE = 10
RESULTS_DIR = 'results'
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768
path = './comments.csv'

# exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

browser, tab = None, None
HEADLESS = True


async def init():
    global browser, tab
    # browser = await launch(headless=HEADLESS,
    browser = await launch(headless=False,userDataDir='./userdata',
                           args=['--disable-infobars', f'--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}'])
    tab = await browser.newPage()
    await tab.setViewport({'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT})
    await tab.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
    js_text = """
        () =>{ 
            Object.defineProperties(navigator,{ webdriver:{ get: () => false } });
            window.navigator.chrome = { runtime: {},  };
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], });
        }
    """
    await tab.evaluateOnNewDocument(js_text)  # 本页刷新后值不变，自动执行js
    await tab.setUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62"
    )



async def scrape_page(url, selector):
    logging.info('scraping %s', url)
    try:
        await tab.goto(url)
        await tab.waitForSelector(selector, options={
            'timeout': TIMEOUT * 1000
        })
    except TimeoutError:
        logging.error('error occurred while scraping %s', url, exc_info=True)


async def scrape_index():
    url = INDEX_URL
    await scrape_page(url, '.kg-rate-ct-review-item')


async def parse_index():
    return await tab.querySelectorAllEval('.item .name', 'nodes => nodes.map(node => node.href)')


async def scrape_detail(url):
    await scrape_page(url, 'h2')


async def parse_detail():
    url = tab.url
    li_htmls = await tab.querySelectorAllEval('.kg-rate-ct-review-item', 'nodes => nodes.map(node => node.outerHTML)')
    # print(li_htmls)
    return li_htmls

    # name = await tab.querySelectorAllEval('.from-whom div', 'nodes => nodes.map(node => node.innerText)')
    # touxiang = await tab.querySelectorAllEval('div.from-whom img:nth-child(1)', 'nodes => nodes.map(node => node.src)')
    # xingji = await tab.querySelectorAllEval('.from-whom img:last-child', 'nodes => nodes.map(node => node.src)')

    # categories = await tab.querySelectorAllEval('div:first-child div.J_KgRate_ReviewContent.tb-tbcr-content', 'nodes => nodes.map(node => node.innerText)')
    # times = await tab.querySelectorAllEval('.kg-rate-ct-review-item div.review-details div:first-child div.tb-r-act-bar .tb-r-date', 'nodes => nodes.map(node => node.innerText)')
    # classes = await tab.querySelectorAllEval('.kg-rate-ct-review-item div.review-details div:first-child div.tb-r-act-bar .tb-r-info', 'nodes => nodes.map(node => node.innerText)')
    # youyong = await tab.querySelectorAllEval('.J_KgRate_UsefulNum', 'nodes => nodes.map(node => node.innerText)')

    # zuijia = await tab.querySelectorAllEval('.tb-rev-item.tb-rev-item-append .tb-tbcr-content', 'nodes => nodes.map(node => node.innerText)')
    # zuijia_time = await tab.querySelectorAllEval('.tb-rev-item.tb-rev-item-append .tb-r-date', 'nodes => nodes.map(node => node.innerText)')

    # html = await tab.querySelectorAllEval('.kg-rate-ct-review-item', 'nodes => nodes.map(node => node.outerHTML)')
    # return df
async def parse_li(li):
    # for li in li_htmls:
    li_html = etree.HTML(li)
    nam = li_html.xpath('//li/div[1]/div/text()')[0]
    print(nam)
    name=nam
    touxiang=li_html.xpath('//li/div[1]/img[1]/@src')[0]
    xingji=li_html.xpath('//li/div[1]/img[2]/@src')[0]

    categories=li_html.xpath('//li/div[2]/div[1]/div[1]')[0]
    times=li_html.xpath('//span[@class="tb-r-date"]/text()')[0]
    classes=li_html.xpath('//div[@class="tb-r-info"]/text()')[0]
    youyong=li_html.xpath('//span[@class="J_KgRate_UsefulNum tb-tbcr-num"]/text()')[0]

    zuijia = li_html.xpath('//li/div[2]/div[2]/div[1]/text()')[0]
    zuijias=zuijia if zuijia else ''
    zuijia_time = li_html.xpath("//span[@class='tb-r-date']")[1]
    zuijia_times=zuijia_time if zuijia_time else ''
    data_json = {
        'name':nam,'touxiang':touxiang,'xingji':xingji,'categories':categories,'times':times,'classes':classes,'youyong':youyong,'zuijias':zuijias,'zuijia_times':zuijia_times,'li':li
    }

    return data_json
    # df['name']=name
    # df['touxiang']=touxiang
    # df['xingji']=xingji
    # df['categories']=categories
    # df['times']=times
    # df['classes']=classes
    # df['youyong']=youyong
    # df['zuijias']=zuijias
    # df['zuijia_times']=zuijia_times
    # df['li_htmls']=li_htmls


async def save_data(df,datas):
    # name = data.get('times')[0].replace(':','_')
    # data_path = f'{RESULTS_DIR}/{name}.json'
    # json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    df_concat = pd.concat([df,datas])
    df_concat.to_csv(path,index=False)


async def main():
    await init()
    try:
        await tab.goto('https://s.taobao.com/search?q=%E6%96%B0%E7%96%86%E6%9D%8F&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&ntoffset=-282&s=0')
        time.sleep(30) # 登录
        await scrape_index()
        detail_data = await parse_detail()
        df = pd.DataFrame()
        df['li_htmls'] = detail_data
        df.to_csv(path,index=False)
        while 1:
            await tab.click('.pg-next', options={
                'button': 'left',
                'clickCount': 1,  # 1 or 2
                'delay': 300,  # 毫秒
            })
            await tab.waitForSelector('.kg-rate-ct-review-item', options={
            'timeout': TIMEOUT * 1000
            })
            ts = random.uniform(3,8)
            print('睡眠{}s'.format(ts))
            time.sleep(ts)
            detail_data = await parse_detail()
            logging.info('data %s', detail_data)
            dfs = pd.DataFrame()
            dfs['li_htmls'] = detail_data
            df1 = pd.read_csv(path)
            await save_data(df1, dfs)
    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())