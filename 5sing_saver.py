from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, re, wget

def is_nextpage():
    flag = True
    try:
        driver.find_element_by_link_text('下一页')
        return flag
    except:
        flag = False
        return flag


def findsong(list_name=0):
    strong =driver.find_elements_by_tag_name('strong')
    for i in strong:
        link = i.find_element_by_tag_name('a').get_attribute('href')
        if list_name == 0:
            orglist.append(link)
        else:
            coverlist.append(link)


def savesong(url, path='save'):
    songtitle=' '
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        songtitle = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'h1'))).text
        # print(songtitle)
        songtitle = re.sub(r'[\\/:*?"<>|]', '', songtitle)
    except Exception:
        print('Failed to analyze songs title,URL:' + url)

    if not songtitle==' ':
        try:
            songlink = driver.find_element_by_tag_name('audio').get_attribute('src')
            # print(songlink)
            filename = wget.download(songlink, path + '/' + songtitle + '.mp3')
            print('Saved song ', filename)
        except Exception:
            print('Failed to save songs' + songtitle)
    else:
        pass

def makefolder(path):
    path = re.sub(r'[\\/:*?"<>|]', '', path)
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print('Created folder ' + path + ' successfully')
        else:
            print('Folder existed')
    except Exception:
        print('Creating Folder Failed')
        driver.quit()
        exit()


if __name__ == '__main__':

    print('sing saver')
    print('Author  :  Nakateru (2020.03.05)')
    url = input('Input 5sing URL:')

    if not url.startswith('http://5sing.kugou.com/'):
        print("Error URL")
    else:
        ret = re.match("http://5sing.kugou.com/(.*?)", url)
        if not ret==None:
            url=ret.group()
        else:
            pass

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(chrome_options=options)

        orglist = []
        coverlist = []

        driver.get(url)
        print('Searching songs')

        wait = WebDriverWait(driver, 10)
        ele = wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'原创'))).click()
        findsong(0)

        while is_nextpage():
            nexturl = driver.find_element_by_link_text('下一页').get_attribute('href')
            driver.get(nexturl)
            findsong(0)

        orglistlen = len(orglist)
        print('Found', orglistlen, 'org song(s)')

        driver.find_element_by_link_text('翻唱').click()
        findsong(1)

        while is_nextpage():
            nexturl = driver.find_element_by_link_text('下一页').get_attribute('href')
            driver.get(nexturl)
            findsong(1)

        coverlistlen = len(coverlist)
        # print(coverlistlen)
        print('Found', coverlistlen, 'cover song(s)')


        makefolder('原创')
        for i in orglist:
            savesong(i, path='原创')

        makefolder('翻唱')
        for i in coverlist:
            savesong(i, path='翻唱')

        driver.quit()
