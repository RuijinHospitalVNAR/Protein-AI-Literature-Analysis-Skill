#!/usr/bin/env python3
"""
Literature Retriever for Protein AI Literature Analysis

This script retrieves the latest papers on AI-driven protein design from multiple sources:
- PubMed (peer-reviewed papers)
- bioRxiv (biological sciences preprints)
- arXiv (computer science and quantitative biology preprints)

Usage:
    python literature_retriever.py --timeframe 3months --output data/papers.json
    python literature_retriever.py --timeframe 6months --categories "generative models" "reinforcement learning" --output data/custom_papers.json
"""

import argparse
import json
import time
import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

# Try to import Selenium for browser automation
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.edge.options import Options as EdgeOptions
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    selenium_available = True
    edge_available = True
except ImportError as e:
    selenium_available = False
    edge_available = False
    print(f"Selenium or webdriver-manager not available: {e}")
    print("Please install: pip install selenium webdriver-manager")

class LiteratureRetriever:
    def __init__(self, browser="edge"):
        self.pubmed_base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.biorxiv_base_url = "https://api.biorxiv.org/"
        self.arxiv_base_url = "http://export.arxiv.org/api/"
        self.google_scholar_url = "https://scholar.google.com/"
        self.twitter_api_url = "https://api.twitter.com/2/"
        self.papers = []
        self.browser = browser.lower()  # Default to Edge browser
    
    def get_date_range(self, timeframe):
        """Calculate date range based on timeframe"""
        end_date = datetime.now()
        if timeframe.endswith('months') or timeframe.endswith('month'):
            months = int(timeframe.split('month')[0])
            start_date = end_date - timedelta(days=months*30)
        elif timeframe.endswith('days') or timeframe.endswith('day'):
            days = int(timeframe.split('day')[0])
            start_date = end_date - timedelta(days=days)
        elif timeframe.endswith('years') or timeframe.endswith('year'):
            years = int(timeframe.split('year')[0])
            start_date = end_date - timedelta(days=years*365)
        else:
            raise ValueError("Invalid timeframe format. Use 'Xmonths', 'Xdays', or 'Xyears'")
        
        return start_date.strftime('%Y/%m/%d'), end_date.strftime('%Y/%m/%d')
    
    def _create_browser(self):
        """Create browser instance based on selected browser type"""
        if not selenium_available:
            return None
        
        try:
            if self.browser == "edge":
                if edge_available:
                    print(f"  Creating Edge browser instance...")
                    # For newer Selenium versions with webdriver-manager
                    options = EdgeOptions()
                    options.add_argument("--disable-gpu")
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-dev-shm-usage")
                    
                    # Use webdriver-manager to automatically download and manage EdgeDriver
                    try:
                        service = webdriver.edge.service.Service(EdgeChromiumDriverManager().install())
                        driver = webdriver.Edge(service=service, options=options)
                        print(f"  EdgeDriver automatically downloaded and configured")
                    except Exception as e:
                        print(f"  Error creating Edge driver: {e}")
                        print(f"  Please ensure webdriver-manager is installed: pip install webdriver-manager")
                        return None
                else:
                    print(f"  Edge browser not available, falling back to Chrome...")
                    self.browser = "chrome"
            
            if self.browser == "chrome":
                print(f"  Creating Chrome browser instance...")
                options = ChromeOptions()
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                
                try:
                    driver = webdriver.Chrome(options=options)
                except Exception as e:
                    print(f"  Error creating Chrome driver: {e}")
                    print(f"  Please download ChromeDriver and add to PATH")
                    print(f"  Download: https://chromedriver.chromium.org/downloads")
                    return None
            
            return driver
        except Exception as e:
            print(f"  Error creating browser: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def search_pubmed(self, start_date, end_date, max_results=100):
        """Search PubMed for relevant papers"""
        print("Searching PubMed...")
        
        # Build search term - expanded keywords for better coverage
        search_term = '''(("artificial intelligence"[Title/Abstract] OR "machine learning"[Title/Abstract] OR "deep learning"[Title/Abstract] OR "neural network"[Title/Abstract] OR "reinforcement learning"[Title/Abstract] OR "language model"[Title/Abstract] OR "generative model"[Title/Abstract] OR "diffusion model"[Title/Abstract] OR "transformer"[Title/Abstract]) AND ("protein design"[Title/Abstract] OR "protein engineering"[Title/Abstract] OR "directed evolution"[Title/Abstract] OR "de novo design"[Title/Abstract] OR "protein structure"[Title/Abstract] OR "protein folding"[Title/Abstract] OR "protein binder"[Title/Abstract] OR "antibody design"[Title/Abstract] OR "enzyme design"[Title/Abstract] OR "protein function"[Title/Abstract]))'''
        
        # First, get the total count
        esearch_url = f"{self.pubmed_base_url}esearch.fcgi"
        esearch_params = {
            'db': 'pubmed',
            'term': f'{search_term} AND ({start_date}:{end_date}[Date - Publication])',
            'retmax': str(max_results),
            'retmode': 'xml',
            'sort': 'relevance'
        }
        
        try:
            response = requests.get(esearch_url, params=esearch_params)
            response.raise_for_status()
            time.sleep(0.5)  # Respect rate limit
            
            # Parse XML response
            root = ET.fromstring(response.content)
            id_list = [id_elem.text for id_elem in root.findall('.//Id')]
            
            if not id_list:
                print("No PubMed papers found")
                return
            
            # Fetch details for each paper
            efetch_url = f"{self.pubmed_base_url}efetch.fcgi"
            efetch_params = {
                'db': 'pubmed',
                'id': ','.join(id_list),
                'retmode': 'xml',
                'rettype': 'abstract'
            }
            
            response = requests.get(efetch_url, params=efetch_params)
            response.raise_for_status()
            time.sleep(0.5)  # Respect rate limit
            
            # Parse detailed response
            root = ET.fromstring(response.content)
            
            for article in root.findall('.//PubmedArticle'):
                paper = {}
                
                # Title
                title_elem = article.find('.//ArticleTitle')
                paper['title'] = title_elem.text if title_elem is not None else ""
                
                # Authors
                authors = []
                for author in article.findall('.//Author'):
                    last_name = author.find('.//LastName')
                    initials = author.find('.//Initials')
                    if last_name is not None:
                        author_name = last_name.text
                        if initials is not None:
                            author_name += f" {initials.text}"
                        authors.append(author_name)
                paper['authors'] = authors
                
                # Journal
                journal_elem = article.find('.//Journal/Title')
                paper['journal'] = journal_elem.text if journal_elem is not None else ""
                
                # Publication date
                pub_date = article.find('.//PubDate')
                if pub_date is not None:
                    year = pub_date.find('Year')
                    month = pub_date.find('Month')
                    day = pub_date.find('Day')
                    date_parts = []
                    if year is not None:
                        date_parts.append(year.text)
                    if month is not None:
                        date_parts.append(month.text)
                    if day is not None:
                        date_parts.append(day.text)
                    paper['publication_date'] = '-'.join(date_parts) if date_parts else ""
                
                # Abstract
                abstract_elem = article.find('.//AbstractText')
                paper['abstract'] = abstract_elem.text if abstract_elem is not None else ""
                
                # DOI
                doi_elem = article.find('.//ELocationID[@EIdType="doi"]')
                paper['doi'] = doi_elem.text if doi_elem is not None else ""
                
                # URL
                if paper['doi']:
                    paper['url'] = f"https://doi.org/{paper['doi']}"
                else:
                    paper['url'] = ""
                
                # Source
                paper['source'] = 'PubMed'
                paper['type'] = 'peer-reviewed'
                
                if paper['title']:
                    self.papers.append(paper)
                    print(f"  + Added: {paper['title'][:100]}...")
        
        except Exception as e:
            print(f"Error searching PubMed: {e}")
    
    def search_biorxiv(self, start_date, end_date, max_results=100):
        """Search bioRxiv for relevant preprints"""
        print("\nSearching bioRxiv...")
        
        # Convert dates to YYYY-MM-DD format for bioRxiv API
        start_date_bio = start_date.replace('/', '-')
        end_date_bio = end_date.replace('/', '-')
        
        # Search bioRxiv using correct API endpoint
        # Format: https://api.biorxiv.org/details/biorxiv/[start_date]/[end_date]/[cursor]/[format]
        biorxiv_url = f"{self.biorxiv_base_url}details/biorxiv/{start_date_bio}/{end_date_bio}/0/json"
        
        try:
            response = requests.get(biorxiv_url)
            response.raise_for_status()
            time.sleep(0.1)  # Respect rate limit
            
            data = response.json()
            
            # Process papers from the collection
            collection = data.get('collection', [])
            if not collection:
                print("  No papers found in bioRxiv for the specified date range.")
                return
            
            for paper_data in collection[:max_results]:
                # Filter by relevant keywords in title or abstract - expanded keywords
                title = paper_data.get('title', '').lower()
                abstract = paper_data.get('abstract', '').lower()
                
                keywords = ['protein design', 'artificial intelligence', 'machine learning', 'deep learning', 
                           'neural network', 'reinforcement learning', 'language model', 'generative model',
                           'diffusion model', 'transformer', 'protein engineering', 'directed evolution',
                           'de novo design', 'protein structure', 'protein folding', 'protein binder',
                           'antibody design', 'enzyme design', 'protein function']
                
                if any(keyword in title or keyword in abstract for keyword in keywords):
                    # Parse authors
                    authors_str = paper_data.get('authors', '')
                    if authors_str:
                        authors = [author.strip() for author in authors_str.split(';')]
                    else:
                        authors = []
                    
                    paper = {
                        'title': paper_data.get('title', ''),
                        'authors': authors,
                        'journal': 'bioRxiv',
                        'publication_date': paper_data.get('date', ''),
                        'abstract': paper_data.get('abstract', ''),
                        'doi': paper_data.get('doi', ''),
                        'url': f"https://doi.org/{paper_data.get('doi', '')}" if paper_data.get('doi') else '',
                        'source': 'bioRxiv',
                        'type': 'preprint'
                    }
                    
                    self.papers.append(paper)
                    print(f"  + Added: {paper['title'][:100]}...")
            
            print(f"  Found {len([p for p in self.papers if p['source'] == 'bioRxiv'])} papers on bioRxiv")
        
        except Exception as e:
            print(f"Error searching bioRxiv: {e}")
    
    def search_arxiv(self, start_date, end_date, max_results=100):
        """Search arXiv for relevant preprints"""
        print("\nSearching arXiv...")
        
        # Build search query
        search_query = 'all:(("protein design" OR "protein engineering") AND ("artificial intelligence" OR "machine learning" OR "deep learning"))'
        
        # Convert dates to YYYYMMDD format
        start_date_arxiv = start_date.replace('/', '')
        end_date_arxiv = end_date.replace('/', '')
        
        # Search arXiv
        arxiv_url = f"{self.arxiv_base_url}query"
        params = {
            'search_query': search_query,
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        try:
            response = requests.get(arxiv_url, params=params)
            response.raise_for_status()
            time.sleep(3)  # Respect rate limit
            
            # Parse XML response
            root = ET.fromstring(response.content)
            
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                # Extract published date
                published = entry.find('{http://www.w3.org/2005/Atom}published').text
                pub_date = published.split('T')[0]  # YYYY-MM-DD format
                
                # Filter by date range
                if not (start_date <= pub_date.replace('-', '/') <= end_date):
                    continue
                
                # Title
                title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
                
                # Authors
                authors = []
                for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                    name = author.find('{http://www.w3.org/2005/Atom}name').text
                    authors.append(name)
                
                # Abstract
                abstract = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
                
                # DOI
                doi = ''
                for link in entry.findall('{http://www.w3.org/2005/Atom}link'):
                    if link.get('title') == 'doi':
                        doi = link.get('href').split('/')[-1]
                        break
                
                # URL
                url = ''
                for link in entry.findall('{http://www.w3.org/2005/Atom}link'):
                    if link.get('rel') == 'alternate':
                        url = link.get('href')
                        break
                
                paper = {
                    'title': title,
                    'authors': authors,
                    'journal': 'arXiv',
                    'publication_date': pub_date,
                    'abstract': abstract,
                    'doi': doi,
                    'url': url,
                    'source': 'arXiv',
                    'type': 'preprint'
                }
                
                self.papers.append(paper)
                print(f"  + Added: {paper['title'][:100]}...")
        
        except Exception as e:
            print(f"Error searching arXiv: {e}")
    
    def search_google_scholar(self, start_date, end_date, max_results=100):
        """Search Google Scholar for relevant papers using browser automation"""
        print("\nSearching Google Scholar...")
        
        # Note: Google Scholar doesn't have an official API
        # This implementation uses Selenium for browser automation
        
        try:
            if not selenium_available:
                print("  Selenium not available. Please install:")
                print("  1. pip install selenium")
                print("  2. Download ChromeDriver and add to PATH")
                print("  For ChromeDriver: https://chromedriver.chromium.org/downloads")
                return
            
            # Configure browser options
            if self.browser == "chrome":
                browser_options = ChromeOptions()
            else:
                browser_options = EdgeOptions()
            
            # Uncomment the next line to run in headless mode
            # browser_options.add_argument("--headless")
            browser_options.add_argument("--disable-gpu")
            browser_options.add_argument("--no-sandbox")
            browser_options.add_argument("--disable-dev-shm-usage")
            
            # Start browser
            print("  Starting browser...")
            driver = self._create_browser()
            
            if not driver:
                print("  Failed to create browser instance. Skipping Google Scholar search.")
                return
            
            try:
                # Navigate to Google Scholar
                driver.get("https://scholar.google.com/")
                time.sleep(2)
                
                # Build search query
                search_query = f"artificial intelligence protein design {start_date}..{end_date}"
                
                # Find search box and enter query
                search_box = driver.find_element(By.NAME, "q")
                search_box.send_keys(search_query)
                search_box.send_keys(Keys.RETURN)
                time.sleep(3)
                
                # Check for CAPTCHA
                if "CaptchaRedirect" in driver.current_url or "recaptcha" in driver.page_source:
                    print("  CAPTCHA challenge detected!")
                    print("  Please complete the CAPTCHA in the browser window.")
                    print("  Press Enter in the terminal after completing CAPTCHA...")
                    input()
                    time.sleep(3)
                
                # Extract results
                results = []
                page = 1
                
                while len(results) < max_results:
                    # Find result elements
                    result_elements = driver.find_elements(By.CSS_SELECTOR, "div.gs_r.gs_or.gs_scl")
                    
                    for result in result_elements:
                        if len(results) >= max_results:
                            break
                        
                        try:
                            # Extract title
                            title_elem = result.find_element(By.CSS_SELECTOR, "h3.gs_rt a")
                            title = title_elem.text
                            url = title_elem.get_attribute("href")
                            
                            # Extract authors, journal, etc.
                            info_elem = result.find_element(By.CSS_SELECTOR, "div.gs_a")
                            info = info_elem.text
                            
                            # Extract abstract
                            abstract_elem = result.find_element(By.CSS_SELECTOR, "div.gs_rs")
                            abstract = abstract_elem.text
                            
                            # Parse authors and journal from info
                            authors = []
                            journal = ""
                            pub_date = ""
                            
                            # Simple parsing - adjust as needed
                            if " - " in info:
                                parts = info.split(" - ")
                                if len(parts) >= 3:
                                    authors_part = parts[0]
                                    journal = parts[1]
                                    pub_date = parts[2].split(",")[0]
                                    
                                    # Parse authors
                                    authors = [author.strip() for author in authors_part.split(",")]
                            
                            # Create paper object
                            paper = {
                                'title': title,
                                'authors': authors,
                                'journal': journal,
                                'publication_date': pub_date,
                                'abstract': abstract,
                                'url': url,
                                'source': 'Google Scholar',
                                'type': 'scholarly_article'
                            }
                            
                            results.append(paper)
                            print(f"  + Added: {title[:100]}...")
                            
                        except Exception as e:
                            # Skip if we can't parse the result
                            continue
                    
                    # Try to go to next page
                    try:
                        next_button = driver.find_element(By.LINK_TEXT, "Next")
                        next_button.click()
                        time.sleep(3)
                        page += 1
                    except:
                        # No more pages
                        break
                
                # Add results to papers list
                self.papers.extend(results)
                print(f"  Found {len(results)} papers on Google Scholar")
                
            finally:
                # Close browser
                driver.quit()
                
        except Exception as e:
            print(f"Error searching Google Scholar: {e}")
            import traceback
            traceback.print_exc()
    
    def search_twitter(self, start_date, end_date, max_results=100):
        """Search X (Twitter) for relevant discussions and links using browser automation"""
        print("\nSearching X (Twitter)...")
        
        try:
            if not selenium_available:
                print("  Selenium not available. Please install:")
                print("  1. pip install selenium")
                print("  2. Download ChromeDriver and add to PATH")
                print("  For ChromeDriver: https://chromedriver.chromium.org/downloads")
                return
            
            # Configure browser options
            if self.browser == "chrome":
                browser_options = ChromeOptions()
            else:
                browser_options = EdgeOptions()
            
            # Uncomment the next line to run in headless mode
            # browser_options.add_argument("--headless")
            browser_options.add_argument("--disable-gpu")
            browser_options.add_argument("--no-sandbox")
            browser_options.add_argument("--disable-dev-shm-usage")
            
            # Start browser
            print("  Starting browser...")
            driver = self._create_browser()
            
            if not driver:
                print("  Failed to create browser instance. Skipping X (Twitter) search.")
                return
            
            try:
                # Navigate to X (Twitter)
                driver.get("https://x.com/search")
                time.sleep(2)
                
                # Build search query
                search_query = f"(protein design OR protein engineering) (AI OR 'artificial intelligence' OR 'machine learning') filter:links"
                
                # Find search box and enter query
                # Note: X's search UI may change, so selectors might need updating
                try:
                    # Try to find the search box
                    search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search']")
                except:
                    # Alternative selector
                    search_box = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Search query']")
                
                search_box.send_keys(search_query)
                search_box.send_keys(Keys.RETURN)
                time.sleep(3)
                
                # Check for login prompt
                if "login" in driver.current_url.lower() or "signin" in driver.current_url.lower():
                    print("  X requires login to view search results!")
                    print("  Please login to your X account in the browser window.")
                    print("  Press Enter in the terminal after logging in...")
                    input()
                    time.sleep(3)
                
                # Extract tweets
                tweets = []
                
                # Scroll to load more tweets
                last_height = driver.execute_script("return document.body.scrollHeight")
                
                while len(tweets) < max_results:
                    # Find tweet elements
                    tweet_elements = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")
                    
                    for tweet in tweet_elements:
                        if len(tweets) >= max_results:
                            break
                        
                        try:
                            # Extract text
                            text_elem = tweet.find_element(By.CSS_SELECTOR, "div[data-testid='tweetText']")
                            text = text_elem.text
                            
                            # Extract links
                            links = []
                            link_elements = tweet.find_elements(By.CSS_SELECTOR, "a[href]")
                            for link in link_elements:
                                href = link.get_attribute("href")
                                if href and not href.startswith("https://x.com"):
                                    links.append(href)
                            
                            # Extract date
                            date_elem = tweet.find_element(By.CSS_SELECTOR, "time")
                            date = date_elem.get_attribute("datetime")
                            if date:
                                date = date.split("T")[0]  # YYYY-MM-DD format
                            
                            # Extract user
                            user_elem = tweet.find_element(By.CSS_SELECTOR, "span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
                            user = user_elem.text
                            
                            # Create tweet object
                            tweet_obj = {
                                'text': text,
                                'links': links,
                                'date': date,
                                'user': user,
                                'source': 'X (Twitter)',
                                'type': 'social_media_post'
                            }
                            
                            # Only add if it has links
                            if links:
                                tweets.append(tweet_obj)
                                print(f"  + Added tweet from @{user} with {len(links)} link(s)")
                                
                        except Exception as e:
                            # Skip if we can't parse the tweet
                            continue
                    
                    # Scroll down to load more tweets
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    
                    # Check if we've reached the end
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                
                # Add tweet links to papers list
                for tweet in tweets:
                    for link in tweet['links']:
                        # Create a paper object for each link
                        paper = {
                            'title': f"Tweet discussion: {tweet['text'][:100]}...",
                            'authors': [tweet['user']],
                            'journal': 'X (Twitter)',
                            'publication_date': tweet['date'],
                            'abstract': tweet['text'],
                            'url': link,
                            'source': 'X (Twitter)',
                            'type': 'social_media_link'
                        }
                        
                        self.papers.append(paper)
                
                print(f"  Found {len(tweets)} relevant tweets with links")
                
            finally:
                # Close browser
                driver.quit()
                
        except Exception as e:
            print(f"Error searching X (Twitter): {e}")
            import traceback
            traceback.print_exc()
    
    def search_openalex(self, start_date, end_date, max_results=100):
        """Search OpenAlex for relevant papers"""
        print("\nSearching OpenAlex...")
        
        # OpenAlex API endpoint
        base_url = "https://api.openalex.org/works"
        
        # Search query - AI & protein design
        query = "artificial intelligence protein design"
        
        # Build API URL - use year-based filter instead of date-based filter
        # Extract year from dates
        start_year = start_date.split('/')[0]
        end_year = end_date.split('/')[0]
        
        params = {
            "search": query,
            "filter": f"publication_year:{start_year}",
            "sort": "publication_date:desc",
            "per_page": 100,
            "api_key": "FpssNE9d5DnuruuzYviWgS"
        }
        
        try:
            print(f"  API URL: {base_url}")
            print(f"  Search query: {query}")
            print(f"  Year filter: {start_year}")
            
            response = requests.get(base_url, params=params, timeout=30)
            print(f"  API Response Status: {response.status_code}")
            
            response.raise_for_status()
            
            data = response.json()
            print(f"  API Response - Total results: {data.get('meta', {}).get('count', 0)}")
            print(f"  API Response - Results per page: {data.get('meta', {}).get('per_page', 0)}")
            
            works = data.get('results', [])
            print(f"  Number of results in current page: {len(works)}")
            
            for work in works:
                doi = work.get('doi', '')
                if doi:
                    doi = doi.replace('https://doi.org/', '')
                
                paper = {
                    "title": work.get('title', ''),
                    "authors": [author.get('author', {}).get('display_name', '') for author in work.get('authorships', [])],
                    "journal": work.get('primary_location', {}).get('source', {}).get('display_name', ''),
                    "publication_date": work.get('publication_date', ''),
                    "abstract": work.get('abstract', ''),
                    "doi": doi,
                    "url": work.get('doi', '') or work.get('id', ''),
                    "source": "OpenAlex",
                    "type": "peer-reviewed" if work.get('type') == 'article' else 'preprint'
                }
                
                if paper['title']:
                    self.papers.append(paper)
                    print(f"  + Added: {paper['title'][:100]}...")
            
            print(f"  Found {len(works)} papers on OpenAlex")
            
        except Exception as e:
            print(f"Error searching OpenAlex: {e}")
            import traceback
            traceback.print_exc()
    
    def run(self, timeframe, output_file):
        """Run the full retrieval process"""
        print(f"Starting literature retrieval for timeframe: {timeframe}")
        
        # Calculate date range
        start_date, end_date = self.get_date_range(timeframe)
        print(f"Date range: {start_date} to {end_date}")
        
        # Search all sources
        self.search_pubmed(start_date, end_date)
        self.search_biorxiv(start_date, end_date)
        self.search_arxiv(start_date, end_date)
        self.search_openalex(start_date, end_date)
        # self.search_google_scholar(start_date, end_date)
        # self.search_twitter(start_date, end_date)
        
        # Remove duplicates within current run
        seen_titles = set()
        unique_papers = []
        for paper in self.papers:
            title = paper['title'].lower()
            if title not in seen_titles:
                seen_titles.add(title)
                unique_papers.append(paper)
        
        # Read existing papers if file exists
        existing_papers = []
        import os
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_papers = json.load(f)
                print(f"Loaded {len(existing_papers)} existing papers")
            except Exception as e:
                print(f"Error reading existing papers: {e}")
        
        # Merge with existing papers and remove duplicates
        all_papers = existing_papers + unique_papers
        merged_seen_titles = set()
        merged_unique_papers = []
        for paper in all_papers:
            title = paper['title'].lower()
            if title not in merged_seen_titles:
                merged_seen_titles.add(title)
                merged_unique_papers.append(paper)
        
        # Save results
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_unique_papers, f, indent=2, ensure_ascii=False)
        
        print(f"\nTotal papers retrieved in current run: {len(unique_papers)}")
        print(f"Total unique papers after merging: {len(merged_unique_papers)}")
        print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve AI & protein design literature")
    parser.add_argument('--timeframe', default='3months', help='Timeframe for search (e.g., 3months, 1year)')
    parser.add_argument('--output', default='data/papers.json', help='Output file path')
    parser.add_argument('--categories', nargs='*', help='Specific research categories to focus on')
    parser.add_argument('--browser', default='edge', choices=['edge', 'chrome'], help='Browser to use for web scraping (default: edge)')
    
    args = parser.parse_args()
    
    # Create LiteratureRetriever instance
    retriever = LiteratureRetriever(browser=args.browser)
    retriever.run(args.timeframe, args.output)
