import requests
import json
from bs4 import BeautifulSoup
import re


# Class for colored terminal output
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Constant to use for printing separation lines
breakPrint = f"{bcolors.UNDERLINE}\n{' ' * 80}\n{bcolors.ENDC}"

# List of text to avoid
avoid_text = ["mobiles accessories", "TV & Home Appliances", "Personal Cares"]


def custom_print(data: any, endPrint=False):
    """
    Print data with a custom separator before and after the content.
    If endPrint is True, print the separator after the content as well.
    """
    print(breakPrint)
    print(data)
    if endPrint:
        print(breakPrint)


def custom_print_dict(data: dict):
    """
    Print each key-value pair in the dictionary using custom_print function.
    """
    print(breakPrint)
    for key, value in data.items():
        print(f"{key}: {value}")
    print(breakPrint)


def print_list(data: list):
    """
    Print each item in the list using custom_print function.
    """
    for item in data:
        custom_print(item)
    print(breakPrint)


def write_in_file(data: any, file_name: str):
    """
    Write data to a file in JSON format. If an error occurs, print an error message.
    """
    try:
        with open(file_name, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error writing to the file: {file_name} - {e}")


def fetch_page(url: str) -> BeautifulSoup:
    """
    Fetch the HTML content of a given URL using requests and parse it with BeautifulSoup.
    If an error occurs, print an error message and return None.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"{bcolors.OKGREEN}{url}{bcolors.ENDC}")
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred: {e} on url: {url}{bcolors.ENDC}")
        return None


def append_to_list_in_file(key: str, number: float):
    """
    Append a number to a list in a JSON file under a specified key.
    If the file does not exist or contains invalid JSON, initialize with an empty dictionary.
    """
    try:
        try:
            with open("time.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if key in data:
            data[key].append(number)
        else:
            data[key] = [number]

        with open("time.json", "w") as file:
            json.dump(data, file)
    except Exception as e:
        print(f"An error occurred: {e}")


def print_execution_time(start: float, end: float):
    """
    Print the time taken for an operation.
    """
    custom_print(f"Time taken = {end-start:.3f} Seconds", True)


def soup_text_exists(soup: BeautifulSoup) -> str:
    """
    Check if a BeautifulSoup element exists and return its text.
    """
    return soup.text.strip() if soup else ""


def is_in_stock(soup: BeautifulSoup) -> bool:
    """
    Check if a product is in stock based on its BeautifulSoup element.
    """
    return True if soup and soup.text == "In Stock" else False


def get_max_page_number(soup: BeautifulSoup) -> int:
    """
    Extract the maximum page number from a pagination element in the BeautifulSoup object.
    """
    data = [
        int(x.text) for x in soup.select(".pagination a") if x and x.text.isnumeric()
    ]
    return data[-1] if data else 1


def get_product_urls(soup: BeautifulSoup, base_url: str) -> list[str]:
    """
    Extract product URLs from the BeautifulSoup object and append them to the base URL.
    """
    return [base_url + x["href"] for x in soup.select(".productBox a")]


def extract_numbers(text: str) -> float:
    """
    Extract the first number from a string, which may include commas and decimal points.
    """
    if not text:
        return None

    match = re.search(r"\d+(?:,\d{3})*(?:\.\d+)?", text)
    if match:
        num_str = match.group(0)
        return (
            int(num_str.replace(",", ""))
            if "." not in num_str
            else float(num_str.replace(",", ""))
        )
    return None


def product_json_data(data: BeautifulSoup, url: str) -> dict:
    """
    Extract product data from a BeautifulSoup object containing JSON-LD scripts.
    """
    ld_json_scripts = data.select('script[type="application/ld+json"]')

    if len(ld_json_scripts) > 2:
        json_string = ld_json_scripts[2].string.strip()
        sanitized_json_string = json_string.replace("\n", " ").replace("\r", " ")
        sanitized_json_string = re.sub(r"[\x00-\x1f\x7f]", "", sanitized_json_string)
        try:
            product_data = json.loads(sanitized_json_string)
        except json.JSONDecodeError as e:
            custom_print(f"Error parsing JSON: {e} on url: {url}", True)
            product_data = {}
    else:
        custom_print("Not enough JSON-LD scripts found.", True)
        product_data = {}

    return product_data


def main_img_url(soup: BeautifulSoup) -> list[str]:
    """
    Extract the main product image URL from the BeautifulSoup object.
    """
    img = soup.select_one("#product-image-main img")
    return [img["src"]] if img else []


def check_duplicates(file_name="data.json"):
    """
    Check for duplicate product URLs in a JSON file.
    """
    try:
        with open(file_name, "r") as file:
            urls = [x["product_url"] for x in json.load(file)]

        seen = set()
        duplicates = [url for url in urls if url in seen or seen.add(url)]
        (
            print_list(duplicates)
            if duplicates
            else custom_print("Hurray!! No duplicate Data", True)
        )
    except Exception as e:
        print(f"An error occurred: {e}")


def product_dict(data, json_data, offers, aggregate_rating, url, urls) -> dict:
    """
    Create a dictionary with product details extracted from JSON data and BeautifulSoup object.
    """
    return {
        "product_name": json_data.get("name", ""),
        "brand_name": json_data.get("brand", ""),
        "price": int(offers.get("price", 0)),
        "previous_price": extract_numbers(
            soup_text_exists(data.select_one(".stock-info"))
        ),
        "currency": offers.get("priceCurrency"),
        "images": [img["src"] for img in data.select(".product-image-thumbnail img")]
        or main_img_url(data),
        "in_stock": is_in_stock(data.select_one(".stock-status")),
        "rating": float(aggregate_rating.get("ratingValue", 0.0)),
        "rating_count": int(aggregate_rating.get("ratingCount", 0)),
        "colors": [color.text for color in data.select(".color-name")],
        "product_url": json_data.get("url", url),
        "trail": urls,
    }


def unique_by_last_element(lists: list[list[str]]) -> list[list[str]]:
    """
    Find unique sublists in a list of lists based on the last element of each sublist.
    """
    unique_dict = {}
    for sublist in lists:
        if not sublist:
            continue
        key = sublist[-1]
        if key not in unique_dict:
            unique_dict[key] = sublist

    return list(unique_dict.values())
