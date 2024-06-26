import requests
from bs4 import BeautifulSoup

url = 'https://verafiles.org/articles/when-sara-militarized-the-deped'
response = requests.get(url)

if response.status_code == 200:
    print('Successfully retrieved the webpage \n')
else:
    print('Failed to retrieve the webpage', response.status_code)
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

title = soup.find('h1', class_='article_title heading-size-1')
if title:
    print('Title:\n')
    print(title.text.strip())
else:
    print('No title found.')

# Find and extract the article content
content = soup.find('div', class_='entry-content')
if content:
    print('\nContent:\n')
    print(content.text.strip())
else:
    print('No content found.')

