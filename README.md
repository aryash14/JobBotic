## Introduction

Imagine if you could automate your job search, saving you valuable time spent browsing for your ideal job. With the power of Metaphor and OpenAI's API, this project makes it possible by generating a list of relevant job listings sourced from LinkedIn.

You simply provide a descriptive query, such as job title, location, or experience level, and the rest is automated! You'll receive a comprehensive list of jobs that match your criteria. But that's not all – we go a step further. Ever wondered how challenging a particular job might be in terms of qualifications required, such as education level and years of experience? Using generative AI, we assign a rating to each job on a scale of 0 to 10, along with an explanation. This rating can help you filter and prioritize job listings based on your qualifications.

## Features

The end result includes the following details for each job listing:

1. Job Title
2. Company
3. Location
4. Job Description
5. Link to the Job
6. Rating (0 - 10)
7. Reasoning for Rating

## Getting Started

To run the program, follow these steps:

1. Execute `python3 main.py` in your terminal.
2. Send a POST request to `http://0.0.0.0:8080/job_search` using a tool like Postman to retrieve the results.

## Current Issues

Please note the following issues with the current implementation:

- Only results from LinkedIn are returned, as there is a web scraping element specific to LinkedIn.
- The runtime is not optimized, with an average processing time of approximately 2 minutes and 43 seconds. This delay is primarily due to the job difficulty rating generation process.
