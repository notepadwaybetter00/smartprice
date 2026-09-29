# LIVE price overrides — verified against current web listings / price trackers
# (Amazon & Flipkart + 91mobiles, Smartprix, Gadgets360, news coverage) in late Sep 2026.
# Each value is the current market price; when applied, Amazon & Flipkart are set to it
# and the brand store is marked ~5% above (list price).
#
# Sources (Sep 18-29, 2026):
#   - Samsung S26 series hike -> 91mobiles / SamMobile / WION (new prices effective Sep 23)
#   - iPhone 17/Air hike + iPhone 18 launch -> The Hindu (Sep 10) / smartprix.com
#   - Xiaomi/Redmi prices -> gadgets360.com price list, gadgetsnow (Note 17 Pro launch)
#   - OnePlus 15 / Nord 5 -> flipkart.com live listings
#   - Vivo X300 / X300 FE hike -> pricehunt.com, 91mobiles (Sep 25)
#   - Nothing 4a/4b -> 91mobiles (Sep 28), smartprix
#   - iQOO 15 / Z11 -> beebom, swapupdate, cashify
LIVE_UPDATES = {
    # Samsung flagships (hiked Sep 23 2026)
    "Samsung Galaxy S26": 102999,
    "Samsung Galaxy S26 Plus": 134999,
    "Samsung Galaxy S26 Ultra": 154999,
    "Galaxy S26 Ultra (512 GB)": 174999,
    # Apple
    "iPhone 17 (256 GB)": 99900,
    "iPhone 17 Pro (256 GB)": 126900,
    "iPhone 17 Air (256 GB)": 149900,
    # Xiaomi / Redmi
    "Xiaomi 17T": 57990,
    "Redmi Note 15 5G (128 GB)": 23034,
    "Redmi Note 15 Pro 5G (256 GB)": 28340,
    "Redmi Note 15 Pro+ 5G (256 GB)": 39490,
    "Redmi Note 17 Pro (128 GB)": 36999,
    "Redmi Note 17 Pro (256 GB)": 39999,
    # OnePlus
    "OnePlus 15": 83990,
    "OnePlus Nord 5": 39999,
    # Vivo
    "Vivo X300 FE": 89999,
    "Vivo V70": 42415,
    "Vivo V70 FE": 38250,
    "Vivo T5 (128 GB)": 34999,
    "Vivo Y51 Pro": 32999,
    # Oppo
    "Oppo Find X9": 66000,
    "Oppo F33 Pro 5G": 36990,
    # Nothing
    "Nothing Phone 4b": 35999,
    "Nothing Phone 4a": 39999,
    "Nothing Phone 4a Pro": 49999,
    # iQOO
    "iQOO 15": 76999,
    "iQOO 15R": 53990,
    "iQOO Z11": 34999,
    # Motorola
    "Motorola Edge 70 Max (256 GB)": 54999,
}