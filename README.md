# LinkedIn Ad Library API – working example (Python, JS, n8n)

Export every ad a company runs on LinkedIn from the public LinkedIn Ad Library – copy, headline, CTA, landing page, impressions, countries and targeting – to CSV or JSON.

Powered by the [linkedin-ad-library-scraper](https://apify.com/lagenuina_agency/linkedin-ad-library-scraper) actor on Apify. No browser, no cookies, no account on LinkedIn.

## Example output (real result, shortened)

```json
{
  "adId": "1558746953",
  "adUrl": "https://www.linkedin.com/ad-library/detail/1558746953",
  "format": "SINGLE_IMAGE",
  "advertiserName": "IXTENSA 🧡 HubSpot",
  "paidBy": "IXTENSA GmbH & Co. KG",
  "headline": "Live-Webinar am 14.10.2026 um 11 Uhr",
  "body": "Viele HubSpot-Kunden kämpfen mit denselben Problemen…",
  "ctas": [
    "Sign Up"
  ],
  "clickUrl": "https://lp.ixtensa.de/webinar-hubspot-probleme?utm_campaign=Webinar+HubSpot+Probleme&utm_source=linkedin&utm_medium=paid",
  "landingDomain": "lp.ixtensa.de",
  "availability": {
    "start": "2026-09-24",
    "end": "2026-10-10"
  },
  "impressions": "5k-10k",
  "impressionsMin": 5000,
  "impressionsMax": 10000,
  "impressionsPerCountry": [
    {
      "country": "Germany",
      "impressions": "100%",
      "percent": 100
    }
  ],
  "targeting": {
    "language": "English",
    "location": "Germany"
  }
}
```

## Quickstart (3 steps)

1. Create a free Apify account and copy your API token from [Settings → Integrations](https://console.apify.com/settings/integrations).
2. Put it in an environment variable (never in code): `export APIFY_TOKEN=your_token`
3. Run the example:

```bash
pip install -r python/requirements.txt
python python/example.py hubspot --country US
```

JavaScript: `cd js && npm install && node example.mjs`

## Examples

**Python** (`pip install "apify-client<2"`)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("lagenuina_agency/linkedin-ad-library-scraper").call(run_input={
  "companies": [
    "hubspot"
  ],
  "countries": [
    "US"
  ],
  "dateOption": "last-30-days",
  "resultsLimit": 50
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

**JavaScript / Node.js** (`npm install apify-client`)

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('lagenuina_agency/linkedin-ad-library-scraper').call({"companies": ["hubspot"], "countries": ["US"], "dateOption": "last-30-days", "resultsLimit": 50});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

**cURL / any language** – one HTTP call, results in the response:

```bash
curl -X POST "https://api.apify.com/v2/acts/lagenuina_agency~linkedin-ad-library-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["cybersecurity"], "countries": ["DE"], "resultsLimit": 100, "skipDetails": true}'
```

All input fields are documented on the [actor page](https://apify.com/lagenuina_agency/linkedin-ad-library-scraper) (Input tab).

## Use case: Export all of a company's LinkedIn ads to CSV

`python/example.py` searches the LinkedIn Ad Library for one advertiser and writes `linkedin_ads_<company>.csv` with ad ID, format, headline, copy, CTA, landing page, impressions range, run dates, payer and ad URL – ready for Excel or Google Sheets.

## n8n workflow

[`n8n/workflow.json`](n8n/workflow.json): every Monday 08:00 → run the actor (only ads not seen before) → flatten the fields with a Set node → append to Google Sheets.

1. In n8n: **Workflows → Import from File** and pick `n8n/workflow.json`.
2. Create a **Header Auth** credential named `Apify API token` with name `Authorization` and value `Bearer <your token>`, and select it in the *Run Apify actor* node.
3. Edit the JSON body (your keywords/targets), set your Google Sheet ID and activate.

The `run-sync-get-dataset-items` endpoint waits up to 300 s; for bigger runs use `/runs` plus a webhook.

## Use with AI agents (MCP)

Give Claude, ChatGPT, Cursor or any MCP client this actor as a tool:

```
https://mcp.apify.com/?actors=lagenuina_agency/linkedin-ad-library-scraper
```

Example config (Claude Desktop, Cursor, VS Code):

```json
{
  "mcpServers": {
    "linkedin-ad-library-scraper": {
      "url": "https://mcp.apify.com/?actors=lagenuina_agency/linkedin-ad-library-scraper"
    }
  }
}
```

Sign in with Apify OAuth when asked, or send `Authorization: Bearer <APIFY_TOKEN>`.

## Pricing

From $3.20 per 1,000 ads with full details on the Apify Free plan down to $0.90 on Gold and above (list-only with `skipDetails`: $1.60 down to $0.44), no start fee, pay only for results – see [lagenuina_agency/linkedin-ad-library-scraper](https://apify.com/lagenuina_agency/linkedin-ad-library-scraper).

## Disclaimer

Independent, not affiliated with LinkedIn (not endorsed by LinkedIn Corporation). It reads only publicly available data. Use it in line with the applicable terms and laws.

## License

[MIT](LICENSE) © Quelli di Carne Genuina
