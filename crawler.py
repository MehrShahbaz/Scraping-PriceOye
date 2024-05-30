from custom_parser import (
    fetch_product_category_urls,
    fetch_all_product_urls,
    fetch_product_details,
)
import multiprocessing

from helper import (
    fetch_page,
    get_max_page_number,
    get_product_urls,
    unique_by_last_element,
)


def scrape_all_product_urls(urls: list[str]) -> list[str]:
    soup = fetch_page(urls[-1])
    max_page = get_max_page_number(soup)
    results = get_product_urls(soup, urls)

    if max_page > 1:
        results.extend(fetch_all_product_urls(max_page, urls))

    return results


def scrape_all_product_category_urls(urls: list[list[str]]):
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = pool.map(scrape_all_product_urls, urls)
    pool.close()
    pool.join()

    return [item for sublist in results for item in sublist]


def fetch_all_product_details(urls: list[list[str]]):
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = pool.map(fetch_product_details, urls)
    pool.close()
    pool.join()

    return [x for x in results if x]


def crawl(base_url: str) -> list[dict]:
    product_category_urls = fetch_product_category_urls(base_url)

    res = scrape_all_product_category_urls(product_category_urls)

    result = unique_by_last_element(res)

    results = fetch_all_product_details(result)

    return results
