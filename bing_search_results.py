from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
from urllib.error import URLError
from urllib.error import HTTPError
# # https://www.bing.com/search?q=tkinter+tutorial&first=21
def bing_query_search_links(query_search, start=1, num_links=101):
    if start == 0:
        print('warn: start must not equals: Zero.')
        print('what? _the start must starts from: One.')
        exit
    if num_links > 1000:
        print('warn: number of links must not be larger than : 1000')
        exit
    print('1: start & end has been checked!')
    q = '+'.join(query_search.split())
    print('2: query has been prepared!')
    search_url = 'https://www.bing.com/search?q='+q
    print('3: search url has been prepared!')
    page_number_keyword = '&first='
    # // 1  >  1
    # // 2  > 11
    # // 3  > 21
    # // 10 > 91
    print('--------')
    print('4: start preparations the links of query= '+q)
    search_links = []
    # Need to change this loop to start from user_start
    # start from link_1
    for start in range(num_links):
        page_search_url = ''
        if start == 0:
            print('start getting the urls!')
        elif start == 1:
            page_search_url = search_url+page_number_keyword+str(start)
            print('link'+str(start)+' has been prepared!')
        else:
            number_of_page = str(start-1)+str(1)
            page_search_url = search_url+page_number_keyword+number_of_page
            print('link'+str(start)+' has been prepared!')
        if start != 0:
            search_links.append(page_search_url+'&FORM=')
            print('link'+str(start)+' has been add!')
        print('--------')
    return search_links
bing_query_links = bing_query_search_links('content marketting', 1, 10)
print('5: url links has been prepared!')
def new_bs(url):
    try:
        res = urlopen(url)
    except URLError as e:
        print('server error!', e)
        return None
    except HTTPError as e:
        print('response error!', e)
        return None
    html = res.read()
    return BeautifulSoup(html, 'html.parser')
# [['title':title,'description':desc, 'link':link], [],[]]
def bing_url_results_data(page):
    page_rslts_data = []
    page_rslts = page.select("#b_results")[0].find_all(
        "li", {'class': 'b_algo'})
    # h2 > title & link
    # .b_caption > Caption []
    for rslt in page_rslts:
        title_link = rslt.select('h2')[0]
        # print(title_link)
        title = 'not found!'
        link = 'not found!'
        # print(title_link.a.get_text().strip())
        # print(title_link != None)
        # print(title_link.a['href'])
        # print(rslt.find(class_='b_caption').p.get_text().strip())
        # print('------------')
        if title_link != None:
            # print(title_link)
            # print('------')
            try:
                title = title_link.a.get_text().strip()
                # print(title)
                # print('--------')
                if 'href' in title_link.a.attrs:
                    link = title_link.a['href']
            except AttributeError:
                title = 'a is not available!'
                link = 'a is not available!'
        try:
            description = rslt.find(class_='b_caption').p.get_text().strip()
        except AttributeError:
            description = 'there is no description available!'
        page_rslts_data.append([title, link, description])
    # print(len(page_rslts))
    # print(page_rslts[0].attrs)
    print('end extract url!')
    return page_rslts_data
    # return [[], []]
def bing_url_data(pages_urls):
    # urls_data = []
    for page_url in pages_urls:
        print('start request the url: '+page_url)
        page = new_bs(page_url)
        if page != None:
            print('start extract url: '+page_url)
            page_data = bing_url_results_data(page)
            # print(page_data)
            # print('-----------------------')
            store_bing_rslts_urls(page_data)
        else:
            print('request_error: url= '+page_url+' -> we cannont request it.')
print('6: store results and links')
def store_bing_rslts_urls(page_data):
    # urls_data = bing_page_date(query_urls)
    with open('content_marketting.csv', 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        for data in page_data:
            csv_writer.writerow(data)
    print('end store url data!')  
bing_url_data(bing_query_links)
# for url in bing_query_links:
#   print(url)
# i = 1
# for i in range(3):
#   print(i)
# # 0
# # 1
# # 2
