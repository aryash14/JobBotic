# %%
import requests
from bs4 import BeautifulSoup
import json
import openai
import os
from tqdm import tqdm
# %%

#getting the API key
openai.api_key  = os.getenv('OpenAI_API_Key')

#function calling OpenAI's modek
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    text = response.choices[0].message["content"]
    data = json.loads(text)
    return data

#function for webcrawling
#currently is formated for LinkedIn
def get_information(url):
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        # Find the job listings container element
        job_listings_container = soup.find('ul', class_='jobs-search__results-list')
        # print(job_listings_container)
        if job_listings_container:
            # Initialize a list to store job listings
            job_listings = []

            # Iterate through each job listing in the container
            for job in tqdm(job_listings_container.find_all('li')):
                # Extract job details
                job_title = job.find('h3', class_='base-search-card__title').get_text(strip=True)
                company_name = job.find('a', class_='hidden-nested-link').get_text(strip=True)
                location = job.find('span', class_='job-search-card__location').get_text(strip=True)
                job_link = job.find('a', class_ = "base-card__full-link").get('href')

                job_description_response = requests.get(job_link)
                if job_description_response.status_code == 200:
                    # Parse the job listing page's HTML content
                    job_description_soup = BeautifulSoup(job_description_response.text, 'html.parser')

                    # Find the job description element
                    job_description_element = job_description_soup.find('div', class_='show-more-less-html__markup')

                    # Extract the job description
                    job_description = job_description_element.get_text() if job_description_element else "Description not found"
                
                    prompt = f"""
                            You are a rating chatbot. Your job is to look at job descriptions and rate their difficulty out of 10. 
                            Provide a 3 to 5 sentence reasoning for the rating. 
                            A 0 indicates that this job is fairly easy, and a 10 indicates this job is complex and has a lot of qualification factors. 
                            You will return the output in a JSON format with the following keys: Rating, Reasoning
                            {{
                                "Rating": "value1",
                                "Reasoning": "value2"
                            }}
                            Job Description: {job_description}
                        """
                    #get job rating and reasoning using the gpt model
                    res = get_completion(prompt)

                    # Store job details in a dictionary
                    job_details = {
                        'job_title': job_title,
                        'company_name': company_name,
                        'location': location,
                        'job_link': job_link,
                        'job_description': job_description,
                        'rating' :res["Rating"],
                        'reasoning' :res["Reasoning"]
                    }

                    # Append the job details to the list
                    job_listings.append(job_details)
    

            # Convert the list of job listings to JSON
            job_listings_json = json.dumps(job_listings, indent=4)
            return job_listings
        else:
            print("No job listings found on the page.")
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)
    return []



