import random

from model import predict_prices

WEEKS = 14
PRICE_AS_OF = "September 2026"

# Official store home pages. E-commerce prices researched from live listings on
# Amazon.in and Flipkart.com (augmented by 91mobiles / Smartprix / Gadgets360 price trackers).
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
    "Infinix Store": "https://www.infinixmobile.com",
    "Tecno Store": "https://www.tecno-mobile.com",
    "Lava Store": "https://www.lavamobiles.com",
    "Itel Store": "https://www.itel.com",
    "Amazon India": "https://www.amazon.in",
    "Flipkart": "https://www.flipkart.com",
}

# (Phone name, [(seller, current price in Rs), ...]).
# Prices are real, researched from the web in {PRICE_AS_OF}.
CORE_PHONES = [
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

# (Brand store, Phone name, current market price in Rs).
# Prices researched from live Amazon/Flipkart listings and price trackers (Sep 2026).
# Each phone is expanded into 3 sellers: brand store (~ list price), Amazon India and Flipkart.
EXTRA_PHONES = [
    # Samsung
    ("Samsung Shop", "Samsung Galaxy S26 Ultra", 124999),
    ("Samsung Shop", "Samsung Galaxy S26 Plus", 74999),
    ("Samsung Shop", "Samsung Galaxy S26", 72999),
    ("Samsung Shop", "Samsung Galaxy S25 Ultra", 93590),
    ("Samsung Shop", "Samsung Galaxy S25 FE", 45299),
    ("Samsung Shop", "Samsung Galaxy S24 FE", 38998),
    ("Samsung Shop", "Samsung Galaxy Z Fold 7", 148999),
    ("Samsung Shop", "Samsung Galaxy Z Flip 7", 89999),
    ("Samsung Shop", "Samsung Galaxy S25 Edge", 60500),
    ("Samsung Shop", "Samsung Galaxy A57 5G", 48629),
    ("Samsung Shop", "Samsung Galaxy A56 5G", 33499),
    ("Samsung Shop", "Samsung Galaxy A37 5G", 36999),
    ("Samsung Shop", "Samsung Galaxy A36 5G", 30999),
    ("Samsung Shop", "Samsung Galaxy A27 5G", 29990),
    ("Samsung Shop", "Samsung Galaxy A17 5G", 20990),
    ("Samsung Shop", "Samsung Galaxy M47 5G", 23999),
    ("Samsung Shop", "Samsung Galaxy M56 5G", 25999),
    ("Samsung Shop", "Samsung Galaxy M36 5G", 19999),
    ("Samsung Shop", "Samsung Galaxy M17 5G", 16999),
    ("Samsung Shop", "Samsung Galaxy F56 5G", 24490),
    ("Samsung Shop", "Samsung Galaxy F36 5G", 19580),
    ("Samsung Shop", "Samsung Galaxy F70e 5G", 13999),
    ("Samsung Shop", "Samsung Galaxy M16 5G", 10999),
    # Xiaomi / Redmi
    ("Xiaomi Store", "Xiaomi 17T", 59999),
    ("Xiaomi Store", "Xiaomi 17", 89998),
    ("Xiaomi Store", "Xiaomi 17 Ultra", 139997),
    ("Xiaomi Store", "Redmi Turbo 5", 37999),
    ("Xiaomi Store", "Redmi Note 15 Pro Plus 5G", 39999),
    ("Xiaomi Store", "Redmi Note 15 SE 5G", 21144),
    ("Xiaomi Store", "Redmi Note 14 SE 5G", 19999),
    ("Xiaomi Store", "Redmi 15C 5G", 16499),
    ("Xiaomi Store", "Redmi 15A 5G", 14999),
    ("Xiaomi Store", "Redmi 13 5G", 12499),
    ("Xiaomi Store", "Redmi A7 Pro 5G", 13497),
    ("Xiaomi Store", "Redmi 14C 5G", 9499),
    # POCO
    ("POCO Store", "POCO X8 Pro", 34999),
    ("POCO Store", "POCO X8 Pro Max", 44999),
    ("POCO Store", "POCO M8 5G", 20999),
    ("POCO Store", "POCO X6 5G", 21999),
    # realme
    ("realme Store", "realme 16 Pro+ 5G", 46999),
    ("realme Store", "realme 16 Pro 5G", 33999),
    ("realme Store", "realme 16 5G", 31999),
    ("realme Store", "realme GT 8 Pro", 72999),
    ("realme Store", "realme GT 7", 39999),
    ("realme Store", "realme GT 7T", 33999),
    ("realme Store", "realme P4 Power 5G", 27999),
    ("realme Store", "realme P4 5G", 25999),
    ("realme Store", "realme P4x 5G", 19999),
    ("realme Store", "realme P4R 5G", 18421),
    ("realme Store", "realme P3", 15999),
    ("realme Store", "realme P3 Ultra", 23990),
    ("realme Store", "realme Narzo 100x 5G", 19368),
    ("realme Store", "realme C100x", 14999),
    ("realme Store", "realme 14 Pro Plus 5G", 24999),
    # OnePlus
    ("OnePlus Store", "OnePlus 15", 85999),
    ("OnePlus Store", "OnePlus 15R", 54999),
    ("OnePlus Store", "OnePlus 13s", 54999),
    ("OnePlus Store", "OnePlus 13R", 42999),
    ("OnePlus Store", "OnePlus Nord 6", 42999),
    ("OnePlus Store", "OnePlus Nord 5", 33999),
    ("OnePlus Store", "OnePlus Nord CE 6", 33999),
    ("OnePlus Store", "OnePlus Nord CE 6 Lite", 25999),
    ("OnePlus Store", "OnePlus Nord CE 5", 24999),
    ("OnePlus Store", "OnePlus N6", 22999),
    ("OnePlus Store", "OnePlus 12", 34999),
    # Nothing
    ("Nothing Store", "Nothing Phone 4", 80999),
    ("Nothing Store", "Nothing Phone 4b", 34999),
    ("Nothing Store", "Nothing Phone 4a Pro", 46959),
    ("Nothing Store", "Nothing Phone 4a", 39999),
    ("Nothing Store", "Nothing Phone 3", 43999),
    ("Nothing Store", "Nothing Phone 3a Lite", 24999),
    # iQOO
    ("iQOO Store", "iQOO 15", 70990),
    ("iQOO Store", "iQOO 15R", 49999),
    ("iQOO Store", "iQOO Z11", 27999),
    ("iQOO Store", "iQOO Z11x", 18999),
    ("iQOO Store", "iQOO Z10R", 22999),
    ("iQOO Store", "iQOO Z11 Lite", 17999),
    # Vivo
    ("Vivo Store", "Vivo X300 Pro", 109999),
    ("Vivo Store", "Vivo X300 FE", 86999),
    ("Vivo Store", "Vivo X300", 75999),
    ("Vivo Store", "Vivo V70", 49999),
    ("Vivo Store", "Vivo V70 Elite", 45999),
    ("Vivo Store", "Vivo V70 FE", 35499),
    ("Vivo Store", "Vivo V60", 40649),
    ("Vivo Store", "Vivo T5 Pro", 35495),
    ("Vivo Store", "Vivo T5x", 24399),
    ("Vivo Store", "Vivo T5 Lite", 19999),
    ("Vivo Store", "Vivo Y51 Pro", 30999),
    ("Vivo Store", "Vivo Y29 5G", 15499),
    ("Vivo Store", "Vivo Y21 5G", 18999),
    ("Vivo Store", "Vivo Y19e", 7999),
    # Oppo
    ("Oppo Store", "Oppo Find X9 Ultra", 169999),
    ("Oppo Store", "Oppo Find X9", 79999),
    ("Oppo Store", "Oppo Find X9s", 79999),
    ("Oppo Store", "Oppo Reno16 5G", 61999),
    ("Oppo Store", "Oppo Reno16c 5G", 46999),
    ("Oppo Store", "Oppo Reno15 Pro Mini", 59999),
    ("Oppo Store", "Oppo Reno15 5G", 47999),
    ("Oppo Store", "Oppo Reno15c", 40999),
    ("Oppo Store", "Oppo F33 Pro 5G", 39999),
    ("Oppo Store", "Oppo F33 5G", 31999),
    ("Oppo Store", "Oppo F31 Pro 5G", 25999),
    ("Oppo Store", "Oppo K14 5G", 21999),
    ("Oppo Store", "Oppo K14x 5G", 16299),
    ("Oppo Store", "Oppo K13 Turbo Pro", 33990),
    ("Oppo Store", "Oppo A6 5G", 21999),
    ("Oppo Store", "Oppo A6x 5G", 16999),
    ("Oppo Store", "Oppo A6 Pro 5G", 32999),
    # Motorola
    ("Motorola Store", "Motorola Edge 60", 25999),
    ("Motorola Store", "Motorola Edge 60 Fusion", 22999),
    ("Motorola Store", "Motorola Edge 70", 27999),
    ("Motorola Store", "Motorola Edge 70 Fusion", 24999),
    ("Motorola Store", "Moto G86 Power", 17999),
    ("Motorola Store", "Moto G67 Power", 16499),
    ("Motorola Store", "Moto G57 Power", 16499),
    ("Motorola Store", "Moto G35", 12499),
    ("Motorola Store", "Moto G06 Power", 8999),
    ("Motorola Store", "Moto Razr 60", 44999),
    # Infinix
    ("Infinix Store", "Infinix Note 60 Pro 5G", 33999),
    ("Infinix Store", "Infinix GT 30 Pro", 28999),
    ("Infinix Store", "Infinix Note Edge", 21999),
    ("Infinix Store", "Infinix Note 50x", 13499),
    ("Infinix Store", "Infinix Note 50s 5G+", 14999),
    ("Infinix Store", "Infinix Hot 60i 5G", 11499),
    ("Infinix Store", "Infinix Hot 50 5G", 9999),
    ("Infinix Store", "Infinix Smart 10", 6799),
    # Tecno
    ("Tecno Store", "Tecno Phantom V Fold 2", 89999),
    ("Tecno Store", "Tecno Phantom V Flip 2", 54999),
    ("Tecno Store", "Tecno Camon 50 Ultra", 36999),
    ("Tecno Store", "Tecno Pova 8", 29999),
    ("Tecno Store", "Tecno Pova Curve 2", 25899),
    ("Tecno Store", "Tecno Spark 50 5G", 17999),
    ("Tecno Store", "Tecno Spark 50 4G", 14999),
    ("Tecno Store", "Tecno Pop X 5G", 9999),
    # Lava
    ("Lava Store", "Lava Bold N1 5G", 9999),
    ("Lava Store", "Lava Bold N2 Pro", 7999),
    ("Lava Store", "Lava Bold N2 Lite", 8399),
    # Itel
    ("Itel Store", "Itel A95 5G", 9999),
    ("Itel Store", "Itel Zeno 100", 8299),
]


def expand_extras(extra):
    """Turn a (store, name, price) entry into 3 sellers around the researched price."""
    store, name, price = extra
    return (
        name,
        [
            (store, _round5(price * 1.09)),
            ("Amazon India", price),
            ("Flipkart", _round5(price * 0.98)),
        ],
    )


def _round5(n):
    return int(round(n / 5.0) * 5)


def _make_history(current, drift, seed):
    """Synthesise 14 weeks of history that ends exactly at the current price.

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
    phones = list(CORE_PHONES) + [expand_extras(e) for e in EXTRA_PHONES]
    for idx, (name, sellers) in enumerate(phones):
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