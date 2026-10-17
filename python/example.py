"""Export every LinkedIn ad of one company to CSV.

Usage: python example.py hubspot --country US
"""
import argparse
import csv
import os
import sys

from apify_client import ApifyClient

ACTOR = "lagenuina_agency/linkedin-ad-library-scraper"
TOKEN = os.environ.get("APIFY_TOKEN")
if not TOKEN:
    sys.exit("Set APIFY_TOKEN first: https://console.apify.com/settings/integrations")

FIELDS = ["adId", "format", "advertiserName", "headline", "body", "ctas", "clickUrl",
          "impressionsMin", "impressionsMax", "start", "end", "paidBy", "adUrl"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("company", help="advertiser name as typed in the Ad Library, e.g. hubspot")
    p.add_argument("--country", action="append", default=[], help="two-letter code, repeatable")
    p.add_argument("--limit", type=int, default=500)
    a = p.parse_args()

    client = ApifyClient(TOKEN)
    run = client.actor(ACTOR).call(run_input={
        "companies": [a.company],
        "countries": a.country,
        "resultsLimit": a.limit,
    })
    out = f"linkedin_ads_{a.company}.csv"
    n = 0
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for ad in client.dataset(run["defaultDatasetId"]).iterate_items():
            ran = ad.get("availability") or {}
            w.writerow({**ad, "ctas": " | ".join(ad.get("ctas") or []), "start": ran.get("start"), "end": ran.get("end")})
            n += 1
    print(f"{n} ads -> {out}")


if __name__ == "__main__":
    main()
