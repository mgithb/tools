const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
// Enable the stealth plugin
puppeteer.use(StealthPlugin());
// Parse arguments from the command line
const args = process.argv.slice(2);
const targetUrl = args[0];
if (!targetUrl) {
  console.error('Please provide a URL as the first argument.');
  process.exit(1);
}
(async () => {
  console.log('Launching browser in headless mode...');
  const browser = await puppeteer.launch({
    ignoreHTTPSErrors: true,
    headless: true, // Running the browser in headless mode
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  // Set a specific user agent
  await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/117.0.5938.60 Safari/537.36');
  // Add event listeners for logging
  page.on('console', message => console.log('PAGE LOG:', message.text()));
  page.on('pageerror', ({ message }) => console.log('PAGE ERROR:', message));
  page.on('response', response => console.log(`Response from ${response.url()}: ${response.status()}`));
  page.on('requestfailed', request => console.log(`Request failed ${request.url()}: ${request.failure().errorText}`));
  page.on('request', request => {
    if (request.resourceType() === 'script')
      console.log(`Script request to ${request.url()}`);
  });
  console.log(`Navigating to ${targetUrl}...`);
  await page.goto(targetUrl, { waitUntil: 'networkidle2', timeout: 0 }).catch(e => {
    console.log('Navigation failed:', e);
  });
  console.log('Page loaded, network is idle now.');
  // Interact with the page, e.g., click a button
  console.log('Attempting to click on the element...');
  await page.click('SELECTOR_FOR_CLICK').catch(e => {
    console.log('Click failed:', e);
  });
  console.log('Interaction complete.');
  console.log('Closing browser...');
  await browser.close();
})();
