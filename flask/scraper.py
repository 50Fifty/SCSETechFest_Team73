import pandas as pd 
from bs4 import BeautifulSoup 
from selenium.webdriver import Chrome
import re 
import time
import json
import math

path = "\jobstreet\chromedriver_win32"
driver = Chrome(executable_path=path)
base_url = "https://www.jobstreet.com.sg/en/job-search/{}-jobs/{}/"

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def get_page_number(keyword):
    #input: keyword for job_postings
    #output: number of pages

    url = base_url.format(keyword, 1)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #Finds the number of search results (Page and Total)
    result_text = soup.find("span",{"class": "sx2jih0 zcydq84u es8sxo0 es8sxo1 es8sxo21 _1d0g9qk4 es8sxo7"})
    
    #Splits the search results into a list
    results = result_text.text.split()
    
    #Replace comma from result and gets the total number of results returned
    result = int(result_text.text.split()[-2].replace(',', ''))
    
    #Gets the number of pages
    page_number = math.ceil(result/30)
    
    #Returns total number of pages
    return page_number

def job_page_scraper(link):

    url = "https://www.jobstreet.com.sg"+link
    print("scraping...", url)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    scripts = soup.find_all("script")

    for script in scripts:
        if script.contents:
            txt = script.contents[0].strip()
            if 'window.REDUX_STATE = ' in txt:
                jsonStr = script.contents[0].strip()
                jsonStr = jsonStr.split('window.REDUX_STATE = ')[1].strip()
                jsonStr = jsonStr.split('}}}};')[0].strip()
                jsonStr = jsonStr+"}}}}"
                jsonObj = json.loads(jsonStr)
    
    job = jsonObj['details']
    
    if(job['id']!=''):
        try:
            job_salary_min = job['header']['salary']['min']
            job_salary_max = job['header']['salary']['max']
            job_salary_currency = job['header']['salary']['currency']
        except Exception:
            job_salary_min =''
            job_salary_max = ''
            job_salary_currency = ''

        job_title = job['header']['jobTitle']
        company = job['header']['company']['name']
        job_post_date = job['header']['postedDate']
        job_internship = job['header']['isInternship']
        company_overview = job['companyDetail']['companyOverview']['html']
        company_overview = remove_html_tags(company_overview)
        job_description = job['jobDetail']['jobDescription']['html']
        #Remove html tags
        job_description = remove_html_tags(job_description)
        job_requirement_career_level = job['jobDetail']['jobRequirement']['careerLevel']
        job_requirement_yearsOfExperience = job['jobDetail']['jobRequirement']['yearsOfExperience']
        job_requirement_qualification = job['jobDetail']['jobRequirement']['qualification']
        job_employment_type = job['jobDetail']['jobRequirement']['employmentType']
        job_apply_url = job['applyUrl']['url']
        job_location = job['location'][0]['location']
        job_country = job['sourceCountry']

        return [job_title, job_salary_min, job_salary_max, job_salary_currency, company, job_post_date, job_internship, company_overview, job_description, job_requirement_career_level, job_requirement_yearsOfExperience, job_requirement_qualification, job_employment_type, job_apply_url, job_location, job_country]
    else:
        return []

def page_crawler(keyword):
    # input: keyword for job postings
    # output: dataframe of links scraped from each page

    # page number
    page_number = get_page_number(keyword)
    job_links = []

    for n in range(page_number):
        print('Loading page {} ...'.format(n+1))
        url = base_url.format(keyword, n+1)
        #Load URL
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    
        #extract all job links
        links = soup.find_all('a',{'rel':'nofollow noopener noreferrer'})
        job_links += links
 
    jobs = []

    for link in job_links:
        job_link = link['href'].strip().split('?', 1)[0]
        jobs.append(job_page_scraper(job_link))
    
    #Creates dataframe with jobs as values, and columns as column names
    result_df = pd.DataFrame(jobs, columns = ["job_title", "job_salary_min", "job_salary_max", "job_salary_currency", "company", "job_post_date", "job_internship", "company_overview", "job_description", "job_requirement_career_level", "job_requirement_yearsOfExperience", "job_requirement_qualification", "job_employment_type", "job_apply_url", "job_location", "job_country"])
    return result_df

# def main():

#     # a list of job roles to be crawled
#     key_words = ['frontend ux developer morgan']
#     dfs = []

#     for key in key_words:
#         key_df = page_crawler(key)
#         dfs.append(key_df)

#     # save scraped information as csv
#     pd.concat(dfs).to_csv("job_postings_results.csv")

# if __name__ == '__main__':
#     main()

#Request keyword
def scraper(search_term):
    key_words = [search_term]
    dfs = []

    for key in key_words:
        key_df = page_crawler(key)
        dfs.append(key_df)

    #Export as JSON
    #key_df.to_json('dataframe2.json', orient='records')

    #Get as dictionary
    key_df3 = key_df.to_json(orient='records')
    result_dict = json.loads(key_df3)
    return result_dict
    # result_dict[0]