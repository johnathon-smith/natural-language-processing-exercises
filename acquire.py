import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from request import get
import os

#Since these blog articles will have similar structure, create a function that loops through
#Each url and grabs the appropriate info
def get_blog_articles(refresh = False):
    """
    This function uses a list of urls for Codeup blog articles. It will loop through each
    of them, gather the article title and content, put it into a dictionary, and finally
    return the list of dictionaries.

    This function will cache the results and load those results in future function calls. However,
    there will be a kwa that allows the user to specify whether or not to get fresh information.
    """
    
    filename = 'codeup_blog_posts.csv'

    #Check for 'codeup_blog_posts.csv'
    if os.path.is_file(filename) && refresh == False:
        return pd.read_csv(filename)
    else:
        #Create the list of urls
        urls = ['https://codeup.com/data-science/codeups-data-science-career-accelerator-is-here/',
                'https://codeup.com/data-science/data-science-myths/',
                'https://codeup.com/data-science/data-science-vs-data-analytics-whats-the-difference/',
                'https://codeup.com/data-science/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
                'https://codeup.com/data-science/competitor-bootcamps-are-closing-is-the-model-in-danger/'
            ]

        #Create the empty list to append the article dicts to
        articles = []
        
        for url in urls:
            response = get(url, headers = {'user-agent':'Codeup DS Germain'})
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            article = {
                'title': soup.find('h1', class_ = 'entry-title').text,
                'date': soup.find('span', class_ = 'published').text,
                'category': soup.find('a', rel = 'category tag').text,
                'content': soup.find('div', class_ = 'et_pb_post_content').text.strip().replace('\n', ' ').replace('\xa0', ' ')
            }
            
            articles.append(article)
            
        #Convert the list to dataframe.
        articles = pd.DataFrame(articles)

        #Cache the newly acquired df
        articles.to_csv(filename, index = False)
        
        return articles

#Now build a function to get the data from the entire page
def get_page_data(category):
    """
    This function takes in a category as a string, builds the proper url, collects the data for each article and adds it to a list of dictionaries,
    and finally returns the list of dictionaries.
    """
    #Build the url
    url = 'https://inshorts.com/en/read/' + category
    
    #Get the html
    response = get(url, headers = {'user-agent':'Codeup DS Germain'})
    soup = BeautifulSoup(response.content, 'html.parser')
    
    #Access the news_stack that contains the articles
    news_stack = soup.find('div', class_ = 'card-stack')
    
    #Access the articles inside the news_stack
    articles = news_stack.find_all('div', class_ = 'news-card')
    
    #Create an empty list to store the article info
    article_info = []
    
    #Loop through each article and gather the info
    for article in articles:
        article_dict = {
            'title': article.find('span', itemprop = 'headline').text,
            'author': article.find('span', class_ = 'author').text,
            'date': article.find('span', clas = 'date').text.split(',')[0],
            'category': category,
            'content': article.find('div', itemprop = 'articleBody').text
        }
        
        article_info.append(article_dict)
        
    return article_info

def get_news_articles(categories = ['business', 'sports', 'technology', 'entertainment'], refresh = False):
    """
    This function takes in a list of categories. It will loop through the list, gather the article
    info from each category, add it to a list of dicts, and return a list of dictionaries of all
    articles in those categories.

    This function will cache the results and load those results in future function calls. However,
    there will be a kwa that allows the user to specify whether or not to get fresh information.
    """

    filename = 'news_articles.csv'

    #Check for 'news_articles.csv'
    if os.path.isfile(filename) && refresh == False:
        return pd.read_csv(filename)
    else:
        #First, create the empty list of article dicts
        article_info = []
        
        #Loop through the list of cats
        for cat in categories:
            article_list = get_page_data(cat)
            
            #Loop through the list and append each entry individually to article_info
            for article in article_list:
                article_info.append(article)

        #Cache the newly acquired df
        article_info = pd.DataFrame(article_info)

        article_info.to_csv(filename, index = False)
        
        return article_info
    