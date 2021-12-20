import asyncio,time
from pyppeteer import launch
from pyquery import PyQuery as pq
 
async def main():
   browser = await launch(headless=False)
   page = await browser.newPage()
   await page.goto('http://news.baidu.com/')
   await page.waitForSelector('.hdline0 a')
   await page.click('.hdline0 a', options={
       'button': 'left',
       'clickCount': 1,  # 1 or 2
       'delay': 300,  # 毫秒
   })
   time.sleep(6)
   await browser.close()
 
asyncio.get_event_loop().run_until_complete(main())