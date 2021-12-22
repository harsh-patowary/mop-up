import cycler
import extractor

cycler_obj = cycler.cycle()
extractor_obj = extractor.extract()


if __name__ == "__main__":
    # base_url = input("Enter the base url: ")
    urls = set()
    urls = cycler_obj.url_cycling()
    for url in urls:
        extractor_obj.email_extracting(url)
