from urllib.parse import urlparse

def get_domain_name(url):
    return urlparse(url).netloc

def group_links(urls):
    links = {}
    for l in urls:
        domain = get_domain_name(l)
        if domain in links:
            links.get(domain).append(l)
        else:
            links.update({domain: [l]})

    return links
