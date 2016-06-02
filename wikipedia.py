import requests

def clean_uni_gram_candidates(uni_grams, wiki_term):
    unknowns = []
    knowns = []
    for term in wiki_term:
        a = term[0].split(' ')
        knowns.append(a[0])
        knowns.append(a[1])
    for word in uni_grams:
        if word not in knowns:
            unknowns.append(word)
    return unknowns

def get_title(url):
    response = requests.get(url).json()
    page_id = response['query']['pages'].keys()[0]
    if int(page_id) > 0:
        title = response['query']['pages'][page_id]['title']
        return title
    else:
        return None

def get_wikipedia_urls(url, dest_url, bi_grams):
    wiki_url_terms = []
    flag = False
    for bi_gram in bi_grams:
        if not flag:
            wiki_term = get_title(url + bi_gram)
            if wiki_term != None:
                wiki_url_terms.append([bi_gram, wiki_term])
                flag = True
                continue;

        flag = False
    return wiki_url_terms