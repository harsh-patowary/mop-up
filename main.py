import cycler
import extractor


cycler_obj = cycler.cycle()
extractor_obj = extractor.extract()


if __name__ == "__main__":
    # base_url = input("Enter the base url: ")
    urls = set()
    urls = cycler_obj.url_cycling()
    emails = []
    for url in urls:
        
        emails = extractor_obj.email_extracting(url)
        extractor_obj.write_file(emails, url)
        if(len(emails)>0):
            # print(emails)
            print("**Crawl Successfull**")

        else:
            print(f"+Empty Link+ {url}+")
            print(f"Empty links are links with null extracts")
