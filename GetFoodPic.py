from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen, build_opener, urlretrieve, Request
import json
import lxml
import os

#programtically go through google image ajax json return and save links to list#
#num_images is more of a suggestion                                            #
#it will get the ceiling of the nearest 100 if available                       #
def get_links(query_string):
    #initialize place for links
    links = []
    query_string = query_string.replace(' ','%20')

    url="https://www.google.co.in/search?q="+query_string+"&source=lnms&tbm=isch"

    print('URL: %s' %url)

    #set user agent to avoid 403 error
    request = Request(url, None, {'User-Agent': 'Mozilla/5.0'})
    #returns json formatted string of the html
    json_string = urlopen(request).read()

    new_soup = Soup(json_string, 'lxml')

    #all img tags, only returns results of search
    imgs = new_soup.find_all('img')

    #loop through images and put src in links list
    for j in range(len(imgs)):
        this_string  = str(imgs[j])
        if ('src' in this_string):
            img_url = this_string.split('''src="''')[1].split('''"''')[0]
            if ('http' in img_url):
                links.append(img_url)

    return links

def get_image(name):
    links = get_links(name)

    #for i in range(len(links)):
    filename, headers = urlretrieve(links[0])
    #img_name = filename.split('\\')[-1]
    #os.rename(filename, dest_dir + img_name + '.jpg')

    #return img_name + '.jpg'
    return filename

if __name__ == '__main__':
    pass
