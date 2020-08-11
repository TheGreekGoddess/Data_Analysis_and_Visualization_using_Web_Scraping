# Import dependencies and setup
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
import time
import datetime as dt

# Set the executable path and initialize the Chrome browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless = False)

### 1. Scrape the NASA Mars News Website
def mars_news(browser):
    
    # Visit the NASA Mars news website
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    # Retrieve intial list item
    browser.is_element_present_by_css("ul.item_list li.slide")

    # Time delay of one second to ensure the browser loads
    time.sleep(1)
    
    # Set-up Browser
    html = browser.html

    # Create a BeautifulSoup object and parse the HTML results
    news_soup = bs(html, "html.parser")

    # Retrieve all elements
    try:
        slide_element = news_soup.select_one("ul.item_list li.slide")
        slide_element.find("div", class_ = "content_title")

        # Scrape the latest News title
        # Use Parent Element to Find First <a> Tag and Save it as news_title
        news_title = slide_element.find("div", class_ = "content_title").get_text()
        print(news_title)

        # Scrape the corresponding paragraph text
        news_paragraph = slide_element.find("div", class_ = "article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_paragraph


### 2. Scrape the Nasa JPL (Jet Propulsion Laboratory) Website for Mars Space Images
def featured_image(browser):
    # Visit the NASA JPL website
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Use Splinter to visit the website and click the "Full Image" button
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    # Locate the "More Info" button and click it
    browser.is_element_present_by_text("more info", wait_time = 1)
    more_info_element = browser.links.find_by_partial_text("more info")
    more_info_element.click()

    # Set-up Browser
    html = browser.html

    # Create a BeautifulSoup object and parse the HTML results
    image_soup = bs(html, "html.parser")

    try:
        img_url = image_soup.select_one("figure.lede a img").get("src")
    except AttributeError:
        return None

    # Use Base URL to create an absolute URL
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    return img_url


### 3. Scrape the Mars Weather from Twitter for user handle @MarsWxReport
def twitter_weather(browser):
    # Visit the Mars Weather Twitter Account
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    browser.links.find_by_partial_text('Next')

    # Set-up Browser
    html = browser.html

    # Create a BeautifulSoup object and parse the HTML results 
    weather_soup = bs(html, "html.parser")

    # Retrieve the latest Mars weather tweet
    mars_weather_tweet = weather_soup.find('div',attrs={"data-testid":"tweet"}).text

    # Use .strip to take off the preceeding text extracted to only print the tweet text
    mars_weather = mars_weather_tweet.strip().replace("Mars Weather@MarsWxReport·Aug 9InSight ","")
    return mars_weather


### 4. Scrape the Space Facts Website for Mars Facts
def mars_facts():
    # Visit the Mars Facts Site Using Pandas to Read
    try:
        mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None

    # Rename the DataFrame columns and set index
    mars_df.columns = ["Description", "Value"]
    mars_df.set_index("Description", inplace = True)
    return mars_df.to_html(classes = "table table-striped")


### 5. Scrape the USGS Astrogeology Website for high resolution images for each of Mar's hemispheres
def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center website
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)

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
    return hemisphere_image_urls


def scrape_all():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless = False)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    return data

# Close the browser
browser.quit()