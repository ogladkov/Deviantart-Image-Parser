from bs4 import BeautifulSoup
import requests
from time import sleep
import os

cycles = int(input('Type how many searchterms you will use: '))

header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
searchterm = []

for _ in range(cycles):
    key = input('Type next searchterm: ')
    qty = int(input('How many of them do you want? '))
    searchterm.append([key, qty])
    
def parse_da(key, qty):
    
    print('Starting with {0} images of {1}...'.format(qty, key))
    counter = 0
    succounter = 0
    
    if not os.path.exists(key):
        os.mkdir(key)
    
    kw_merged = ''
    for k in key.split(' '):
        if k != key.split(' ')[-1]:
            kw_merged += (k + '+')
        else:
            kw_merged += k
            
    url = r'https://www.deviantart.com/popular-all-time/?q={0}&offset={1}'.format(kw_merged, qty)
    
    urls = []
    for number in [str(o) for o in list(range(0, qty, 23))]:
        urls.append(r'https://www.deviantart.com/popular-all-time/?q={0}&offset={1}'.format(kw_merged, number))
    
    print('Prepairing urls...')
    img_links = []
    for url in urls:
        response = requests.Session()
        response = response.get(url, headers=header)
        soup = BeautifulSoup(response.text, "html5lib")
        for s in soup.body.findAll('a'):
            if str(s).startswith('<a class="torpedo-thumb-link"'):
                row = (str(s).split(' '))
                for s in row:
                    if s.startswith('src='):
                        s = s.split('"')[1]
                        s = s.split('jpg')[0] + 'jpg'
                        img_links.append(s)
        response.close()
        sleep(2)
    
    print('Downloading...')
    for img in img_links:
        if counter >= qty:
            break
        counter += 1    
        try:
            response = requests.get(img, stream=True, headers=header)
            img_path = os.getcwd() + '/%s' % key + '/' + img.split('/')[-1]
            file = open(img_path, "wb")
            file.write(response.raw.read())
            file.close()
            succounter += 1
        except:
            print("Couldn't get the image")
        del response
        sleep(3)
    print('Finished for searchterm {}\n'.format(key))
    
# Run the script    
for key, qty in searchterm:
    parse_da(key, qty)