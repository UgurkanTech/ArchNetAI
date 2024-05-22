import urllib.request
import re
import html
import socket
from urllib.parse import unquote

class HTMLCleaner:
    def __init__(self):
        pass

    def clean(html_content):
        body = re.search('<body.*?>(.*)</body>', html_content, re.DOTALL)
        if body:
            body_content = body.group(1)
            # Remove script tags and their content
            body_content = re.sub('<script.*?>.*?</script>', '', body_content, flags=re.DOTALL)
            # Remove HTML comments
            body_content = re.sub('<!--.*?-->', '', body_content, flags=re.DOTALL)
            # Remove CSS styles
            body_content = re.sub('<style.*?>.*?</style>', '', body_content, flags=re.DOTALL)
            # Remove <ol class="references"> sections
            body_content = re.sub('<ol class="references">.*?</ol>', '', body_content, flags=re.DOTALL)
            body_content = re.sub('<div class="ref.*?</div>', '', body_content, flags=re.DOTALL)
            # Remove <li class="interlanguage-link sections
            body_content = re.sub('<li class="interlanguage-link.*?</li>', '', body_content)
            # Remove li with id pt-*
            body_content = re.sub('<li id="pt-.*?</li>', '', body_content)
            # Remove vector-menus
            body_content = re.sub('<div class="vector-menu.*?</div>', '', body_content, flags=re.DOTALL)
            # Remove data-* attributes
            body_content = re.sub('data-.*?=".*?"', '', body_content)
            # Remove hyperlinks
            body_content = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', body_content)
            # Remove input fields
            body_content = re.sub('<input.*?>', '', body_content, flags=re.DOTALL)
            # Remove navigation menus
            body_content = re.sub('<nav.*?>.*?</nav>', '', body_content, flags=re.DOTALL)
            # Remove footers
            body_content = re.sub('<footer.*?>.*</footer>', '', body_content, flags=re.DOTALL)
            body_content = re.sub('<ul id="footer.*?>.*</ul>', '', body_content, flags=re.DOTALL)
            body_content = re.sub('<div id="footer.*?>.*</div>', '', body_content, flags=re.DOTALL)
            body_content = re.sub('<li id="footer.*?>.*</li>', '', body_content, flags=re.DOTALL)
            body_content = re.sub('<div class="printfooter.*?>.*</div>', '', body_content, flags=re.DOTALL)
            body_content = re.sub('<div id="catlinks.*?>.*</div>', '', body_content, flags=re.DOTALL)
            body_content = re.sub('<div class="catlinks.*?>.*</div>', '', body_content, flags=re.DOTALL)
            # Remove navigation menus
            body_content = re.sub('<div role="nav.*?>.*</div>', '', body_content, flags=re.DOTALL)
            body_content = re.sub('<div class="nav.*?>.*</div>', '', body_content, flags=re.DOTALL)
            # Remove remaining HTML tags, but not their content - Last step
            body_content = re.sub('<[^<]+?>', '', body_content)

            # Remove empty lines
            body_content = re.sub(r'\n\s*\n', '\n', body_content)
            # Replace new lines with spaces
            body_content = re.sub('\n', ' ', body_content)
            # Replace tabs with a single space
            body_content = re.sub('\t', ' ', body_content)
            # Replace multiple spaces with a single space
            body_content = re.sub(' +', ' ', body_content)
            # Convert HTML entities to regular characters
            body_content = html.unescape(body_content)
            
            #cleanup unescaped HTML entities
            body_content = re.sub('&#;', '', body_content)
            body_content = re.sub(r'\[\d+\]', '', body_content)
            body_content = re.sub(r'\[edit\]', '', body_content)

            return body_content
        else:
            return None
            
    def clean_google_search(html_content):
        body = re.search('<body.*?>(.*)</body>', html_content, re.DOTALL)
        if body:
            result = body.group(1) 
            link_matches = re.findall(r'<a href="(/url\?.*?)"', result)
            urls = []
            domains = []
            for link in link_matches:
                parts = link.split('url=')
                if len(parts) > 1:
                    url = parts[1]
                    url = re.sub(r'&amp;ved=.*?&amp;usg=.*$', '', url)
                    url = unquote(unquote(url))
                    if not re.search(r'google\.com', url) and not re.search(r'youtube\.com', url) and not re.search(r'gstatic\.com', url)  and url.startswith('http'):
                        domain = re.search(r'https?://(.*?)/', url).group(1)
                        parts = domain.split('.')
                        if len(parts) > 2:
                            domain = '.'.join(parts[-2:])
                        if domain not in domains:
                            urls.append(url)
                            domains.append(domain)
                   
            return urls
        
class WebScraper:
    def __init__(self) -> None:
        pass

    def fetch_url(self, url: str) -> str:

        print("\nFetching URL: " + url + "\n")

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3 Edge/12.246',
                'Accept': 'text/html ',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.google.com/'
            }
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, timeout=10)
            html_content = response.read().decode(errors='ignore')
        except (urllib.error.URLError, socket.timeout) as e:
            print(f"Error fetching URL: {e}")
            return None
        
        context = HTMLCleaner.clean(html_content)

        return context
    
    def fetch_google_search(self, query: str) -> str:
        query = query.replace(' ', '+')
        url = f"https://www.google.com/search?q={query}&num=3&hl=en&sa=N&filter=1&lr=lang_en"
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3 Edge/12.246',
                'Accept': 'text/html',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.google.com/'
            }
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, timeout=10)
            html_content = response.read().decode(errors='ignore')
        except (urllib.error.URLError, socket.timeout) as e:
            print(f"Error fetching URL: {e}")
            return None

        context = HTMLCleaner.clean_google_search(html_content)

        return context