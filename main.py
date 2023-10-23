import sys
import requests 
from bs4 import BeautifulSoup


TO_CRAWL = []
CRAWLED = set()


def request(url):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}
    try:
        response = requests.get(url, headers=header)
        return response.text
    except KeyboardInterrupt:
        print("\nProgram interrupted by the user.")
        sys.exit()
    except:
        pass


def get_links(html):
    links = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        tags_a = soup.find_all("a", href=True)
        if tags_a is not None:
            for tag in tags_a:
                link = tag["href"]
                if link.startswith("http"):
                    links.append(link)
        return links
    except:
        pass

def crawl():
    try:
        while 1:
            if TO_CRAWL:
                url = TO_CRAWL.pop()
                html = request(url)
                if html:
                    links = get_links(html)
                    if links:
                        for link in links:
                            if link not in CRAWLED and link not in TO_CRAWL:
                                TO_CRAWL.append(link)
                    print(f"Crawling {url}")
                    CRAWLED.add(url)
                else:
                    CRAWLED.add(url)
            else:
                print("Done!")
                break
    except KeyboardInterrupt:
        print("\nProgram interrupted by the user.")


if __name__ == "__main__":
    url = sys.argv[1]
    TO_CRAWL.append(url)
    crawl()
