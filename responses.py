import random
import requests
import pyjokes
from bs4 import BeautifulSoup
from datetime import datetime


def get_tech_news():       # This function is responsible for fetching the latest tech news links from a specified URL
    url = 'https://news.ycombinator.com/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    links = soup.select('.titleline > a')[0:5]  # Find all the <a> tags that contain the article titles and links

    news_links = []
    for idx, item in enumerate(links):
        title = links[idx].getText()  # Extract the text of the article title
        href = links[idx].get('href', None)  # Extract the URL link of the article, None in case there is no link.
        news_links.append({'title': title, 'link': href})
    return news_links


def get_response(message):       # Function takes a message as input and returns a response based on the content.
    user_message = message.lower()

    if user_message == 'hello':
        return 'Hi there! How can I assist you?'

    if user_message == 'whats new':
        links = get_tech_news()  # Fetch the latest news links
        if len(links) > 0:
            return format_news_links(links)
        else:
            return 'Sorry, there are no new articles at the moment. Please try again later.'

    if user_message == 'roll':
        return f"The dice rolled and you got {random.randint(1, 6)}!"

    if user_message == 'help':
        return '''Here are some available commands:
- hello: Greet the bot.
- whats new: Get the latest tech news.
- roll: Roll a dice and get a random number from 1 to 6.
- !help: Display the list of available commands.'''

    if user_message == 'about':
        return 'I am a Discord bot designed to provide tech news updates and basic functionality.'

    if user_message == 'goodbye':
        return 'Goodbye! Have a great day!'

    if user_message == 'time':
        current_time = datetime.now().strftime('%H:%M:%S')
        return f'The current time is {current_time}.'

    if user_message == 'date':
        current_date = datetime.now().strftime('%Y-%m-%d')
        return f'The current date is {current_date}.'

    if user_message == 'tell me a funny joke':
        joke = pyjokes.get_joke()
        return joke

    return "I'm sorry, I couldn't understand your message. Please try again or type '!help' for assistance."


# The below function extracts the title and link from each article dictionary and combines them into a formatted string
# Where each line contains the title of an article followed by the corresponding link.


def format_news_links(links):
    formatted_links = ""
    for article in links:
        title = article['title']
        link = article['link']
        formatted_links += f"{title}: {link}\n"    # The \n adds a newline character to separate each article.
    return formatted_links

