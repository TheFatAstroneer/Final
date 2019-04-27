from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen, build_opener, urlretrieve, Request
import json
import lxml
import os

'''
This script searches images on Google given a query, using urllib to access html and obtain info
from html pages. The images found on html are saved locally.
'''
def get_links(query_string):
    '''
    This method gets links of images found on Googel after searching the query given
    **Parameters**
        query_string: *String*
            The name to be searched on Google Image
    **Return**
        links: *list* *String*
            A list of links of images found
    '''
    # Initialize list that stores image links
    links = []
    # Put query into url that allows Google search
    query_string = query_string.replace(' ','%20')
    url="https://www.google.co.in/search?q="+query_string+"&source=lnms&tbm=isch"

    #set user agent to avoid 403 error
    request = Request(url, None, {'User-Agent': 'Mozilla/5.0'})
    #get page info after accessing the url
    page = urlopen(request).read()
    #analyze and find all links that directs to images on the web page
    new_soup = Soup(page, 'lxml')
    imgs = new_soup.find_all('img')

    #loop through image links and put those links into the list
    for j in range(len(imgs)):
        this_string  = str(imgs[j])
        if ('src' in this_string):
            img_url = this_string.split('''src="''')[1].split('''"''')[0]
            if ('http' in img_url):
                links.append(img_url)

    return links

def get_image(name):
    '''
    Access the first image link and download it
    **Parameters**
        name: *String*
            The name to be searched
    **Return**
        filename: *String*
            The directory of the image file downloaded
    '''
    links = get_links(name)
    filename, headers = urlretrieve(links[0])
    return filename

if __name__ == '__main__':
    pass
