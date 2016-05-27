import requests

def get_title(url, dest_url):
    response = requests.get(url).json()
    page_id = response['query']['pages'].keys()[0]
    if int(page_id) > 0:
        title = response['query']['pages'][page_id]['title'].replace(' ', '_')
        return '<' + dest_url + title + '>'
    else:
        return None

def get_wikipedia_urls(url, dest_url, words):
    wiki_urls = []
    for line in words:
        urls_dict = {}
        if type(line[0]) == tuple:
            i = 0
            while i < len (line):
                tup = line[i]
                key = tup[0] + '%20' + tup[1]
                final_dest_url = get_title(url + key, dest_url)
                if final_dest_url != None:
                    urls_dict[tup[0] + " " + tup[1]] = final_dest_url
                    i += 1
                else:
                    final_dest_url = get_title(url + tup[0], dest_url)
                    if final_dest_url != None:
                        urls_dict[tup[0]] = final_dest_url
                i += 1

        wiki_urls.append(urls_dict)

    final_dest_url = get_title(url + tup[1], dest_url)
    if final_dest_url != None:
        wiki_urls[-1][tup[1]] = final_dest_url

    return wiki_urls

