from helper import (
    avoid_text,
    custom_print,
    fetch_page,
    get_product_urls,
    product_dict,
    product_json_data,
)


def fetch_product_details(urls: list[str]) -> dict:
    try:
        if not urls:
            return {}

        url = urls.pop()
        data = fetch_page(url)

        if not data:
            return {}

        json_data = product_json_data(data, url)
        if not json_data:
            return {}

        offers = json_data.get("offers", {})
        aggregate_rating = json_data.get("aggregateRating", {})

        return product_dict(data, json_data, offers, aggregate_rating, url, urls)
    except Exception as e:
        custom_print(f"An error occurred: {e} on url: {url}", True)
        return {}


def fetch_product_urls_from_page(urls: list[str]):
    soup = fetch_page(urls[-1])
    if soup:
        return get_product_urls(soup, urls)
    return []


def fetch_all_product_urls(max_page: int, base_urls: list[str]) -> list[str]:
    urls = [base_urls + [base_urls[-1] + f"?page={x}"] for x in range(2, max_page + 1)]

    results = []
    for url in urls:
        results.extend(fetch_product_urls_from_page(url))

    return results


def fetch_product_category_urls(base_url: str) -> list[str]:
    soup = fetch_page(base_url)
    return [
        [base_url, x["href"]]
        for x in soup.select(".all-cat-icon a")
        if x.text not in avoid_text
    ]
