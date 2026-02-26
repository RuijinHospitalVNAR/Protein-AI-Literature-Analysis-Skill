# API Documentation

This document provides detailed information about the APIs used by the Protein AI Literature Analysis skill.

## PubMed API

### Base URL
`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

### Endpoints

#### ESearch
Used to search PubMed and retrieve PMIDs (PubMed IDs).

**URL:** `esearch.fcgi`

**Parameters:**
- `db`: Database to search (must be 'pubmed')
- `term`: Search term in PubMed syntax
- `retmax`: Maximum number of results to return
- `retmode`: Return mode (xml or json)
- `sort`: Sort order (relevance, newest, etc.)

**Rate Limit:** 3 requests per second

#### EFetch
Used to retrieve detailed information for a list of PMIDs.

**URL:** `efetch.fcgi`

**Parameters:**
- `db`: Database to fetch from (must be 'pubmed')
- `id`: Comma-separated list of PMIDs
- `retmode`: Return mode (xml or json)
- `rettype`: Return type (abstract, full, etc.)

**Rate Limit:** 3 requests per second

## bioRxiv API

### Base URL
`https://api.biorxiv.org/`

### Endpoints

#### Papers
Used to search for bioRxiv preprints.

**URL:** `papers/`

**Parameters:**
- `jcode`: Journal code (biorxiv or medrxiv)
- `limit`: Maximum number of results to return
- `format`: Response format (json)
- `subject_category`: Comma-separated list of subject categories
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)

**Rate Limit:** 10 requests per second

#### Detail
Used to get detailed information for a specific preprint.

**URL:** `detail/{jcode}/{server}/{id}`

**Parameters:**
- `jcode`: Journal code (biorxiv or medrxiv)
- `server`: Server identifier
- `id`: Preprint ID

**Rate Limit:** 10 requests per second

## arXiv API

### Base URL
`http://export.arxiv.org/api/`

### Endpoints

#### Query
Used to search arXiv for papers.

**URL:** `query`

**Parameters:**
- `search_query`: Search query in arXiv syntax
- `start`: Start index for results
- `max_results`: Maximum number of results to return
- `sortBy`: Sort order (relevance, submittedDate, lastUpdatedDate)
- `sortOrder`: Sort direction (ascending or descending)

**Rate Limit:** 1 request per 3 seconds

## Google Scholar

### Overview
Google Scholar does not provide an official API. However, there are multiple approaches to search Google Scholar programmatically.

### Recommended Approaches

#### 1. Scholarly Library (Python)
- **GitHub:** https://github.com/scholarly-python-package/scholarly
- **Installation:** `pip install scholarly`
- **Features:** Free, open-source, basic search capabilities
- **Limitations:** Subject to rate limiting, may require CAPTCHA solving

#### 2. SerpAPI
- **Website:** https://serpapi.com/
- **Pricing:** Paid service with free tier
- **Features:** Reliable, comprehensive, no rate limiting
- **Benefits:** Handles CAPTCHAs, provides structured JSON responses

#### 3. Browser Automation (Selenium)
- **Installation:** `pip install selenium`
- **Additional Requirement:** ChromeDriver (download and add to PATH)
- **Features:** Full browser interaction, handles CAPTCHAs manually
- **Benefits:** Works like a real user, no API restrictions
- **Limitations:** Slower, requires manual CAPTCHA solving

### Browser Automation Example
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# Configure browser
options = Options()
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

try:
    # Navigate to Google Scholar
    driver.get("https://scholar.google.com/")
    time.sleep(2)
    
    # Search
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("artificial intelligence protein design")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    
    # Handle CAPTCHA if present
    if "CaptchaRedirect" in driver.current_url:
        print("Complete CAPTCHA in browser")
        input()
        time.sleep(3)
    
    # Extract results
    results = driver.find_elements(By.CSS_SELECTOR, "div.gs_r.gs_or.gs_scl")
    for result in results:
        title = result.find_element(By.CSS_SELECTOR, "h3.gs_rt a").text
        url = result.find_element(By.CSS_SELECTOR, "h3.gs_rt a").get_attribute("href")
        print(f"{title}: {url}")
finally:
    driver.quit()
```

### Example Usage (Scholarly)
```python
from scholarly import scholarly

# Search Google Scholar
search_query = scholarly.search_pubs('artificial intelligence protein design')

# Iterate through results
for i, pub in enumerate(search_query):
    print(f"{i+1}. {pub['bib']['title']}")
    if i >= 9:  # Limit to 10 results
        break
```

## X (Twitter) API

### Overview
X (Twitter) provides an official API, but it requires authentication and has rate limits. For users without API access, browser automation is an alternative approach.

### Official API Approach

#### Base URL
`https://api.twitter.com/2/`

#### Authentication
Requires a Twitter Developer account and bearer token authentication.

1. Create a Twitter Developer account: https://developer.twitter.com/
2. Create a project and app
3. Generate a bearer token
4. Include the bearer token in API requests

#### Endpoints

##### Recent Search
Used to search for recent tweets matching a query.

**URL:** `tweets/search/recent`

**Parameters:**
- `query`: Search query
- `max_results`: Maximum number of results (10-100)
- `tweet.fields`: Comma-separated list of fields to return
- `expansions`: Comma-separated list of expansions

**Rate Limit:** 450 requests per 15-minute window

### Browser Automation Approach

#### Requirements
- **Installation:** `pip install selenium`
- **Browser Drivers:**
  - **Edge:** EdgeDriver (download and add to PATH)
    - Download: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
  - **Chrome:** ChromeDriver (download and add to PATH)
    - Download: https://chromedriver.chromium.org/downloads
- **X Account:** Required for viewing search results

#### Features
- **No API limits:** Uses the web interface like a regular user
- **Full access:** Can view all tweets visible in the browser
- **Interactive:** Allows manual login and interaction
- **Browser Choice:** Supports both Edge and Chrome browsers

#### Limitations
- **Slower:** Requires browser interaction
- **Login required:** Must be logged in to view search results
- **UI dependent:** Selectors may break if X changes their UI

### Browser Automation Example
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# Configure browser
options = Options()
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

try:
    # Navigate to X search
    driver.get("https://x.com/search")
    time.sleep(2)
    
    # Enter search query
    search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search']")
    search_query = "(protein design) (AI) filter:links"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    
    # Handle login prompt
    if "login" in driver.current_url.lower():
        print("Please login to your X account in the browser")
        input()
        time.sleep(3)
    
    # Scroll to load more tweets
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    # Extract tweets
    tweet_elements = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")
    for tweet in tweet_elements:
        try:
            text = tweet.find_element(By.CSS_SELECTOR, "div[data-testid='tweetText']").text
            links = []
            for link in tweet.find_elements(By.CSS_SELECTOR, "a[href]"):
                href = link.get_attribute("href")
                if href and not href.startswith("https://x.com"):
                    links.append(href)
            if links:
                print(f"Tweet: {text[:100]}...")
                print(f"Links: {links}")
        except:
            continue
    
finally:
    driver.quit()
```

### Example API Call
```python
import requests

bearer_token = "YOUR_BEARER_TOKEN"
headers = {"Authorization": f"Bearer {bearer_token}"}
search_url = "https://api.twitter.com/2/tweets/search/recent"

params = {
    'query': '(protein design OR protein engineering) (AI OR "artificial intelligence") has:links',
    'max_results': 100,
    'tweet.fields': 'created_at,text,entities'
}

response = requests.get(search_url, headers=headers, params=params)
data = response.json()
```

## API Usage Best Practices

### Rate Limiting
- Always respect API rate limits to avoid being blocked
- Implement exponential backoff for retries
- Use the built-in `RateLimiter` class from `utils.py`
- For Google Scholar: Use delays between requests to avoid CAPTCHAs
- For X API: Monitor rate limits and implement backoff strategies

### Error Handling
- Implement robust error handling for API failures
- Handle network timeouts gracefully
- Retry failed requests with increasing delays
- For Google Scholar: Handle CAPTCHA challenges appropriately
- For X API: Handle authentication errors and token expiration

### Data Processing
- Process API responses incrementally for large datasets
- Use pagination for large result sets
- Cache results when appropriate to reduce API calls
- For X API: Extract and validate URLs from tweets

### Authentication
- Most academic APIs don't require authentication
- If authentication is needed, store credentials securely
- Never hardcode API keys in source files
- For X API: Use environment variables or secure credential storage

### Google Scholar Specific
- **API Approaches:** Start with scholarly library for basic needs, consider SerpAPI for production
- **Browser Automation:** Use Selenium for full control and human-like interaction
- **CAPTCHA Handling:** Be prepared to solve CAPTCHAs manually when using browser automation
- **Rate Limiting:** Add delays between requests to avoid being blocked
- **Caching:** Implement caching to reduce repeated searches and avoid rate limits

### X (Twitter) Specific
- **API Approach:** Use official API for structured data and higher rate limits
- **Browser Automation:** Use Selenium if you don't have API access or need full web interface
- **Login Requirements:** Be prepared to login to your X account when using browser automation
- **Content Filtering:** Focus on tweets with links to papers or preprints
- **Search Operators:** Use advanced search operators to filter relevant content
- **Engagement Metrics:** Consider tweet engagement to identify important discussions
- **Terms of Service:** Respect X's terms of service for both API and web usage

### Browser Automation Best Practices

#### General Best Practices
- **User-Agent:** Set a realistic user-agent to avoid detection
- **Delays:** Add random delays between actions to mimic human behavior
- **Error Handling:** Implement robust error handling for UI changes and timeouts
- **Headless Mode:** Use headless mode for automated workflows (but may trigger more CAPTCHAs)
- **Session Management:** Maintain browser sessions to avoid repeated logins
- **Selector Flexibility:** Use multiple selectors for critical elements to handle UI changes
- **Resource Management:** Always quit the browser to free resources
- **Ethical Usage:** Use browser automation responsibly and respect website terms of service

#### Edge Browser Specific
- **EdgeDriver:** Download the correct version matching your Edge browser
- **Installation:** Add EdgeDriver to your system PATH
- **Performance:** Edge is generally faster and more memory-efficient than Chrome
- **Compatibility:** Better integration with Windows operating system
- **Sync:** Can use your existing Edge profile and bookmarks

#### Chrome Browser Specific
- **ChromeDriver:** Download the correct version matching your Chrome browser
- **Installation:** Add ChromeDriver to your system PATH
- **Compatibility:** More widely used and tested with Selenium
- **Extensions:** Supports a wide range of browser extensions
- **Cross-Platform:** Consistent behavior across Windows, macOS, and Linux

## Example API Calls

### PubMed Search Example
```python
import requests

url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
    'db': 'pubmed',
    'term': '"artificial intelligence"[Title/Abstract] AND "protein design"[Title/Abstract]',
    'retmax': '100',
    'retmode': 'xml',
    'sort': 'relevance'
}

response = requests.get(url, params=params)
# Parse XML response
```

### bioRxiv Search Example
```python
import requests

url = "https://api.biorxiv.org/papers/"
params = {
    'jcode': 'biorxiv',
    'limit': '100',
    'format': 'json',
    'subject_category': 'biophysics,molecular biology,structural biology',
    'date_from': '2024-01-01',
    'date_to': '2024-03-31'
}

response = requests.get(url, params=params)
data = response.json()
```

### arXiv Search Example
```python
import requests

url = "http://export.arxiv.org/api/query"
params = {
    'search_query': 'all:("protein design" AND "artificial intelligence")',
    'start': '0',
    'max_results': '100',
    'sortBy': 'relevance',
    'sortOrder': 'descending'
}

response = requests.get(url, params=params)
# Parse XML response
```
