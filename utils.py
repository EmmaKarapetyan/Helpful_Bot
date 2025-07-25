from bs4 import BeautifulSoup
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
import pyautogui
import time
import ast
import random


def translate_text(search_txt = ' '):
    try:
        translator = Translator()
        translated = translator.translate(search_txt)
        return translated.text
    except:
        return "Translation not found"    


def user_gen():
    try:
        url = 'https://randomuser.me/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')

        res = ''
        for tag in soup.find_all(['pre']):
            res = tag.text
        res_dict = ast.literal_eval(res)
        return res_dict['results']
    except:
        return "Generate stoped"


def rand_name_chooses():
    try:
        url = 'https://www.fakenamegenerator.com/'
        Headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        response = requests.get(url, headers=Headers)
        soup = BeautifulSoup(response.text,'html.parser')

        choose = {}
        atr = ['gen', 'n', 'c']
        c = 0
        for i in soup.find(['div'], id="criteria").find_all(['li'], class_='lab'):
            try:
                l=[]
                for j in soup.find(['div'], id="criteria").find(['select'], id=atr[c]).find_all(['option']):
                    l.append(j.text)
                choose[i.text] = l
                c += 1        
            except:
                break         
        return '\n'.join([f'{key}: {value}' for key, value in choose.items()])
    except:
        return "Search stoped"

def name_gen(g = 'random', n='American', c='Australia'):
    try:
        name_sets = {'American': 'us', 'Arabic': 'ar', 'Australian': 'au', 'Brazil': 'br', 'Chechen (Latin)': 'chechen-latin', 
            'Chinese': 'ch', 'Chinese (Traditional)': 'ch-traditional','Croatian': 'hr', 'Czech': 'cz', 'Danish': 'dk', 'Dutch': 'nl',
            'England/Wales': 'england-wales', 'Eritrean': 'er', 'Finnish': 'fi', 'French': 'fr', 'German': 'de', 'Greenland': 'gl',
            'Hispanic': 'his', 'Hobbit': 'hobbit', 'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Italian': 'it',
            'Japanese': 'jp', 'Japanese (Anglicized)': 'jp-anglicized', 'Klingon': 'klingon', 'Ninja': 'ninja', 'Norwegian': 'no',
            'Persian': 'fa', 'Polish': 'pl', 'Russian': 'ru', 'Russian (Cyrillic)': 'ru-cyrillic', 'Scottish': 'sc',
            'Slovenian': 'sl', 'Swedish': 'se', 'Thai': 'th', 'Vietnamese': 'vn'
        }

        country_names_map = {'Australia': 'au', 'Austria': 'at', 'Belgium': 'be', 'Brazil': 'br', 'Canada': 'ca', 
            'Cyprus (Anglicized)': 'cy-anglicized', 'Cyprus (Greek)': 'cy-greek', 'Czech Republic': 'cz', 'Denmark': 'dk', 'Estonia': 'ee',
            'Finland': 'fi', 'France': 'fr', 'Germany': 'de', 'Greenland': 'gl', 'Hungary': 'hu', 'Iceland': 'is', 'Italy': 'it', 
            'Netherlands': 'nl', 'New Zealand': 'nz', 'Norway': 'no', 'Poland': 'pl', 'Portugal': 'pt', 'Slovenia': 'si',
            'South Africa': 'za', 'Spain': 'es', 'Sweden': 'se', 'Switzerland': 'ch', 'Tunisia': 'tn', 'United Kingdom': 'uk', 
            'United States': 'us', 'Uruguay': 'uy'
        }

        name_set = name_sets[n]
        country = country_names_map[c]

        url = f'https://www.fakenamegenerator.com/gen-{g}-{name_set}-{country}.php'        
        Headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        response = requests.get(url, headers=Headers)
        soup = BeautifulSoup(response.text,'html.parser')
        info = {}

        info['name'] = soup.find(['div'], class_ = 'info').find(['div'], class_="address").find(['h3']).text
        info['address'] = soup.find(['div'], class_ = 'info').find(['div'], class_="adr").text.strip()

        for item in soup.find(['div'], class_ = 'info').find(['div'], class_="extra").find_all(['dl']):
            try:
                key = item.find(['dt']).text
                value = item.find(['dd']).text
                info[key] = value
                value += f'{item.find('a')['href']}'
                info[key] = value
            except:
                continue
        info.pop('QR Code')
        return info
    except:
        return "Generate stoped"


def rand_num(start, end):
    return random.randrange(start, end)


def rand_any(key):
    info = name_gen()
    return info[key]


def check_email_pwned(email): 
    if email != 'Previous page':
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://haveibeenpwned.com/')
        time.sleep(3)
        pyautogui.typewrite(email)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(10)
        res = requests.get('https://haveibeenpwned.com/')
        textik = res.text
        #print(textik)
        driver.quit()
        if 'Good news' in textik:
            return 'Everything is OK with your gmail!'
        return 'Your gmail is pwned!'

def email_search_by_url(url):#+
    if url != 'Previous page':
        ans = ""
        response = requests.get(f'https://www.skymem.info/srch?q={url}&ss=home')
        soup = BeautifulSoup(response.text,'html.parser')
        for tag in soup.find_all(['a'],href=True):
            href = tag['href']
            if href and '@' in href:
                ans+=href[8:]
                ans+="\n"
        return ans
