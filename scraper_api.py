import requests
import pandas as pd
import json
from bs4 import BeautifulSoup

def scrape_remotive(keyword="python"):
    """Scrapes Remotive jobs using their public API based on a search keyword."""
    api_url = "https://remotive.com/api/remote-jobs"
    params = {"search": keyword}
    headers = {"User-Agent": "Manus AI Agent for Job Scraping Task"}

    print(f"Attempting to fetch jobs from Remotive API for keyword: 	{keyword}")

    try:
        res = requests.get(api_url, params=params, headers=headers, timeout=20)
        res.raise_for_status()

        if "application/json" not in res.headers.get("Content-Type", ""):
            print(f"Error: Expected JSON response, but got {res.headers.get('Content-Type', '')}")
            print(f"Response text: {res.text[:500]}...")
            return []

        data = res.json()

        if "jobs" not in data:
            print("Error: \'jobs\' key not found in API response.")
            print(f"API Response: {json.dumps(data, indent=2)}")
            return []

        api_jobs = data["jobs"]
        print(f"Found {len(api_jobs)} jobs via API for keyword 	{keyword}")

        jobs = []
        for job_data in api_jobs:
            description_html = job_data.get("description", "")
            soup = BeautifulSoup(description_html, "html.parser")
            description_text = soup.get_text(separator="\n", strip=True)

            jobs.append({
                "title": job_data.get("title", "N/A"),
                "company": job_data.get("company_name", "N/A"),
                "location": job_data.get("candidate_required_location", "N/A"),
                "date": job_data.get("publication_date", "N/A"),
                "url": job_data.get("url", "N/A"),
                "job_type": job_data.get("job_type", "N/A"),
                "salary": job_data.get("salary", "N/A"),
                "source": "Remotive API"
            })

        print(f"Successfully processed {len(jobs)} jobs from API response.")
        return jobs

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error fetching Remotive jobs via API: {e}")
        print(f"Response Status Code: {e.response.status_code}")
        print(f"Response Text: {e.response.text[:500]}...")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching Remotive jobs via API: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from API: {e}")
        print(f"Response text: {res.text[:500]}...")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during API scraping: {e}")
        return []

def save_to_csv(jobs, filename="jobs.csv"):
    """Saves a list of job dictionaries to a CSV file."""
    if not jobs:
        print("No jobs to save.")
        return
    try:
        df = pd.DataFrame(jobs)
        expected_cols = [
            "title", "company", "location", "date", "job_type",
            "salary", "url", "source"
        ]
        for col in expected_cols:
            if col not in df.columns:
                df[col] = "N/A"
        df = df[expected_cols]

        df.to_csv(filename, index=False)
        print(f"[✓] Saved {len(df)} job listings to {filename}")
    except Exception as e:
        print(f"Error saving jobs to CSV: {e}")

if __name__ == "__main__":
    test_keyword = "python developer"
    print(f"--- Testing API scraper with keyword: {test_keyword} ---")
    scraped_jobs = scrape_remotive(keyword=test_keyword)
    if scraped_jobs:
        save_to_csv(scraped_jobs, filename=f"api_jobs_test.csv")
    else:
        print(f"--- No jobs found via API for keyword: {test_keyword} ---")


