// LinkedIn ads of a company in the last 30 days, with reach.
// Usage: node example.mjs hubspot
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set APIFY_TOKEN first: https://console.apify.com/settings/integrations');
    process.exit(1);
}

const company = process.argv[2] ?? 'hubspot';
const client = new ApifyClient({ token });
const run = await client.actor('lagenuina_agency/linkedin-ad-library-scraper').call({
    companies: [company],
    dateOption: 'last-30-days',
    resultsLimit: 50,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const ad of items) {
    console.log(`${ad.format}  ${ad.impressions ?? '?'} impressions  ${ad.headline ?? ''}  ${ad.adUrl}`);
}
