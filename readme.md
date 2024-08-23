# Multi Domain Web Crawler
- It is a web crawler developed using scrapy and python. A user can give multiple domains and the domain_patters regex to crawl different pages of a website. 

# Functionality
- A user can provide the start_urls or domains in the start_url array in the script. 
- Also the user can specify the domain_patterns which the user want's to crawl. 
- Once the data is crawled, it is written in a json format in a json file.

# Tech Stack Used
- scrapy
- python

# Steps to Run the Program
- First of all please setup the required tools and libraries. 
- Setup vs code, and install all the python extensions required for basic python programming. 
- Download and install python from the official python website. 
- Setup the paths if required according to you OS. 
- Navigate to the multiDomainCrawler.py file and run the below command
 - scrapy crawl multi_domain_spider
- That's all your crawled data would be present in a output file starting with the domain name. 

# Future Scope of this Project
- We can even integrate a data store like mongoDB to save the crawled data for future use. 
- We can even send this crawled data to some metabase pipelines using event streaming platforms like kafka. 

# Note**
- This script is only handling the saving of json data for [bookstoscrap.com](https://books.toscrape.com/)
- If you want to handle proper saving of data you need to write if else conditions for the same based on your domain name. 

