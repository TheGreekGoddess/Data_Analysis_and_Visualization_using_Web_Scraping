#!/usr/bin/env python
# coding: utf-8

# ## Initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter

# In[1]:


# Import dependencies and setup
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
import time

# ### 1. Scrape the NASA Mars News Website

# In[2]:


# Set the executable path and initialize the Chrome browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless = False)


# In[3]:


# Visit the NASA Mars news website
news_url = "https://mars.nasa.gov/news/"
browser.visit(news_url)

# Time delay of one second to ensure the browser loads
time.sleep(1)


# In[4]:


# Set-up Browser
html = browser.html

# Create a BeautifulSoup object and parse the HTML results
news_soup = bs(html, "html.parser")
slide_element = news_soup.select_one("ul.item_list li.slide")
slide_element.find("div", class_="content_title")


# In[5]:


# Scrape the latest News title
# Use Parent Element to Find First <a> Tag and Save it as news_title
news_title = slide_element.find("div", class_="content_title").get_text()
print(news_title)


# In[6]:


# Scrape the corresponding paragraph text
news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
print(news_paragraph)


# In[7]:


# Close the browser
browser.quit()


# ### 2. Scrape the Nasa JPL (Jet Propulsion Laboratory) Website for Mars Space Images

# In[8]:


# Set the executable path and initialize the Chrome browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless = False)


# In[9]:


# Visit the NASA JPL website
jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(jpl_url)

# Time delay of one second to ensure the browser loads
time.sleep(1)


# In[10]:


# Use Splinter to visit the website and click the "Full Image" button
full_image_button = browser.find_by_id("full_image")
full_image_button.click()


# In[11]:


# Locate the "More Info" button and click it
browser.is_element_present_by_text("more info", wait_time = 1)
more_info_element = browser.links.find_by_partial_text("more info")
more_info_element.click()


# In[12]:


# Set-up Browser
html = browser.html

# Create a BeautifulSoup object and parse the HTML results
image_soup = bs(html, "html.parser")
img_url = image_soup.select_one("figure.lede a img").get("src")

# Use Base URL to create an absolute URL
img_url = f"https://www.jpl.nasa.gov{img_url}"
print(img_url)


# In[13]:


# Close the browser
browser.quit()


# ### 3. Scrape the Mars Weather from Twitter for user handle @MarsWxReport

# In[14]:


# Set the executable path and initialize the Chrome browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless = False)


# In[15]:


# Visit the Mars Weather Twitter Account
twitter_url = "https://twitter.com/marswxreport?lang=en"
browser.visit(twitter_url)

# Time delay of one second to ensure the browser loads
time.sleep(1)


# In[16]:


# Set-up Browser
html = browser.html
# browser.links.find_by_partial_text('Next')

# Create a BeautifulSoup object and parse the HTML results 
weather_soup = bs(html, "html.parser")


# In[17]:


# Retrieve the latest Mars weather tweet
mars_weather_tweet =  weather_soup.find('div',attrs={"data-testid":"tweet"}).text

# Use .strip to take off the preceeding text extracted to only print the tweet text
mars_weather = mars_weather_tweet.strip().replace("Mars Weather@MarsWxReport·","")
print(mars_weather)


# In[18]:


# Close the browser
browser.quit()


# ### 4. Scrape the Space Facts Website for Mars Facts

# In[19]:


# Visit the Mars Facts Site Using Pandas to Read
mars_df = pd.read_html("https://space-facts.com/mars/")[0]
print(mars_df)


# In[20]:


# Rename the DataFrame columns and set index
mars_df.columns=["Description", "Value"]
mars_df.set_index("Description", inplace = True)
mars_df


# ### 5. Scrape the USGS Astrogeology Website for high resolution images for each of Mar's hemispheres

# In[21]:


# Set the executable path and initialize the Chrome browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless = False)


# In[22]:


# Visit the USGS Astrogeology Science Center website
usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(usgs_url)

# Time delay of one second to ensure the browser loads
time.sleep(1)


# In[23]:


hemisphere_image_urls = []

# Create a loop to retrieve each of Mars's hemispheres
links = browser.find_by_css("a.product-item h3")
for item in range(len(links)):
    hemisphere = {}
    
    # Retrieve elements as each loop processes
    browser.find_by_css("a.product-item h3")[item].click()
    sample_element = browser.links.find_by_text("Sample").first
    hemisphere["img_url"] = sample_element["href"]
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    # Append each hemisphere object to the list
    hemisphere_image_urls.append(hemisphere)
    
    # Use browser.back to move back one page in the current session history
    browser.back()

# Print the results
hemisphere_image_urls


# In[24]:


# Close the browser
browser.quit()


# ## End of Jupyter Notebook
