import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

def fetch_sitemap(url):
    print(f"Fetching sitemap from {url}")
    response = requests.get(url)
    return response.text

def parse_sitemap(sitemap_xml):
    print("Parsing sitemap XML")
    soup = BeautifulSoup(sitemap_xml, features='xml')
    urls = [url.loc.text for url in soup.find_all('url')]
    print(f"Found {len(urls)} URLs in sitemap")
    return urls

def filter_cerfa_urls(urls):
    print("Filtering URLs to include only those containing 'cerfa'")
    cerfa_urls = [url for url in urls if 'cerfa' in url]
    print(f"Found {len(cerfa_urls)} 'cerfa' URLs")
    return cerfa_urls

def fetch_page_content(url):
    response = requests.get(url)
    return response.text

def filter_urls(urls):
    filtered_urls = []
    print("Filtering URLs based on content")
    for url in tqdm(urls):
        page_content = fetch_page_content(url)
        soup = BeautifulSoup(page_content, 'html.parser')

        # Exclusion based on specific div
        if soup.select_one("body > div.page-content > div.bg-light.pb-8.pb-lg-12 > div > div > div.col-xxl-3.col-md-4.order-1.order-md-0 > div"):
            continue

        # Exclusion based on word count in specific section
        seo_section = soup.select_one("#section-seo")
        if seo_section and len(seo_section.get_text().split()) > 350:
            continue

        title = soup.title.string if soup.title else ''
        meta_description = ''
        if soup.find('meta', attrs={'name': 'description'}):
            meta_description = soup.find('meta', attrs={'name': 'description'})['content']
        
        filtered_urls.append({
            'url': url,
            'title': title,
            'meta_description': meta_description
        })

    print(f"Filtered down to {len(filtered_urls)} URLs")
    return filtered_urls

def save_to_json(data, filename='filtered_urls.json'):
    print(f"Saving filtered URLs to {filename}")
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("Save complete")

def main():
    sitemap_url = 'https://www.startdoc.fr/sitemap_documents.xml'
    sitemap_xml = fetch_sitemap(sitemap_url)
    urls = parse_sitemap(sitemap_xml)
    cerfa_urls = filter_cerfa_urls(urls)
    filtered_urls = filter_urls(cerfa_urls)
    save_to_json(filtered_urls)

if __name__ == '__main__':
    main()
