import re
import requets
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd


def main(url):
    original_url = urllib
    unscraped = deque([original_url])
    scraped = set()
    emails = set()

    while len(unscraped):
        url = unscraped.popleft()
        scrapped.add(url)
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        if '/' in parts.path:
            path = url[:url.rfind('/')+1]
        else:
            path = url

        print("Crawling through URL %s" % url)
        try:
            reponse = request.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        # ignore pages with errors and continue with next url
        continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com",
                  response.text, re.I)) # re.I: (ignore case)
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, 'lxml')

        for anchor in soup.find_all("a"):

            if "href" in anchor.attrs:
                link = anchor.attrs["href"]
            else:
                link = ''

            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link

            if not link.endswith(".gz"):
                if not link in unscraped and not link in scraped:
                    unscraped.append(link)

    df = pd.DataFrame(emails, columns=["Email"]) # replace with column name you prefer
    df.to_csv('email.csv', index=False)


if __name__ == '__main__':
    print("Enter url..... ")
    url = input(">>> ")
    main(url)
