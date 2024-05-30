# Scrape Priceoye

This python Script scrapes website [Priceoye](https://priceoye.pk/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip install -r requirements.txt
```

## Usage

### Command

```bash
python main.py
```

## Description

- After the Usage command is run the website will be scrapped
- A new file (data.json) if not existing will be created
- The data will be stored in the file
- time.json file be created with list of execution time which is in .gitignore

## Data Format

```bash
[
   {
    "product_name": "String",
    "brand_name": "String",
    "price": Number,
    "previous_price": Number //if present,
    "currency": "String" //if present,
    "images": ["String"],
    "in_stock": Bool,
    "rating": Float,
    "rating_count": Number,
    "colors": ["String"],
    "product_url": "String",
    "trail": ["String"]
  }
]
```

## Sample Data

```bash
{
    "product_name": "Xiaomi Redmi Note 13",
    "brand_name": "Xiaomi",
    "price": 47299,
    "previous_price": 49999,
    "currency": "PKR",
    "images": [
      "https://images.priceoye.pk/xiaomi-redmi-note-13-pakistan-priceoye-5bmcz-500x500.webp"
    ],
    "in_stock": true,
    "rating": 5.0,
    "rating_count": 186,
    "colors": ["Ocean Sunset", "Ice Blue", "Mint Green", "Midnight Black"],
    "product_url": "https://priceoye.pk/mobiles/xiaomi/xiaomi-redmi-note-13",
    "trail": ["https://priceoye.pk", "https://priceoye.pk/mobiles"]
  }
]
```

## Packages used

- Python (3.12.2)
- beautifulsoup4
- certifi
- charset-normalizer
- idna
- lxml
- requests
- soupsieve
- urllib3
