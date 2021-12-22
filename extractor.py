import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
import os
# from google.colab import files
#change

class extract:

  def email_extracting(self, u):

    original_url = u

    unscraped = deque([original_url])

    scraped = set()

    emails = set()

    while len(unscraped):
        url = unscraped.popleft()
        scraped.add(url)

        parts = urlsplit(url)

        base_url = "{0.scheme}://{0.netloc}".format(parts)
        if '/' in parts.path:
          path = url[:url.rfind('/')+1]
        else:
          path = url

        print("Crawling URL %s" % url)
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        doms = {'.in', '.com', '.org', '.edu'}

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", response.text, re.I))
        new_emails_1 = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.in", response.text, re.I))
        new_emails_2 = set(re.findall(r"[a-z0-9\.\-+_]+[at][a-z0-9\.\-+_]+\[dot]]", response.text, re.I))
        emails.update(new_emails)
        emails.update(new_emails_1)
        emails.update(new_emails_2)

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


    # path = os.getcwd()
    df = pd.DataFrame(emails, columns=["Email"])
    
    df.to_csv('/home/kali/scripts/mop-up/data/emails.csv', index=False)
    return emails


obj = extract()
obj.email_extracting("http://www.technicianoverlord.com/emails/k")