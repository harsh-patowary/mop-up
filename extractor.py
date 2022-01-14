import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
import csv
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


   
    return emails


  def write_file(self, emails, u):
    # file = open("/data/emails.csv")
    dict = {} 
    # print(emails)
    for email in emails:
      # print(email) 
      dict.update({email: u})

    print(dict)
    if (len(dict)>0):
      with open('data/emails.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for email, u in dict.items():
          writer.writerow([email, u])
          print("**writing**")

    print("**write func complete**")
# obj = extract()
# emails = ["adada@asdcsc.com", "ada@asdcsc.com", "adada@assc.com", "aa@asdcsc.com", "adada@assc.com"]
# u = "http://www.technician.com/emails/"
# obj.write_file(emails, u)
# obj.email_extracting("http://www.technicianoverlord.com/emails/")