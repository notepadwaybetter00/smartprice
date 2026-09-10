import random

from model import predict_prices

WEEKS = 14

PRODUCTS = [
    {
        "name": "iPhone 15 128GB",
        "category": "Mobile",
        "sellers": [
            ("Apple Store", 79900, 65900),
            ("Amazon India", 79990, 62990),
            ("Flipkart", 79999, 61999),
        ],
    },
    {
        "name": "Samsung Galaxy S23 5G",
        "category": "Mobile",
        "sellers": [
            ("Samsung Shop", 74999, 58999),
            ("Amazon India", 74999, 54000),
            ("Flipkart", 74999, 53999),
        ],
    },
    {
        "name": "Realme 11 Pro 5G (256GB)",
        "category": "Mobile",
        "sellers": [
            ("Realme Store", 27999, 21999),
            ("Amazon India", 27999, 20998),
            ("Flipkart", 27999, 20990),
        ],
    },
    {
        "name": "Sony WH-1000XM5 Headphones",
        "category": "Electronics",
        "sellers": [
            ("Sony Store", 29990, 24990),
            ("Amazon India", 29950, 23990),
            ("Flipkart", 29990, 23499),
        ],
    },
    {
        "name": "boAt Airdopes 141 TWS Earbuds",
        "category": "Electronics",
        "sellers": [
            ("boAt Store", 1999, 1299),
            ("Amazon India", 1999, 1099),
            ("Flipkart", 1999, 999),
        ],
    },
    {
        "name": "Dell Inspiron 15 Laptop (i5 13th Gen)",
        "category": "Laptop",
        "sellers": [
            ("Dell Store", 75990, 62990),
            ("Amazon India", 75990, 58490),
            ("Flipkart", 75990, 57990),
        ],
    },
    {
        "name": "Nike Air Zoom Pegasus 40",
        "category": "Footwear",
        "sellers": [
            ("Nike Store", 11995, 7495),
            ("Amazon India", 11995, 6895),
            ("Flipkart", 11995, 6495),
        ],
    },
    {
        "name": "Campus Odyssey Running Shoes",
        "category": "Footwear",
        "sellers": [
            ("Campus Store", 1599, 1099),
            ("Amazon India", 1599, 899),
            ("Flipkart", 1599, 849),
        ],
    },
]


def _make_history(base, low, trend, seed):
    rng = random.Random(seed)
    prices = []
    for w in range(WEEKS):
        drift = base + (trend * w)
        seasonal_dip = -450 if 8 <= w <= 10 else 0
        noise = rng.uniform(-0.02, 0.02) * base
        p = max(low - 300, round(drift + seasonal_dip + noise))
        prices.append(p)
    return prices


def build_catalog():
    catalog = []
    for p in PRODUCTS:
        item = {
            "name": p["name"],
            "category": p["category"],
            "sellers": [],
        }
        for i, (seller, base, low) in enumerate(p["sellers"]):
            # trend in rupees per week: mix of falling, steady, rising
            trend = random.Random(len(catalog) * 100 + i).choice(
                [-380, -200, -90, 40, 180]
            )
            item["sellers"].append(
                {
                    "seller": seller,
                    "url": "https://example.com/" + seller.lower().replace(" ", "-"),
                    "history": _make_history(base, low, trend, seed=len(catalog) * 7 + i),
                }
            )
        catalog.append(item)
    return catalog


def search_products(catalog, query):
    q = query.lower()
    if not q:
        return catalog[:4]
    out = []
    for item in catalog:
        if q in item["name"].lower() or q in item["category"].lower():
            out.append(item)
    return out


def enrich(product):
    rows = []
    for s in product["sellers"]:
        hist = s["history"]
        current = hist[-1]
        predictions = predict_prices(hist, steps=2)
        future = predictions[-1]
        savings = max(0, round(current - future))
        rows.append(
            {
                "seller": s["seller"],
                "url": s["url"],
                "current": current,
                "predicted": future,
                "savings": savings,
                "slope": (future - current) / max(1, current),
            }
        )
    rows.sort(key=lambda r: r["current"])
    cheapest = rows[0]
    trend_up = cheapest["slope"] > 0.01
    trend_down = cheapest["slope"] < -0.01
    if trend_up:
        advice = "Prices are RISING. Buy now to save before it gets costlier."
        verdict = "BUY NOW"
    elif trend_down:
        advice = (
            f"Prices are DROPPING. Waiting ~2 weeks may save you around "
            f"Rs. {cheapest['savings']} more. Consider waiting."
        )
        verdict = "WAIT"
    else:
        advice = "Prices are stable. This is already a good time to buy."
        verdict = "BUY NOW"
    return {
        "name": product["name"],
        "category": product["category"],
        "rows": rows,
        "least": {"seller": cheapest["seller"], "price": cheapest["current"]},
        "advice": advice,
        "verdict": verdict,
        "save_now": cheapest["savings"],
    }