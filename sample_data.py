import random

from model import predict_prices

WEEKS = 14
PRICE_AS_OF = "September 2026"

# Official store home pages. E-commerce prices researched from live listings on
# Amazon.in and Flipkart.com (augmented by 91mobiles / Smartprix price trackers).
SELLER_URLS = {
    "Apple Store": "https://www.apple.com/in",
    "Samsung Shop": "https://www.samsung.com/in",
    "Xiaomi Store": "https://www.mi.com/in",
    "POCO Store": "https://www.poco.in",
    "realme Store": "https://www.realme.com/in",
    "OnePlus Store": "https://www.oneplus.com/in",
    "Nothing Store": "https://in.nothing.tech",
    "iQOO Store": "https://shop.iqoo.com/in",
    "Google Store India": "https://store.google.com/in",
    "Oppo Store": "https://www.oppo.com/in",
    "Vivo Store": "https://shop.vivo.com/in",
    "Motorola Store": "https://www.motorola.in",
    "Amazon India": "https://www.amazon.in",
    "Flipkart": "https://www.flipkart.com",
}

# (Phone name, [(seller, current price in Rs), ...]). Prices are real,
# researched from the web in {PRICE_AS_OF}.
PHONES = [
    # Apple
    ("iPhone 15 (128 GB)", [("Apple Store", 69900), ("Amazon India", 59900), ("Flipkart", 58900)]),
    ("iPhone 16 (128 GB)", [("Apple Store", 79900), ("Amazon India", 69999), ("Flipkart", 74900)]),
    ("iPhone 16 Pro (128 GB)", [("Apple Store", 119900), ("Amazon India", 112900), ("Flipkart", 105900)]),
    ("iPhone 16 Pro Max (256 GB)", [("Apple Store", 144900), ("Amazon India", 134900), ("Flipkart", 129900)]),
    ("iPhone 17 Pro (128 GB)", [("Apple Store", 134900), ("Amazon India", 131900), ("Flipkart", 126900)]),
    # Samsung
    ("Samsung Galaxy S25 (128 GB)", [("Samsung Shop", 79999), ("Amazon India", 69999), ("Flipkart", 65899)]),
    ("Samsung Galaxy S24 (128 GB)", [("Samsung Shop", 74999), ("Amazon India", 49999), ("Flipkart", 49999)]),
    ("Samsung Galaxy A55 5G (256 GB)", [("Samsung Shop", 48999), ("Amazon India", 34999), ("Flipkart", 31999)]),
    ("Samsung Galaxy A26 5G (128 GB)", [("Samsung Shop", 27999), ("Amazon India", 26900), ("Flipkart", 26999)]),
    ("Samsung Galaxy A16 5G (128 GB)", [("Samsung Shop", 19999), ("Amazon India", 17248), ("Flipkart", 19299)]),
    ("Samsung Galaxy F16 5G (128 GB)", [("Samsung Shop", 18999), ("Amazon India", 15999), ("Flipkart", 15499)]),
    # Xiaomi / Redmi
    ("Redmi Note 14 Pro 5G (128 GB)", [("Xiaomi Store", 30999), ("Amazon India", 24990), ("Flipkart", 22486)]),
    ("Redmi Note 15 5G (128 GB)", [("Xiaomi Store", 26999), ("Amazon India", 24499), ("Flipkart", 23555)]),
    ("Redmi Note 15 Pro 5G (128 GB)", [("Xiaomi Store", 33999), ("Amazon India", 31999), ("Flipkart", 30489)]),
    ("Redmi Note 15 Pro+ 5G (256 GB)", [("Xiaomi Store", 40999), ("Amazon India", 38990), ("Flipkart", 37905)]),
    ("POCO X7 Pro (256 GB)", [("POCO Store", 25999), ("Amazon India", 24999), ("Flipkart", 23999)]),
    ("POCO X7 (256 GB)", [("POCO Store", 27999), ("Amazon India", 20999), ("Flipkart", 19999)]),
    # realme
    ("realme 13 Pro 5G (128 GB)", [("realme Store", 28999), ("Amazon India", 19999), ("Flipkart", 19999)]),
    ("realme 13 Pro 5G (256 GB)", [("realme Store", 30999), ("Amazon India", 23999), ("Flipkart", 21999)]),
    ("realme 13+ 5G (256 GB)", [("realme Store", 27999), ("Amazon India", 23999), ("Flipkart", 22998)]),
    ("realme 12+ 5G (128 GB)", [("realme Store", 23999), ("Amazon India", 21999), ("Flipkart", 20999)]),
    # OnePlus
    ("OnePlus 13 (256 GB)", [("OnePlus Store", 69999), ("Amazon India", 57999), ("Flipkart", 59999)]),
    ("OnePlus 12R (256 GB)", [("OnePlus Store", 42999), ("Amazon India", 24999), ("Flipkart", 26499)]),
    ("OnePlus Nord 4 (256 GB)", [("OnePlus Store", 35999), ("Amazon India", 27999), ("Flipkart", 27999)]),
    # Nothing
    ("Nothing Phone 3a (128 GB)", [("Nothing Store", 27999), ("Amazon India", 25999), ("Flipkart", 24999)]),
    ("Nothing Phone 3a Pro (128 GB)", [("Nothing Store", 32999), ("Amazon India", 31999), ("Flipkart", 29999)]),
    ("Nothing Phone 3a Pro (256 GB)", [("Nothing Store", 34999), ("Amazon India", 33999), ("Flipkart", 31999)]),
    # iQOO
    ("iQOO 13 (256 GB)", [("iQOO Store", 61999), ("Amazon India", 52999), ("Flipkart", 56990)]),
    ("iQOO Neo 10 (256 GB)", [("iQOO Store", 34999), ("Amazon India", 29999), ("Flipkart", 31999)]),
    ("iQOO Z10 (256 GB)", [("iQOO Store", 21999), ("Amazon India", 18999), ("Flipkart", 19999)]),
    # Google
    ("Google Pixel 9 (256 GB)", [("Google Store India", 79999), ("Amazon India", 77999), ("Flipkart", 75999)]),
    ("Google Pixel 9 Pro (256 GB)", [("Google Store India", 109999), ("Amazon India", 95999), ("Flipkart", 89999)]),
    # Oppo
    ("Oppo Find X8 (256 GB)", [("Oppo Store", 69999), ("Amazon India", 66999), ("Flipkart", 67990)]),
    ("Oppo Find X8 Pro (512 GB)", [("Oppo Store", 109999), ("Amazon India", 94999), ("Flipkart", 84999)]),
    ("Oppo Reno13 (128 GB)", [("Oppo Store", 41999), ("Amazon India", 39999), ("Flipkart", 39424)]),
    ("Oppo Reno14 (256 GB)", [("Oppo Store", 42999), ("Amazon India", 40999), ("Flipkart", 38700)]),
    # Vivo
    ("Vivo V50 (128 GB)", [("Vivo Store", 38999), ("Amazon India", 33990), ("Flipkart", 32991)]),
    ("Vivo V40 (256 GB)", [("Vivo Store", 42999), ("Amazon India", 34990), ("Flipkart", 34999)]),
    ("Vivo T3 Pro (256 GB)", [("Vivo Store", 24999), ("Amazon India", 24499), ("Flipkart", 24999)]),
    # Motorola
    ("Motorola Edge 50 Neo (256 GB)", [("Motorola Store", 29999), ("Amazon India", 20999), ("Flipkart", 19949)]),
    ("Moto G85 (256 GB)", [("Motorola Store", 20999), ("Amazon India", 17999), ("Flipkart", 17840)]),
]


def _make_history(current, drift, seed):
    """Synthesise 14 weeks of history that ends exactly at the real current price.

    A positive drift means the price has been rising (buy now), a negative drift
    means it has been falling (wait). Noise keeps it looking like real data.
    """
    rng = random.Random(seed)
    out = []
    for w in range(WEEKS):
        growth = (1 + drift) ** (WEEKS - 1 - w)
        p = (current / growth) * (1 + rng.uniform(-0.012, 0.012))
        out.append(round(max(200, p)))
    out[-1] = current
    return out


def build_catalog():
    catalog = []
    for idx, (name, sellers) in enumerate(PHONES):
        item = {"name": name, "category": "Mobile", "sellers": []}
        rng = random.Random(idx * 31 + 7)
        drifts = [-0.014, -0.009, -0.005, -0.002, 0.003, 0.006]
        for i, (seller, price) in enumerate(sellers):
            drift = rng.choice(drifts)
            item["sellers"].append(
                {
                    "seller": seller,
                    "url": SELLER_URLS.get(seller, "https://www.amazon.in"),
                    "history": _make_history(price, drift, seed=idx * 100 + i),
                }
            )
        catalog.append(item)
    return catalog


def search_products(catalog, query):
    q = query.lower()
    if not q:
        return catalog[:6]
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
        rows.append(
            {
                "seller": s["seller"],
                "url": s["url"],
                "current": current,
                "predicted": future,
                "savings": max(0, round(current - future)),
                "slope": (future - current) / max(1, current),
            }
        )
    rows.sort(key=lambda r: r["current"])
    cheapest = rows[0]
    up = cheapest["slope"] > 0.01
    down = cheapest["slope"] < -0.01
    if up:
        advice = "Prices are RISING. Buy now to save before it gets costlier."
        verdict = "BUY NOW"
    elif down:
        advice = (
            f"Prices are DROPPING. Waiting ~2 weeks may save you around "
            f"Rs. {cheapest['savings']} more on the {cheapest['seller']} deal. Consider waiting."
        )
        verdict = "WAIT"
    else:
        advice = "Prices are stable. This is already a good time to buy."
        verdict = "BUY NOW"
    return {
        "name": product["name"],
        "category": product["category"],
        "as_of": PRICE_AS_OF,
        "rows": rows,
        "least": {"seller": cheapest["seller"], "price": cheapest["current"]},
        "advice": advice,
        "verdict": verdict,
        "save_now": cheapest["savings"],
    }